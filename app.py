
import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler
from ai.agent import PawPalAgent


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="wide"
)

st.title("🐾 PawPal+")
st.write("A simple pet care scheduling assistant.")


# -----------------------------
# Initialize Session State
# -----------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "care_plan" not in st.session_state:
    st.session_state.care_plan = None

owner = st.session_state.owner
scheduler = Scheduler(owner)
agent = PawPalAgent(owner)


# -----------------------------
# Add a Pet
# -----------------------------
st.divider()
st.header("🐾 Add a Pet")

with st.form("add_pet_form"):

    pet_name = st.text_input(
        "Pet Name",
        placeholder="Enter your pet's name"
    )

    species = st.selectbox(
        "Species",
        ["Dog", "Cat", "Other"]
    )

    add_pet_submitted = st.form_submit_button("Add Pet")

    if add_pet_submitted:

        if not pet_name.strip():
            st.warning("Please enter a pet name.")

        elif any(
            pet.name.lower() == pet_name.strip().lower()
            for pet in owner.pets
        ):
            st.warning("A pet with that name already exists.")

        else:
            new_pet = Pet(
                pet_name.strip(),
                species,
                0
            )

            owner.add_pet(new_pet)
            st.session_state.care_plan = None

            st.success(f"{pet_name} was added successfully!")
            st.rerun()


# -----------------------------
# Display Existing Pets
# -----------------------------
if owner.pets:

    st.subheader("Your Pets")

    for pet in owner.pets:
        st.write(f"🐾 **{pet.name}** — {pet.species}")


# -----------------------------
# Add a Task
# -----------------------------
st.divider()
st.header("📝 Add a Task")

if owner.pets:

    # Select the pet by name
    pet_names = [pet.name for pet in owner.pets]

    selected_pet_name = st.selectbox(
        "Select Pet",
        pet_names,
        key="manual_task_pet_name"
    )

    # Retrieve the actual pet object from the owner
    selected_pet = next(
        pet for pet in owner.pets
        if pet.name == selected_pet_name
    )

    task_title = st.text_input(
        "Task",
        placeholder="Example: Morning walk",
        key="manual_task_title"
    )

    task_time = st.text_input(
        "Time",
        placeholder="Example: 08:00",
        key="manual_task_time"
    )

    frequency = st.selectbox(
        "Frequency",
        ["Daily", "Weekly", "One-time"],
        key="manual_task_frequency"
    )

    if st.button("Add Task", key="add_manual_task"):

        if not task_title.strip() or not task_time.strip():

            st.warning("Please enter both a task and a time.")

        else:

            new_task = Task(
                task_title.strip(),
                task_time.strip(),
                frequency
            )

            selected_pet.add_task(new_task)

            st.success(
                f"{task_title.strip()} was added to "
                f"{selected_pet.name}'s schedule!"
            )

else:

    st.info("Add a pet before creating a task.")


# -----------------------------
# AI Care Assistant
# -----------------------------
st.divider()
st.header("🤖 AI Care Assistant")

st.write(
    "Ask a pet-care question to retrieve relevant information "
    "and generate recommendations for your pet."
)

