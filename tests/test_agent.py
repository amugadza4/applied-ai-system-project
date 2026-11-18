
from pawpal_system import Owner, Pet, Task
from ai.agent import PawPalAgent


def create_test_owner():
    """Create an owner with sample pets and tasks."""
    owner = Owner("Adele")

    buddy = Pet("Buddy", "Dog", 3)
    buddy.add_task(Task("Morning walk", "08:00", "Daily"))

    luna = Pet("Luna", "Cat", 2)
    luna.add_task(Task("Clean litter box", "09:00", "Daily"))

    owner.add_pet(buddy)
    owner.add_pet(luna)

    return owner


def create_dog_plan(agent):
    """Create a valid dog care plan for approval tests."""
    return agent.create_care_plan(
        "Buddy",
        "dog exercise walking"
    )


# --------------------------------------------------
# PET SEARCH TESTS
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

    result = agent.create_care_plan(
        "Buddy",
        "dog exercise walking"
    )

    assert result["success"] is True
    assert result["pet"].name == "Buddy"
    assert len(result["plan"]) > 0
    assert result["approved"] is False


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


def test_missing_pet_returns_error():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Max",
        "exercise"
    )

    assert result["success"] is False
    assert result["plan"] == []


def test_unrelated_request_returns_no_plan():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = agent.create_care_plan(
        "Buddy",
        "repair a computer"
    )

    assert result["success"] is False
    assert result["plan"] == []


def test_care_plan_does_not_modify_existing_tasks():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    buddy = agent.find_pet("Buddy")
    original_task_count = len(buddy.get_tasks())

    agent.create_care_plan(
        "Buddy",
        "dog exercise walking"
    )

    assert len(buddy.get_tasks()) == original_task_count


# --------------------------------------------------
# APPROVAL WORKFLOW TESTS
# --------------------------------------------------

def test_approve_recommendation_adds_task():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)
    original_count = len(result["pet"].get_tasks())

    approval = agent.approve_recommendation(
        result,
        0,
        "10:00",
        "Daily"
    )

    assert approval["success"] is True
    assert len(result["pet"].get_tasks()) == original_count + 1
    assert approval["task"].time == "10:00"
    assert approval["task"].frequency == "Daily"


def test_approval_rejects_invalid_time():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)
    original_count = len(result["pet"].get_tasks())

    approval = agent.approve_recommendation(
        result,
        0,
        "25:90",
        "Daily"
    )

    assert approval["success"] is False
    assert len(result["pet"].get_tasks()) == original_count


def test_approval_rejects_invalid_frequency():
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


def test_approval_prevents_scheduling_conflicts():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)
    original_count = len(result["pet"].get_tasks())

    approval = agent.approve_recommendation(
        result,
        0,
        "09:00",
        "Daily"
    )

    assert approval["success"] is False
    assert approval["message"] == "Scheduling conflict detected."
    assert len(result["pet"].get_tasks()) == original_count


def test_approval_prevents_duplicate_recommendations():
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
    assert len(result["pet"].get_tasks()) == 2


def test_reject_plan_does_not_add_tasks():
    owner = create_test_owner()
    agent = PawPalAgent(owner)

    result = create_dog_plan(agent)
    original_count = len(result["pet"].get_tasks())

    rejection = agent.reject_plan(result)

    assert rejection["success"] is True
    assert result["rejected"] is True
    assert len(result["pet"].get_tasks()) == original_count


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
    assert len(result["pet"].get_tasks()) == 1

