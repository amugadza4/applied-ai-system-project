# PawPal+ 🐾
### Pet Care Scheduling and AI-Assisted Planning Application

## Project Overview

**Original project: PawPal+ (Module 3)**

PawPal originally focused on helping pet owners organize their pets' care routines through pet management and task scheduling. Its core capabilities allowed users to add pets, create care tasks, organize schedules, and track completed responsibilities.

PawPal+ expands that original project by introducing a retrieval-based pet-care assistant, a rule-driven agent workflow, safety checks, and interaction logging.

PawPal+ is a Python and Streamlit application designed to help pet owners manage everyday care responsibilities while accessing relevant pet-care information. It combines traditional software engineering with a structured knowledge-retrieval workflow and keeps owners in control of scheduling decisions.

## Features

### 1. Pet Management
- Add pets to an owner's profile.
- Store pet names and species.
- Select a pet when creating tasks or requesting recommendations.

### 2. Pet Care Scheduling
- Create tasks for individual pets.
- Set task descriptions, scheduled times, and frequencies.
- Organize tasks chronologically.
- Mark tasks as completed.
- Support Daily, Weekly, and Once task frequencies.
- Identify scheduling conflicts.

### 3. AI-Assisted Pet Care

PawPal+ uses a retrieval-based, rule-driven agent to coordinate pet-care requests.

The assistant can:
- Retrieve relevant information from a curated pet-care knowledge base.
- Use the selected pet's species to filter relevant information.
- Organize retrieved information into care recommendations.
- Display supporting sources.
- Check recommendations against existing tasks.
- Present recommendations for owner review.

### 4. Owner Approval Workflow

PawPal+ keeps the owner involved in scheduling decisions.

- Recommendations are not automatically added to the schedule.
- Owners can approve individual recommendations.
- Approved recommendations become scheduled pet-care tasks.
- Owners can reject a care plan before approving recommendations.
- The application checks for scheduling conflicts before adding tasks.

### 5. Safety Guardrails

The application includes basic keyword-based safety checks.

- Emergency-related requests trigger a warning directing owners to contact an emergency veterinarian.
- Medical diagnosis requests are redirected to a licensed veterinarian.
- Requests without relevant knowledge-base information receive a response explaining that no relevant information was found.

PawPal+ is an informational and organizational tool. It does not diagnose medical conditions or replace professional veterinary advice.

### 6. Interaction Logging

The application records AI assistant interactions in JSON Lines format.

Logged information includes:
- Timestamp
- Pet name
- Pet species
- User request
- Interaction outcome
- Retrieved knowledge topics

Logs are stored locally in `logs/ai_interactions.jsonl` and excluded from version control.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic, scheduling, and agent workflow |
| Streamlit | Interactive web application |
| JSON | Structured pet-care knowledge base |
| Pytest | Automated testing |
| Git and GitHub | Version control and project management |

## Architecture Overview

PawPal+ is organized into four main parts:

1. **Core application (`pawpal_system.py`):** Defines the Owner, Pet, Task, and Scheduler classes and manages pet information and scheduling functionality.
2. **AI components (`ai/`):** Handles knowledge retrieval, agent decisions, recommendation approval, safety checks, and interaction logging.
3. **Knowledge base (`knowledge_base/`):** Stores curated pet-care information in a structured JSON file.
4. **User interface (`app.py`):** Connects the core application and AI components through Streamlit.

The architecture diagram in `diagrams/architecture.mmd` illustrates how a user's request moves through the application. The request is handled by the agent, checked against safety rules, and passed to the retrieval component. Retrieved information is used to create recommendations, which the owner can review before approved tasks are added to the scheduling system.

The UML diagrams in `diagrams/` show the relationships and responsibilities of the application's main classes.

## How the AI Assistant Works

PawPal+ uses a retrieval-based, rule-driven workflow rather than a generative AI model or external language model API.

The workflow follows these steps:

1. **User Request:** The owner selects a pet and submits a pet-care question.
2. **Safety Checks:** The agent checks for emergency-related requests and medical diagnosis requests.
3. **Knowledge Retrieval:** The assistant searches the curated JSON knowledge base using keyword matching and relevance scoring.
4. **Recommendation Generation:** The agent organizes relevant retrieved information into recommendations.
5. **Conflict Detection:** The system checks recommendations against the pet's existing tasks.
6. **Owner Review:** The owner reviews recommendations and chooses whether to approve or reject them.
7. **Schedule Update:** Approved recommendations are added to the pet's schedule.
8. **Interaction Logging:** The application records the interaction and its outcome.

This approach demonstrates how structured information retrieval, decision rules, safety checks, and human oversight can work together in an AI-assisted application.

## Sample Interactions

The following examples demonstrate the application's intended behavior and manually verified safety responses.

### Example 1: Pet-care information request

**Input:**

"How much exercise does my dog need?"

**Application behavior:**

