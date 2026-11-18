
import json

from pawpal_system import Owner, Pet, Task
from ai.agent import PawPalAgent


def create_test_owner():
    """Create an owner with one dog and one cat for testing."""
    owner = Owner("Adele")

    buddy = Pet("Buddy", "Dog", 3)
    buddy.add_task(
        Task("Morning walk", "08:00", "Daily")
    )

    luna = Pet("Luna", "Cat", 2)
    luna.add_task(
        Task("Clean litter box", "09:00", "Daily")
    )

    owner.add_pet(buddy)
    owner.add_pet(luna)

    return owner


def create_dog_plan(agent):
    """Create a care plan for Buddy."""
    return agent.create_care_plan(
        "Buddy",
        "dog exercise walking"
    )


# --------------------------------------------------
# PET LOOKUP TESTS
# --------------------------------------------------

def test_find_existing_pet():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    pet = agent.find_pet("Buddy")

    assert pet is not None
    assert pet.name == "Buddy"


def test_find_pet_is_case_insensitive():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    pet = agent.find_pet("buddy")

    assert pet is not None
    assert pet.name == "Buddy"


def test_find_missing_pet():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    pet = agent.find_pet("Max")

    assert pet is None


# --------------------------------------------------
# CARE PLAN TESTS
# --------------------------------------------------

def test_create_dog_care_plan():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)

    assert result["success"] is True
    assert result["pet"].name == "Buddy"
    assert len(result["plan"]) > 0


def test_create_cat_care_plan():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Luna",
        "cat litter box maintenance"
    )

    assert result["success"] is True
    assert result["pet"].name == "Luna"
    assert len(result["plan"]) > 0


def test_care_plan_for_missing_pet():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Max",
        "exercise"
    )

    assert result["success"] is False
    assert result["pet"] is None


def test_unrelated_request_returns_no_results():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Buddy",
        "repair a computer"
    )

    assert result["success"] is False
    assert len(result["plan"]) == 0


def test_creating_plan_does_not_add_tasks():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    buddy = agent.find_pet("Buddy")
    original_count = len(buddy.get_tasks())

    create_dog_plan(agent)

    assert len(buddy.get_tasks()) == original_count


# --------------------------------------------------
# RECOMMENDATION APPROVAL TESTS
# --------------------------------------------------

def test_approve_recommendation_adds_task():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)
    buddy = agent.find_pet("Buddy")

    original_count = len(buddy.get_tasks())

    approval = agent.approve_recommendation(
        result,
        0,
        "10:00",
        "Daily"
    )

    assert approval["success"] is True
    assert len(buddy.get_tasks()) == original_count + 1


def test_approve_recommendation_rejects_invalid_time():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)

    approval = agent.approve_recommendation(
        result,
        0,
        "invalid",
        "Daily"
    )

    assert approval["success"] is False


def test_approve_recommendation_rejects_invalid_frequency():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)

    approval = agent.approve_recommendation(
        result,
        0,
        "10:00",
        "Monthly"
    )

    assert approval["success"] is False


def test_approve_recommendation_detects_time_conflict():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)

    approval = agent.approve_recommendation(
        result,
        0,
        "08:00",
        "Daily"
    )

    assert approval["success"] is False
    assert "already have a task scheduled" in approval["message"]


def test_recommendation_cannot_be_approved_twice():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)

    first_approval = agent.approve_recommendation(
        result,
        0,
        "10:00",
        "Daily"
    )

    second_approval = agent.approve_recommendation(
        result,
        0,
        "11:00",
        "Daily"
    )

    assert first_approval["success"] is True
    assert second_approval["success"] is False


# --------------------------------------------------
# PLAN REJECTION TESTS
# --------------------------------------------------

def test_reject_plan_does_not_add_tasks():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)
    buddy = agent.find_pet("Buddy")

    original_count = len(buddy.get_tasks())

    rejection = agent.reject_plan(result)

    assert rejection["success"] is True
    assert result["rejected"] is True
    assert len(buddy.get_tasks()) == original_count


def test_rejected_plan_cannot_be_approved():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)

    agent.reject_plan(result)

    approval = agent.approve_recommendation(
        result,
        0,
        "10:00",
        "Daily"
    )

    assert approval["success"] is False


# --------------------------------------------------
# SAFETY TESTS
# --------------------------------------------------

def test_emergency_request_returns_warning():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Buddy",
        "My dog is having a seizure"
    )

    assert result["success"] is False
    assert result["safety_warning"] is True
    assert "emergency veterinarian" in result["message"]


def test_emergency_request_does_not_create_tasks():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    buddy = agent.find_pet("Buddy")
    original_count = len(buddy.get_tasks())

    agent.create_care_plan(
        "Buddy",
        "My dog is having trouble breathing"
    )

    assert len(buddy.get_tasks()) == original_count


def test_diagnosis_request_returns_warning():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Buddy",
        "Can you diagnose my dog?"
    )

    assert result["success"] is False
    assert result["safety_warning"] is True
    assert "cannot diagnose" in result["message"]


# --------------------------------------------------
# INTERACTION LOGGING TESTS
# --------------------------------------------------

def test_emergency_request_is_logged(tmp_path):
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    agent.logger.log_path = tmp_path / "interactions.jsonl"

    agent.create_care_plan(
        "Buddy",
        "My dog is choking"
    )

    with agent.logger.log_path.open(encoding="utf-8") as file:
        record = json.loads(file.readline())

    assert record["outcome"] == "emergency_warning"
    assert record["pet_name"] == "Buddy"


def test_successful_request_is_logged(tmp_path):
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    agent.logger.log_path = tmp_path / "interactions.jsonl"

    agent.create_care_plan(
        "Buddy",
        "dog exercise walking"
    )

    with agent.logger.log_path.open(encoding="utf-8") as file:
        record = json.loads(file.readline())

    assert record["outcome"] == "success"
    assert record["pet_name"] == "Buddy"
    assert len(record["topics"]) > 0


def test_unrelated_request_is_logged(tmp_path):
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    agent.logger.log_path = tmp_path / "interactions.jsonl"

    agent.create_care_plan(
        "Buddy",
        "repair a computer"
    )

    with agent.logger.log_path.open(encoding="utf-8") as file:
        record = json.loads(file.readline())

    assert record["outcome"] == "no_relevant_information"