if owner.pets:

    ai_selected_pet = st.selectbox(
        "Choose a pet for the AI assistant",
        owner.pets,
        format_func=lambda pet: pet.name,
        key="ai_selected_pet"
    )

    with st.form("generate_care_plan_form"):

        care_request = st.text_area(
            "What would you like help with?",
            placeholder="Example: How much exercise does my dog need?"
        )

        generate_submitted = st.form_submit_button(
            "Generate Care Plan"
        )

        if generate_submitted:

            if not care_request.strip():

                st.warning(
                    "Please enter a pet-care question or request."
                )

            else:

                with st.spinner("Reviewing pet-care information..."):

                    st.session_state.care_plan = agent.create_care_plan(
                        ai_selected_pet.name,
                        care_request.strip()
                    )

                st.rerun()

    # -----------------------------
    # Display Care Plan
    # -----------------------------
    care_plan = st.session_state.care_plan

    if care_plan:

        plan_pet = care_plan.get("pet")

        if (
            plan_pet is None
            or plan_pet.name.lower() != ai_selected_pet.name.lower()
        ):

            st.info(
                "Generate a new care plan for the selected pet."
            )

        elif not care_plan.get("success"):

            st.warning(
                care_plan.get(
                    "message",
                    "Unable to create care plan."
                )
            )

        else:

            st.success(care_plan["message"])

            st.subheader("📚 Retrieved Pet-Care Information")

            for index, recommendation in enumerate(care_plan["plan"]):

                with st.expander(
                    f"Recommendation {index + 1}: "
                    f"{recommendation['description']}",
                    expanded=True
                ):

                    st.write(recommendation["information"])

                    st.caption(
                        f"Source: {recommendation['source']}"
                    )

                    if recommendation.get("source_url"):

                        st.markdown(
                            f"[View source]({recommendation['source_url']})"
                        )

                    approved_indices = care_plan.get(
                        "approved_recommendations",
                        []
                    )

                    if index in approved_indices:

                        st.success("Already added to the schedule.")

                    elif care_plan.get("rejected"):

                        st.info("This care plan was rejected.")

                    else:

                        with st.form(key=f"approval_form_{index}"):

                            st.write(
                                "Choose when to add this recommendation "
                                "to your pet's schedule."
                            )

                            approval_time = st.text_input(
                                "Scheduled time (24-hour HH:MM)",
                                placeholder="Example: 10:00"
                            )

                            approval_frequency = st.selectbox(
                                "Frequency",
                                ["Daily", "Weekly", "Once"]
                            )

                            approve_submitted = st.form_submit_button(
                                "Approve and Add to Schedule"
                            )

                            if approve_submitted:

                                approval = agent.approve_recommendation(
                                    care_plan,
                                    index,
                                    approval_time.strip(),
                                    approval_frequency
                                )

                                if approval["success"]:

                                    st.success(approval["message"])
                                    st.rerun()

                                else:

                                    st.error(approval["message"])

            # -----------------------------
            # Reject Care Plan
            # -----------------------------
            if (
                not care_plan.get("rejected")
                and not care_plan.get("approved_recommendations")
            ):

                if st.button(
                    "Reject Care Plan",
                    key="reject_care_plan"
                ):

                    rejection = agent.reject_plan(care_plan)

                    if rejection["success"]:

                        st.info(rejection["message"])
                        st.rerun()

                    else:

                        st.error(rejection["message"])

else:

    st.info("Add a pet before using the AI Care Assistant.")


# -----------------------------
# Pet Schedule
# -----------------------------
st.divider()
st.header("📅 Pet Schedule")

all_tasks = scheduler.get_all_tasks()

if all_tasks:

    st.subheader("Sorted Schedule")

    sorted_tasks = scheduler.sort_by_time()

    schedule_data = []

    for task in sorted_tasks:

        schedule_data.append(
            {
                "Time": task.time,
                "Task": task.description,
                "Frequency": task.frequency,
                "Completed": task.completed
            }
        )

    st.table(schedule_data)

    # -----------------------------
    # Schedule Conflicts
    # -----------------------------
    st.subheader("⚠️ Schedule Conflicts")

    conflicts = scheduler.detect_conflicts()

    if conflicts:

        for task1, task2 in conflicts:

            st.warning(
                f"Schedule conflict: **{task1.description}** and "
                f"**{task2.description}** are both scheduled for "
                f"**{task1.time}**."
            )

    else:

        st.success("No scheduling conflicts detected!")

    # -----------------------------
    # Completed Tasks
    # -----------------------------
    st.subheader("✅ Completed Tasks")

    completed_tasks = scheduler.filter_tasks(completed=True)

    if completed_tasks:

        for task in completed_tasks:

            st.success(
                f"{task.time} - {task.description}"
            )

    else:

        st.info("No completed tasks yet.")

else:

    st.info("No tasks have been scheduled yet.")
