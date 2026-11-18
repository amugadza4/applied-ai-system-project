
from ai.ai_assistant import (
    load_knowledge_base,
    retrieve_knowledge,
    format_retrieved_knowledge
)


def test_load_knowledge_base():
    records = load_knowledge_base()

    assert len(records) == 7


def test_retrieve_dog_exercise_information():
    results = retrieve_knowledge(
        "How much exercise does my dog need?",
        species="Dog"
    )

    assert len(results) > 0
    assert results[0]["id"] == "DOG001"


def test_retrieve_cat_litter_information():
    results = retrieve_knowledge(
        "How do I maintain a cat litter box?",
        species="Cat"
    )

    assert len(results) > 0
    assert results[0]["id"] == "CAT002"


def test_species_filter():
    results = retrieve_knowledge(
        "dog exercise walking",
        species="Cat"
    )

    assert all(
        record["species"] in ["Cat", "All"]
        for record in results
    )


def test_no_results_for_unrelated_question():
    results = retrieve_knowledge(
        "How do I repair a computer?"
    )

    assert results == []


def test_format_retrieved_knowledge():
    records = retrieve_knowledge(
        "cat litter box",
        species="Cat"
    )

    formatted = format_retrieved_knowledge(records)

    assert "Cornell Feline Health Center" in formatted
    assert "Source URL" in formatted


