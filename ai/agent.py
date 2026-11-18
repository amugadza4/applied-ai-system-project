
from datetime import datetime

from ai.ai_assistant import (
    retrieve_knowledge,
    format_retrieved_knowledge
)
from ai.interaction_logger import InteractionLogger
from pawpal_system import Task


class PawPalAgent:
    """
    Coordinates pet-care requests using knowledge retrieval,
    safety checks, interaction logging, and owner approval.
    """

    EMERGENCY_KEYWORDS = [
        "difficulty breathing",
        "trouble breathing",
        "can't breathe",
        "cannot breathe",
        "choking",
        "seizure",
        "having a seizure",
        "unconscious",
        "collapsed",
        "collapse",
        "severe bleeding",
        "bleeding heavily",
        "hit by a car",
        "hit by a vehicle",
        "poison",
        "poisoning",
        "toxic substance",
        "ate something toxic",
        "unable to urinate",
        "cannot urinate",
        "can't urinate"
    ]

    DIAGNOSIS_KEYWORDS = [
        "diagnose",
        "diagnosis",
        "what is wrong with",
        "what disease does",
        "does my dog have",
        "does my cat have",
        "does my pet have",
        "is my dog sick",
        "is my cat sick",
        "is my pet sick"
    ]

    def __init__(self, owner):
        self.owner = owner
        self.logger = InteractionLogger()

    def find_pet(self, pet_name):
        """Find a pet belonging to the owner."""
        if not isinstance(pet_name, str):
            return None

        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet

        return None

    def _log_interaction(
        self,
        pet_name,
        species,
        request,
        outcome,
        topics=None
    ):
        """Record an interaction without interrupting the app if logging fails."""
        try:
            self.logger.log_interaction(
                pet_name=pet_name,
                species=species,
                request=request,
                outcome=outcome,
                topics=topics
            )
        except OSError:
            pass

    def _check_emergency(self, request):
        """Check whether a request contains an emergency keyword."""
        request_lower = request.lower()

        return any(
            keyword in request_lower
            for keyword in self.EMERGENCY_KEYWORDS
        )

    def _check_diagnosis_request(self, request):
        """Check whether a user is requesting a medical diagnosis."""
        request_lower = request.lower()

        return any(
            keyword in request_lower
            for keyword in self.DIAGNOSIS_KEYWORDS
        )

    def create_care_plan(self, pet_name, request):
        """Retrieve relevant pet-care information and create recommendations."""

        request = str(request or "").strip()
        pet = self.find_pet(pet_name)

        # Check whether the selected pet exists.
        if pet is None:
            self._log_interaction(
                pet_name,
                None,
                request,
                "pet_not_found"
            )

            return {
                "success": False,
                "message": f"I could not find a pet named {pet_name}.",
                "pet": None,
                "knowledge": [],
                "plan": [],
                "conflicts": []
            }

        # Emergency safety check.
        if self._check_emergency(request):
            message = (
                "This request may describe a veterinary emergency. "
                "Please contact an emergency veterinarian or go to "
                "the nearest emergency animal hospital immediately. "
                "Do not wait for an AI-generated care plan."
            )

            self._log_interaction(
                pet.name,
                pet.species,
                request,
                "emergency_warning"
            )

            return {
                "success": False,
                "message": message,
                "pet": pet,
                "knowledge": [],
                "plan": [],
                "conflicts": [],
                "safety_warning": True
            }

        # Medical diagnosis safety check.
        if self._check_diagnosis_request(request):
            message = (
                "PawPal cannot diagnose medical conditions. "
                "A licensed veterinarian can examine your pet "
                "and provide an accurate diagnosis. Please contact "
                "your veterinarian about your concerns."
            )

            self._log_interaction(
                pet.name,
                pet.species,
                request,
                "medical_boundary"
            )

            return {
                "success": False,
                "message": message,
                "pet": pet,
                "knowledge": [],
                "plan": [],
                "conflicts": [],
                "safety_warning": True
            }

        # Retrieve relevant knowledge.
        knowledge = retrieve_knowledge(
            query=request,
            species=pet.species
        )

        if not knowledge:
            self._log_interaction(
                pet.name,
                pet.species,
                request,
                "no_relevant_information"
            )

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

        # Generate recommendations.
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

        # Check for conflicts with existing pet tasks.
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

        # Log successful interaction.
        self._log_interaction(
            pet.name,
            pet.species,
            request,
            "success",
            topics=[
                record.get("topic", "Unknown")
                for record in knowledge
            ]
        )

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
        """Add an individual recommendation after owner approval."""

        if not isinstance(result, dict) or not result.get("success"):
            return {
                "success": False,
                "message": "There is no valid care plan to approve."
            }

        if result.get("rejected"):
            return {
                "success": False,
                "message": "This care plan has already been rejected."
            }

        pet = result.get("pet")

        if pet is None or self.find_pet(pet.name) is not pet:
            return {
                "success": False,
                "message": "This care plan does not belong to your pet."
            }

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

        # Validate time.
        try:
            datetime.strptime(time, "%H:%M")
        except (ValueError, TypeError):
            return {
                "success": False,
                "message": "Please enter a valid time in HH:MM format."
            }

        # Validate frequency.
        if frequency not in ["Daily", "Weekly", "Once"]:
            return {
                "success": False,
                "message": "Please select Daily, Weekly, or Once."
            }

        approved = result.setdefault(
            "approved_recommendations",
            []
        )

        if recommendation_index in approved:
            return {
                "success": False,
                "message": "This recommendation has already been approved."
            }

        # Prevent scheduling two tasks at the same time.
        for existing_task in self.owner.get_all_tasks():
            try:
                existing_time = existing_task.time

                if existing_time == time:
                    return {
                        "success": False,
                        "message": (
                            f"You already have a task scheduled "
                            f"at {time}. Please choose another time."
                        )
                    }

            except AttributeError:
                continue

        recommendation = plan[recommendation_index]

        new_task = Task(
            description=recommendation["description"],
            time=time,
            frequency=frequency
        )

        pet.add_task(new_task)

        approved.append(recommendation_index)

        result["approved"] = (
            len(approved) == len(plan)
        )

        return {
            "success": True,
            "message": (
                f"{recommendation['description']} "
                f"has been added to {pet.name}'s schedule."
            ),
            "task": new_task
        }

    def reject_plan(self, result):
        """Reject a care plan without adding recommendations."""

        if not isinstance(result, dict) or not result.get("success"):
            return {
                "success": False,
                "message": "There is no valid care plan to reject."
            }

        if result.get("rejected"):
            return {
                "success": False,
                "message": "This care plan has already been rejected."
            }

        pet = result.get("pet")

        if pet is None or self.find_pet(pet.name) is not pet:
            return {
                "success": False,
                "message": "This care plan does not belong to your pet."
            }

        if result.get("approved_recommendations"):
            return {
                "success": False,
                "message": (
                    "Some recommendations have already been approved. "
                    "The plan cannot be rejected after approval."
                )
            }

        result["rejected"] = True

        return {
            "success": True,
            "message": "Care plan rejected. No tasks were added."
        }
