#!/usr/bin/env python3
"""
Import OATutor algebra content into Fisher App's problems and hints tables.

Usage:
    1. Clone OATutor into the backend directory:
       git clone https://github.com/CAHLR/OATutor backend/oatutor
    2. Run (from project root):
       docker compose run --rm backend python scripts/import_oatutor_content.py
"""
import os
import sys
import json
import uuid
from pathlib import Path

OATUTOR_DIR = Path(__file__).parent.parent / "oatutor"
CONTENT_DIR = OATUTOR_DIR / "content"

SKILL_MAP = {
    "fraction": "frac_basic",
    "fraction-add": "frac_add_sub",
    "fraction-subtract": "frac_add_sub",
    "fraction-multiply": "frac_mult_div",
    "fraction-divide": "frac_mult_div",
    "fraction-simplify": "frac_basic",
    "exponent": "exp_basic",
    "power-rule": "exp_power_rule",
    "negative-exponent": "exp_negative",
    "exponent-product": "exp_product",
    "exponent-quotient": "exp_product",
    "order-of-operations": "order_ops",
    "pemdas": "order_ops",
    "linear-equation": "eq_linear_one",
    "equation-system": "eq_system",
    "quadratic": "eq_quadratic",
    "logarithm": "log_basic",
    "log-rule": "log_properties",
    "natural-log": "log_ln",
    "summation": "sigma_basic",
    "sigma": "sigma_basic",
    "combination": "comb_basic",
    "permutation": "perm_basic",
    "geometric-series": "geom_series",
    "geometric-sequence": "geom_sequence",
}


def map_answer_type(oatutor_type: str) -> str:
    t = (oatutor_type or "").lower()
    if "multiplechoice" in t or "multiple" in t:
        return "multiple_choice"
    return "symbolic"


def extract_answer(answers_field) -> str:
    if not answers_field:
        return ""
    if isinstance(answers_field, list):
        first = answers_field[0] if answers_field else {}
        if isinstance(first, dict):
            return str(first.get("answer", first.get("value", "")))
        return str(first)
    if isinstance(answers_field, dict):
        return str(answers_field.get("answer", answers_field.get("value", "")))
    return str(answers_field)


def extract_choices(problem_data: dict) -> list:
    choices = problem_data.get("choices", problem_data.get("multipleChoiceAnswers", []))
    if not isinstance(choices, list):
        return []
    return [str(c.get("text", c) if isinstance(c, dict) else c) for c in choices[:6]]


def extract_hints(problem_data: dict) -> list:
    """Extract up to 3 hint levels from OATutor hints array."""
    hints = problem_data.get("hints", problem_data.get("hint", []))
    if not hints:
        return []
    if isinstance(hints, str):
        return [hints]

    texts = []
    for h in hints[:3]:
        if isinstance(h, dict):
            texts.append(str(h.get("value", h.get("text", str(h)))))
        else:
            texts.append(str(h))
    return texts


def find_node_id(problem_data: dict):
    """Find the Fisher App node ID from OATutor skill tags."""
    skill_tags = problem_data.get("skillId", problem_data.get("skill", []))
    if isinstance(skill_tags, str):
        skill_tags = [skill_tags]

    for tag in skill_tags:
        tag_lower = tag.lower().replace("_", "-")
        if tag_lower in SKILL_MAP:
            return SKILL_MAP[tag_lower]
        # Partial match
        for key, val in SKILL_MAP.items():
            if key in tag_lower:
                return val
    return None


def main():
    if not OATUTOR_DIR.exists():
        print(f"OATutor directory not found at: {OATUTOR_DIR}")
        print()
        print("To import OATutor content, clone it into the backend directory:")
        print("  git clone https://github.com/CAHLR/OATutor backend/oatutor")
        print("  Then re-run this script.")
        sys.exit(0)

    if not CONTENT_DIR.exists():
        print(f"OATutor content directory not found at: {CONTENT_DIR}")
        sys.exit(1)

    from app.database import SessionLocal
    from app.models.content import Problem, Hint
    from app.models.knowledge import KnowledgeNode

    db = SessionLocal()

    # Collect all node IDs from DB
    db_nodes = {n.id: n for n in db.query(KnowledgeNode).all()}
    print(f"Found {len(db_nodes)} knowledge nodes in database.")

    # Find all JSON files
    json_files = list(CONTENT_DIR.rglob("*.json"))
    print(f"Found {len(json_files)} JSON files in OATutor content directory.")

    imported = 0
    skipped_no_node = 0
    skipped_no_answer = 0
    errors = 0

    for json_file in json_files:
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [error] Could not parse {json_file.name}: {e}")
            errors += 1
            continue

        # OATutor files can be single problem or array
        problems_list = data if isinstance(data, list) else [data]

        for problem_data in problems_list:
            if not isinstance(problem_data, dict):
                continue

            node_id = find_node_id(problem_data)
            if not node_id or node_id not in db_nodes:
                skipped_no_node += 1
                continue

            statement = (
                problem_data.get("question")
                or problem_data.get("body")
                or problem_data.get("title")
                or ""
            )
            if not statement:
                skipped_no_node += 1
                continue

            correct_answer = extract_answer(
                problem_data.get("answers", problem_data.get("answer"))
            )
            if not correct_answer:
                skipped_no_answer += 1
                continue

            answer_type = map_answer_type(problem_data.get("type", ""))
            choices = extract_choices(problem_data) if answer_type == "multiple_choice" else None
            hint_texts = extract_hints(problem_data)

            # Check if problem already imported (by statement + node_id)
            existing = db.query(Problem).filter(
                Problem.node_id == node_id,
                Problem.problem_text == statement,
            ).first()

            if existing:
                # Already imported — skip
                continue

            # Build metadata dict for choices (stored in JSONB metadata_ column)
            metadata = {}
            if choices:
                metadata["choices"] = choices

            prob = Problem(
                id=uuid.uuid4(),
                node_id=node_id,
                problem_text=statement,
                answer_type=answer_type,
                correct_answer=correct_answer,
                difficulty=0.5,
                source="oatutor",
                metadata_=metadata if metadata else None,
            )
            db.add(prob)
            db.flush()  # get prob.id before inserting hints

            # Add hints (level 1, 2, 3)
            for level, hint_text in enumerate(hint_texts, start=1):
                hint = Hint(
                    id=uuid.uuid4(),
                    problem_id=prob.id,
                    level=level,
                    hint_text=hint_text,
                )
                db.add(hint)

            imported += 1
            if imported % 100 == 0:
                print(f"  ... imported {imported} problems so far")
                db.flush()

    db.commit()
    db.close()

    print()
    print("=== OATutor Import Summary ===")
    print(f"  Imported: {imported} problems")
    print(f"  Skipped (no node mapping): {skipped_no_node}")
    print(f"  Skipped (no answer): {skipped_no_answer}")
    print(f"  Errors: {errors}")


if __name__ == "__main__":
    main()
