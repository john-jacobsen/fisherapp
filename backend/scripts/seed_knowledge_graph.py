"""
Seed the knowledge graph from data/knowledge_graph.json into the database.

Usage (from project root):
    docker compose run --rm backend python scripts/seed_knowledge_graph.py
"""
import json
import os

from app.database import SessionLocal, engine
from app.models.knowledge import KnowledgeGraph, KnowledgeNode, KnowledgeEdge
import app.models  # noqa — register all models

GRAPH_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_graph.json")


def seed():
    with open(GRAPH_PATH, encoding="utf-8") as f:
        graph_data = json.load(f)

    db = SessionLocal()
    try:
        # Deactivate existing graphs
        db.query(KnowledgeGraph).update({"is_active": False})

        # Create new graph
        graph = KnowledgeGraph(
            version=1,
            graph_json=graph_data,
            is_active=True,
        )
        db.add(graph)
        db.flush()  # get graph.id

        # Create nodes
        for item in graph_data["items"]:
            node = KnowledgeNode(
                id=item["id"],
                graph_id=graph.id,
                topic=item.get("topic", item["tags"][0] if item.get("tags") else "Unknown"),
                label=item["label"],
                description=item.get("description", ""),
                display_x=item.get("display_x"),
                display_y=item.get("display_y"),
            )
            db.add(node)

        db.flush()

        # Create edges
        for rel in graph_data["surmise_relations"]:
            edge = KnowledgeEdge(
                graph_id=graph.id,
                from_node_id=rel["prerequisite"],
                to_node_id=rel["target"],
            )
            db.add(edge)

        db.commit()
        print(f"Seeded graph with {len(graph_data['items'])} nodes and {len(graph_data['surmise_relations'])} edges.")
        print(f"Graph ID: {graph.id}")
    except Exception as e:
        db.rollback()
        print(f"Error seeding graph: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
