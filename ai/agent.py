
from datetime import datetime

from ai.ai_assistant import (
    retrieve_knowledge,
    format_retrieved_knowledge
)

from pawpal_system import Task


class PawPalAgent:
    """
    Coordinates pet-care requests by retrieving information,
    creating proposed plans, checking conflicts, and managing
    owner approval before modifying the pet schedule.
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

        # Step 3: Prepare a proposed care plan.
        plan = []

        for record in knowledge:
            plan.append({
                "description": record.get(
                    "topic",
                    "Pet care task"
                ),
                "information": record.get("content", ""),
                "source": record.get("source", "Unknown"),
                "source_url": record.get("source_url", "")
            })

        # Step 4: Check for matching existing recommendations.
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

        # Step 5: Return the proposal for owner review.
        return {
            "success": True,
            "message": "Care plan created for review.",
            "pet": pet,
            "knowledge": knowledge,
            "formatted_knowledge": format_retrieved_knowledge(
                knowledge
            ),
            "plan": plan,
            "conflicts": conflicts,
            "approved": False,
            "approved_recommendations": [],
            "rejected": False
        }

    def approve_recommendation(
        self,
        result,
        recommendation_index,
        time,
        frequency
    ):
        """
        Approve a recommendation and add it to the pet's schedule.
        """

        # Step 1: Validate the care plan.
        if not result or not result.get("success"):
            return {
                "success": False,
                "message": "There is no valid care plan to approve."
            }

        if result.get("rejected"):
            return {
                "success": False,
                "message": "This care plan has already been rejected."
            }

        # Step 2: Verify the pet belongs to the owner.
        pet = result.get("pet")

        if not any(
            existing_pet is pet
            for existing_pet in self.owner.pets
        ):
            return {
                "success": False,
                "message": "This pet does not belong to this owner."
            }

        # Step 3: Validate the selected recommendation.
        plan = result.get("plan", [])

        if (
            not isinstance(recommendation_index, int)
            or isinstance(recommendation_index, bool)
            or recommendation_index < 0
            or recommendation_index >= len(plan)
        ):
            return {
                "success": False,
                "message": "Invalid recommendation selection."
            }

        # Step 4: Validate the scheduled time.
        try:
            parsed_time = datetime.strptime(time, "%H:%M")

            if parsed_time.strftime("%H:%M") != time:
                raise ValueError

        except (ValueError, TypeError):
            return {
                "success": False,
                "message": (
                    "Please enter a valid time in HH:MM format."
                )
            }

        # Step 5: Validate task frequency.
        if frequency not in ["Daily", "Weekly", "Once"]:
            return {
                "success": False,
                "message": "Invalid task frequency."
            }

        # Step 6: Prevent duplicate approvals.
        approved_indices = result.setdefault(
            "approved_recommendations",
            []
        )

        if recommendation_index in approved_indices:
            return {
                "success": False,
                "message": (
                    "This recommendation has already been approved."
                )
            }

        recommendation = plan[recommendation_index]
        description = recommendation.get("description")

        if not description:
            return {
                "success": False,
                "message": "The recommendation has no task description."
            }

        # Step 7: Check for scheduling conflicts.
        conflicting_tasks = [
            task
            for task in self.owner.get_all_tasks()
            if task.time == time
        ]

        if conflicting_tasks:
            return {
                "success": False,
                "message": "Scheduling conflict detected.",
                "conflicts": conflicting_tasks
            }

        # Step 8: Add the task after all checks pass.
        new_task = Task(
            description=description,
            time=time,
            frequency=frequency
        )

        pet.add_task(new_task)

        approved_indices.append(recommendation_index)

        result["approved"] = True

        return {
            "success": True,
            "message": (
                "Recommendation approved and added to the schedule."
            ),
            "task": new_task
        }

    def reject_plan(self, result):
        """
        Reject a care plan without changing the pet's schedule.
        """

        # Step 1: Validate the care plan.
        if not result or not result.get("success"):
            return {
                "success": False,
                "message": "There is no valid care plan to reject."
            }

        # Step 2: Verify the pet belongs to the owner.
        if not any(
            result.get("pet") is pet
            for pet in self.owner.pets
        ):
            return {
                "success": False,
                "message": "This pet does not belong to this owner."
            }

        # Step 3: Do not reject a plan with approved tasks.
        if result.get("approved_recommendations"):
            return {
                "success": False,
                "message": (
                    "Some recommendations have already been approved."
                )
            }

        # Step 4: Mark the proposal as rejected.
        result["rejected"] = True

        return {
            "success": True,
            "message": (
                "Care plan rejected. No tasks were added."
            )
        }