- Retrieves relevant dog exercise information from the knowledge base.
- Displays the retrieved information and its supporting source.
- Presents care recommendations for the owner to review.
- Allows the owner to approve recommendations before they are added to the schedule.

**Result:** The normal recommendation and approval workflow was tested successfully.

### Example 2: Medical diagnosis request

**Input:**

"What is wrong with my dog?"

**Application output:**

"PawPal cannot diagnose medical conditions. A licensed veterinarian can examine your pet and provide an accurate diagnosis. Please contact your veterinarian about your concerns."

**Result:** The safety check prevents the application from generating a care plan for a diagnosis-related request.

### Example 3: Potential veterinary emergency

**Input:**

"My dog is having trouble breathing."

**Application output:**

"This request may describe a veterinary emergency. Please contact an emergency veterinarian or go to the nearest emergency animal hospital immediately. Do not wait for an AI-generated care plan."

**Result:** The emergency safety check displays an urgent warning instead of proceeding with a normal care plan.

## Knowledge Base

The pet-care knowledge base is stored in:

`knowledge_base/pet_care.json`

It contains curated information covering topics such as:

- Dog exercise
- Feeding routines
- Veterinary checkups
- Cat litter box maintenance
- Cat enrichment and play
- Veterinary emergencies

The retrieval system uses keyword matching and relevance scoring to identify potentially relevant information.

Retrieved information includes its topic, content, source, and source URL.

## Scheduling System

The core scheduling functionality is implemented in `pawpal_system.py`.

| Method | Responsibility |
|---|---|
| `Task.mark_complete()` | Marks a task as completed and handles recurring tasks. |
| `Pet.add_task()` | Adds a task to a pet. |
| `Pet.get_tasks()` | Retrieves a pet's tasks. |
| `Scheduler.sort_by_time()` | Sorts tasks chronologically. |
| `Scheduler.filter_tasks()` | Filters tasks by pet or completion status. |
| `Scheduler.detect_conflicts()` | Identifies tasks scheduled at the same time. |

One scheduling trade-off is that conflict detection currently checks for matching scheduled times rather than overlapping task durations. This keeps the implementation simple because tasks do not currently have duration or date attributes.

## Installation and Setup

### Requirements

- Python 3.12 or a compatible Python version
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/amugadza4/applied-ai-system-project.git
```

### 2. Navigate to the project directory

```bash
cd applied-ai-system-project
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the virtual environment

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Running PawPal+

### Launch the Streamlit application

```bash
streamlit run app.py
```

Streamlit will provide a local URL that you can open in your browser.

### Run the command-line application

```bash
python3 main.py
```

## Reliability and Testing

PawPal+ uses Pytest to evaluate the core scheduling functionality, knowledge retrieval, agent workflow, safety checks, and interaction logging.

Run the complete test suite:

```bash
python -m pytest -v
```

Or use:

```bash
python -m pytest -q
```

### Test Coverage

| Test File | Functionality |
|---|---|
| `test_pawpal_system.py` | Pet management, task management, recurring tasks, sorting, and conflicts |
| `test_ai_assistant.py` | Knowledge retrieval and handling unrelated requests |
| `test_agent.py` | Care-plan creation, approval, rejection, safety checks, and logging |
| `test_interaction_logger.py` | Log creation, interaction details, and multiple records |

**Latest verified test result: 35 passed.**

### What Worked

- Core pet-management and scheduling functionality.
- Chronological task organization.
- Retrieval of relevant pet-care information.
- Recommendation review and approval.
- Emergency and diagnosis-related safety warnings.
- Local interaction logging.

### Limitations and Lessons Learned

Keyword-based retrieval can return information that is not perfectly relevant to every question. The safety checks also rely on predefined keywords, so they cannot recognize every possible emergency or medical concern. Conflict detection does not account for task duration.

Testing helped identify issues and verify that individual components worked together. It also reinforced the importance of testing the actual user experience rather than relying only on code-level checks.

## Project Documentation

Additional project materials:

- `model_card.md` — Responsible-AI considerations, collaboration, and system limitations.
- `ai_interactions.md` — Documentation for applicable AI-related stretch features.
- `reflection.md` — General project development reflection.
- `diagrams/` — UML and architecture diagrams.

## Future Improvements

Potential enhancements include:

- More advanced natural-language understanding.
- Improved knowledge retrieval and relevance ranking.
- More detailed pet profiles and personalized recommendations.
- Date-based scheduling and task-duration support.
- More advanced scheduling conflict detection.
- Expanded pet-care knowledge sources.
- Additional safety and evaluation tests.

## Project Reflection

Building PawPal+ helped me understand how software components can work together to solve a practical problem. I learned that an AI-assisted application does not necessarily need to rely on a generative model; structured knowledge retrieval and a rule-driven workflow can also provide useful functionality.

The project also reinforced the importance of testing, human oversight, and designing features around the actual needs of the user.

---

PawPal+ demonstrates how Python application development, scheduling algorithms, structured knowledge retrieval, rule-driven agent workflows, and human approval can be combined into a practical pet-care application.
