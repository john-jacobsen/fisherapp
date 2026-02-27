"""
KST Engine — wrapper around kst_utils.py with database integration and caching.
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session as DBSession

from app.config import settings
from app.kst.kst_utils import (
    transitive_closure,
    enumerate_downsets,
    compute_fringes,
    blim_update,
    select_assessment_item,
    entropy,
    validate_graph,
)
from app.models.knowledge import KnowledgeGraph, KnowledgeNode, KnowledgeEdge
from app.models.progress import StudentState

logger = logging.getLogger(__name__)

LUCKY_GUESS = settings.blim_lucky_guess
CARELESS_ERROR = settings.blim_careless_error
MASTERY_THRESHOLD = settings.blim_mastery_threshold
ENTROPY_TERMINATION = settings.blim_entropy_termination

# In-memory cache keyed by graph_id
_state_cache: dict[str, dict] = {}


def _get_relations(db: DBSession, graph_id: str) -> list[tuple[str, str]]:
    """Get all prerequisite edges as (prerequisite, target) pairs."""
    edges = db.query(KnowledgeEdge).filter(KnowledgeEdge.graph_id == graph_id).all()
    return [(e.from_node_id, e.to_node_id) for e in edges]


def _get_items(db: DBSession, graph_id: str) -> list[str]:
    """Get all node IDs for a graph."""
    nodes = db.query(KnowledgeNode.id).filter(KnowledgeNode.graph_id == graph_id).all()
    return [n.id for n in nodes]


def _build_graph_dict(items: list[str], relations: list[tuple[str, str]]) -> dict:
    """Build a graph dict in the format expected by kst_utils functions."""
    return {
        "items": [{"id": iid} for iid in items],
        "surmise_relations": [
            {"prerequisite": p, "target": t, "confidence": 1.0, "relation_type": "prerequisite-of"}
            for p, t in relations
        ],
    }


def _state_key(s: frozenset) -> str:
    """Serialize a frozenset state to a stable string key."""
    return "|".join(sorted(s))


def get_or_build_cache(db: DBSession, graph_id: str) -> dict:
    """
    Build (or return cached) the knowledge states enumeration for a graph.
    Caches: items list, relations, transitive closure, and enumerated downsets.
    """
    graph_id_str = str(graph_id)
    if graph_id_str in _state_cache:
        return _state_cache[graph_id_str]

    items = _get_items(db, graph_id)
    relations = _get_relations(db, graph_id)

    # Build graph dict as required by kst_utils
    graph = _build_graph_dict(items, relations)

    # Compute transitive closure — returns list of new relation dicts
    new_rels = transitive_closure(graph)
    closed_graph = {
        "items": graph["items"],
        "surmise_relations": graph["surmise_relations"] + new_rels,
    }

    try:
        states = enumerate_downsets(closed_graph)
        if len(states) > 10000:
            logger.warning(
                "State space has %d states (>10000) for graph %s. "
                "Using full enumeration — consider pruning the graph.",
                len(states), graph_id_str
            )
    except Exception as e:
        logger.error("Failed to enumerate states for graph %s: %s", graph_id_str, e)
        states = [frozenset(), frozenset(items)]

    # states_dict: {string_key -> frozenset} for blim_update and select_assessment_item
    states_dict = {_state_key(s): s for s in states}

    cache = {
        "items": items,
        "item_ids_set": set(items),
        "relations": relations,
        "closed_graph": closed_graph,
        "states": states,           # list[frozenset[str]]
        "states_set": set(states),  # set[frozenset[str]]
        "states_dict": states_dict, # dict[str, frozenset[str]]
        "graph_id": graph_id_str,
    }
    _state_cache[graph_id_str] = cache
    logger.info("Cached %d knowledge states for graph %s", len(states), graph_id_str)
    return cache


def clear_cache(graph_id: Optional[str] = None):
    """Clear state cache. Pass graph_id to clear specific graph, or None to clear all."""
    if graph_id:
        _state_cache.pop(str(graph_id), None)
    else:
        _state_cache.clear()


def get_active_graph(db: DBSession) -> Optional[KnowledgeGraph]:
    """Return the active knowledge graph."""
    return db.query(KnowledgeGraph).filter(KnowledgeGraph.is_active == True).first()


def initialize_uniform_prior(db: DBSession, graph_id: str) -> dict:
    """Create a uniform prior distribution over all knowledge states."""
    cache = get_or_build_cache(db, graph_id)
    states = cache["states"]
    n = len(states)
    if n == 0:
        return {}
    prob = 1.0 / n
    return {_state_key(s): prob for s in states}


def run_blim_update(
    db: DBSession,
    graph_id: str,
    prior: dict,
    item_id: str,
    is_correct: bool,
) -> dict:
    """
    Run BLIM update after a student response.
    prior: {state_key: probability}
    Returns updated posterior distribution.
    """
    cache = get_or_build_cache(db, graph_id)
    states_dict = cache["states_dict"]  # {str_key: frozenset}

    try:
        updated = blim_update(
            state_probs=prior,
            states=states_dict,
            item_id=item_id,
            response_correct=is_correct,
            lucky_guess=LUCKY_GUESS,
            careless_error=CARELESS_ERROR,
        )
        total = sum(updated.values())
        if total == 0:
            return prior
        return {k: v / total for k, v in updated.items()}
    except Exception as e:
        logger.error("BLIM update failed: %s", e)
        return prior


def get_mastered_nodes_from_distribution(distribution: dict) -> list[str]:
    """
    Find the most probable knowledge state and return its items as mastered nodes.
    """
    if not distribution:
        return []
    best_key = max(distribution, key=lambda k: distribution[k])
    if not best_key:
        return []
    return best_key.split("|")


def compute_node_fringes(db: DBSession, graph_id: str, mastered_set: set[str]) -> tuple[list[str], list[str]]:
    """
    Compute inner and outer fringes for a given set of mastered nodes.
    Returns (inner_fringe, outer_fringe).
    """
    cache = get_or_build_cache(db, graph_id)
    states_set = cache["states_set"]
    item_ids = cache["item_ids_set"]

    try:
        inner, outer = compute_fringes(frozenset(mastered_set), states_set, item_ids)
        return inner, outer
    except Exception as e:
        logger.error("Fringe computation failed: %s", e)
        return [], []


def select_next_assessment_item(
    db: DBSession,
    graph_id: str,
    distribution: dict,
    asked_items: list[str],
) -> Optional[str]:
    """
    Select the most informative next assessment item using maximum discrimination.
    Excludes already-asked items.
    """
    cache = get_or_build_cache(db, graph_id)
    states_dict = cache["states_dict"]
    all_items = cache["item_ids_set"]
    assessed = set(asked_items)

    if not (all_items - assessed):
        return None

    try:
        selected = select_assessment_item(
            state_probs=distribution,
            states=states_dict,
            assessed_items=assessed,
            all_item_ids=all_items,
        )
        return selected
    except Exception as e:
        logger.error("Assessment item selection failed: %s", e)
        remaining = [i for i in cache["items"] if i not in assessed]
        return remaining[0] if remaining else None


def get_distribution_entropy(distribution: dict) -> float:
    """Compute Shannon entropy of a state distribution."""
    if not distribution:
        return 0.0
    try:
        return entropy(distribution)
    except Exception as e:
        logger.error("Entropy computation failed: %s", e)
        return 0.0


def update_student_state(
    db: DBSession,
    user_id: str,
    graph: KnowledgeGraph,
    new_distribution: dict,
) -> StudentState:
    """
    Recompute and save student state after a distribution update.
    Creates state if it doesn't exist.
    """
    graph_id = str(graph.id)
    mastered = get_mastered_nodes_from_distribution(new_distribution)
    inner, outer = compute_node_fringes(db, graph_id, set(mastered))

    state = db.query(StudentState).filter(
        StudentState.user_id == user_id,
        StudentState.graph_id == graph.id,
    ).first()

    if state:
        state.state_distribution = new_distribution
        state.mastered_nodes = mastered
        state.inner_fringe = inner
        state.outer_fringe = outer
    else:
        state = StudentState(
            user_id=user_id,
            graph_id=graph.id,
            graph_version=graph.version,
            state_distribution=new_distribution,
            mastered_nodes=mastered,
            outer_fringe=outer,
            inner_fringe=inner,
        )
        db.add(state)

    db.commit()
    db.refresh(state)
    return state
