
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
