
import json

from ai.interaction_logger import InteractionLogger


def test_logger_creates_log_file(tmp_path):
    log_path = tmp_path / "logs" / "interactions.jsonl"
    logger = InteractionLogger(log_path)

    logger.log_interaction(
        pet_name="Buddy",
        species="Dog",
        request="How much exercise does my dog need?",
        outcome="success",
        topics=["Daily exercise"]
    )

    assert log_path.exists()


def test_logger_saves_interaction_details(tmp_path):
    log_path = tmp_path / "interactions.jsonl"
    logger = InteractionLogger(log_path)

    logger.log_interaction(
        pet_name="Luna",
        species="Cat",
        request="How do I maintain a litter box?",
        outcome="success",
        topics=["Litter box maintenance"]
    )

    with log_path.open(encoding="utf-8") as file:
        record = json.loads(file.readline())

    assert record["pet_name"] == "Luna"
    assert record["species"] == "Cat"
    assert record["outcome"] == "success"
    assert record["topics"] == ["Litter box maintenance"]
    assert record["timestamp"]


def test_logger_appends_multiple_interactions(tmp_path):
    log_path = tmp_path / "interactions.jsonl"
    logger = InteractionLogger(log_path)

    logger.log_interaction(
        "Buddy", "Dog", "Exercise", "success"
    )
    logger.log_interaction(
        "Luna", "Cat", "Litter box", "success"
    )

    with log_path.open(encoding="utf-8") as file:
        records = [json.loads(line) for line in file]

    assert len(records) == 2
    assert records[0]["pet_name"] == "Buddy"
    assert records[1]["pet_name"] == "Luna"
