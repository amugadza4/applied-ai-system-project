
from ai.ai_assistant import (
    retrieve_knowledge,
    format_retrieved_knowledge
)


class PawPalAgent:
    """
    Coordinates pet-care requests by retrieving information,
    creating proposed plans, and checking scheduling conflicts.
    """

    def __init__(self, owner):
        self.owner = owner

    def find_pet(self, pet_name):
        """Find a pet belonging to the owner."""
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet

        return None

    def create_care_plan(self, pet_name, request):
        """
        Retrieve relevant pet-care information and prepare
        a proposed care plan without changing the schedule.
        """

        # Step 1: Find the requested pet.
        pet = self.find_pet(pet_name)

        if pet is None:
            return {
                "success": False,
                "message": f"I could not find a pet named {pet_name}.",
                "pet": None,
                "knowledge": [],
                "plan": [],
                "conflicts": []
            }

        # Step 2: Retrieve relevant knowledge.
        knowledge = retrieve_knowledge(
            query=request,
            species=pet.species
        )

        if not knowledge:
            return {
                "success": False,
                "message": (
                    "I could not find relevant information "
                    "to create a care plan for this request."
                ),
                "pet": pet,
                "knowledge": [],
                "plan": [],
                "conflicts": []
            }

        # Step 3: Prepare a proposed plan.
        # This initial version uses retrieved topics as
        # recommendations rather than inventing exact schedules.
        plan = []

        for record in knowledge:
            plan.append({
                "description": record.get("topic", "Pet care task"),
                "information": record.get("content", ""),
                "source": record.get("source", "Unknown"),
                "source_url": record.get("source_url", "")
            })

        # Step 4: Check existing schedule conflicts.
        existing_tasks = pet.get_tasks()

        conflicts = []

        for proposed_task in plan:
            for existing_task in existing_tasks:
                if (
                    proposed_task["description"].lower()
                    == existing_task.description.lower()
                ):
                    conflicts.append({
                        "proposed_task": proposed_task["description"],
                        "existing_task": existing_task.description,
                        "time": existing_task.time
                    })

        # Step 5: Return the proposal for human review.
        return {
            "success": True,
            "message": "Care plan created for review.",
            "pet": pet,
            "knowledge": knowledge,
            "formatted_knowledge": format_retrieved_knowledge(knowledge),
            "plan": plan,
            "conflicts": conflicts,
            "approved": False
        }
