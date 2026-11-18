
import json
import re
from pathlib import Path


# Locate the project directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_KNOWLEDGE_BASE = (
    PROJECT_ROOT / "knowledge_base" / "pet_care.json"
)


# Common words that do not help identify a topic.
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "do", "does", "did", "how", "what", "when",
    "where", "why", "who", "my", "me", "i",
    "you", "your", "it", "to", "of", "for",
    "and", "or", "in", "on", "with", "should",
    "can", "could", "would", "about"
}


def load_knowledge_base(file_path=DEFAULT_KNOWLEDGE_BASE):
    """Load pet-care records from the JSON knowledge base."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(
            "The knowledge base must contain a list of records."
        )

    return records


def tokenize(text):
    """Convert text into meaningful lowercase search words."""
    words = set(
        re.findall(r"\b[a-z0-9]+\b", text.lower())
    )

    return words - STOP_WORDS


def retrieve_knowledge(query, species=None, top_k=3, knowledge_base=None):
    """
    Retrieve relevant pet-care information using keyword matching.

    Records are ranked based on matching words in their topic,
    category, and content.
    """
    if not query or not query.strip():
        return []

    if top_k < 1:
        return []

    records = (
        knowledge_base
        if knowledge_base is not None
        else load_knowledge_base()
    )

    query_words = tokenize(query)

    if not query_words:
        return []

    results = []

    for record in records:
        record_species = record.get("species", "All")

        # Filter by species when one is provided.
        if species and record_species.lower() not in {
            species.lower(),
            "all"
        }:
            continue

        topic_words = tokenize(record.get("topic", ""))
        category_words = tokenize(record.get("category", ""))
        content_words = tokenize(record.get("content", ""))

        # Count relevant keyword matches.
        topic_matches = query_words.intersection(topic_words)
        category_matches = query_words.intersection(category_words)
        content_matches = query_words.intersection(content_words)

        # Give more importance to topic and category matches.
        score = (
            len(topic_matches) * 3
            + len(category_matches) * 2
            + len(content_matches)
        )

        # Only return records with meaningful keyword matches.
        if score > 0:
            results.append((score, record))

    # Sort by relevance, highest score first.
    results.sort(key=lambda item: item[0], reverse=True)

    return [
        record
        for score, record in results[:top_k]
    ]


def format_retrieved_knowledge(records):
    """Format retrieved records with their source information."""
    if not records:
        return "No relevant pet-care information was found."

    formatted_results = []

    for record in records:
        formatted_results.append(
            f"Topic: {record.get('topic', 'Unknown')}\n"
            f"Information: {record.get('content', '')}\n"
            f"Source: {record.get('source', 'Unknown')}\n"
            f"Source URL: {record.get('source_url', 'Not provided')}"
        )

    return "\n\n".join(formatted_results)

