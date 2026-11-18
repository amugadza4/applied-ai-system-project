# PawPal+ 🐾
## Pet Care Scheduling and AI-Assisted Planning Application

## 1. Project Overview

**Original project: PawPal+ (Module 3)**

The original Module 3 version of PawPal+ focused on helping pet owners organize their pets' care routines. Users could add pets, create care tasks, organize schedules, and track completed responsibilities.

This final project extends that system by introducing a retrieval-based pet-care assistant, a rule-driven agent workflow, safety guardrails, and interaction logging.

PawPal+ is a Python and Streamlit application that combines pet-care scheduling with structured knowledge retrieval. It helps owners access relevant pet-care information and turn recommendations into scheduled tasks while keeping the owner in control of decisions.

## 2. Features

### Pet Management
- Add pets to an owner's profile.
- Store pet names and species.
- Select a pet when creating tasks or requesting recommendations.

### Pet Care Scheduling
- Create care tasks for individual pets.
- Set task descriptions, times, and frequencies.
- Organize tasks chronologically.
- Mark tasks as completed.
- Support Daily, Weekly, and Once task frequencies.
- Identify scheduling conflicts.

### AI-Assisted Pet Care

PawPal+ uses a retrieval-based assistant and rule-driven agent workflow to process pet-care requests.

The assistant can:
- Retrieve relevant information from a curated pet-care knowledge base.
- Filter information based on the selected pet's species.
- Rank retrieved information using keyword relevance scoring.
- Organize retrieved information into care recommendations.
- Display supporting sources.
- Check recommendations against existing scheduled tasks.
- Present recommendations for owner review.

### Owner Approval Workflow
- Recommendations are presented for review rather than automatically added.
- Owners can approve individual recommendations.
- Approved recommendations become scheduled pet-care tasks.
- Owners can reject recommendations.
- The application checks for scheduling conflicts before adding tasks.

### Safety Guardrails
PawPal+ includes basic keyword-based safety checks:
- Emergency-related requests trigger a warning directing owners to contact an emergency veterinarian.
- Medical diagnosis requests are redirected to a licensed veterinarian.
- Requests without relevant knowledge-base information receive a response indicating that no relevant information was found.

PawPal+ is an informational and organizational tool. It does not diagnose medical conditions or replace professional veterinary advice.

### Interaction Logging
The application records AI assistant interactions in JSON Lines format.

Logged information includes:
- Timestamp
- Pet name and species
- User request
- Interaction outcome
- Retrieved knowledge topics

Logs are stored locally in `logs/ai_interactions.jsonl` and excluded from version control.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic, scheduling, and agent workflow |
| Streamlit | Interactive web application |
| JSON | Structured pet-care knowledge base |
| Pytest | Automated testing |
| Git and GitHub | Version control |

## 4. System Architecture

PawPal+ is organized into four main components:

1. **Core application (`pawpal_system.py`):** Defines the Owner, Pet, Task, and Scheduler classes and manages pet information and scheduling.
2. **AI components (`ai/`):** Handle knowledge retrieval, agent decisions, safety checks, recommendation approval, and interaction logging.
3. **Knowledge base (`knowledge_base/`):** Stores curated pet-care information in a structured JSON file.
4. **User interface (`app.py`):** Connects the core application and AI components through Streamlit.

The architecture diagram is maintained as Mermaid source in:

`diagrams/architecture.mmd`

The UML diagram is maintained in:

`diagrams/uml_final.mmd`

The architecture diagram represents the implemented workflow:

**User request → Safety checks → Knowledge retrieval → Recommendation generation → Conflict detection → Owner approval → Schedule update → Interaction logging**

## 5. How the AI Assistant Works

PawPal+ uses structured knowledge retrieval and a rule-driven agent workflow. It does not use a generative language model or external LLM API.

The workflow follows these steps:

1. **User Request:** The owner selects a pet and submits a pet-care question.
2. **Safety Checks:** The agent checks for emergency-related and medical diagnosis requests.
3. **Knowledge Retrieval:** The assistant searches the curated JSON knowledge base using keyword matching and relevance scoring.
4. **Species Filtering:** Retrieved information is filtered to match the selected pet's species where applicable.
5. **Recommendation Generation:** The agent organizes relevant information into care recommendations.
6. **Conflict Detection:** The system checks recommendations against the pet's existing scheduled tasks.
7. **Owner Review:** The owner reviews recommendations and chooses whether to approve or reject them.
8. **Schedule Update:** Approved recommendations are added to the pet's schedule.
9. **Interaction Logging:** The application records the interaction and its outcome.

This workflow demonstrates how retrieval, decision rules, safety checks, and human oversight can work together in an AI-assisted application.

## 6. Sample End-to-End Interactions

The following examples demonstrate the application's expected behavior. The normal care-plan example describes the workflow; the diagnosis and emergency examples show the application's safety response text.

### Example 1: Pet-care information request

**Input:**

```text
How much exercise does my dog need?
```

**Application behavior:**

1. The owner selects a dog in the application.
2. The assistant searches the pet-care knowledge base.
3. Relevant dog exercise information is retrieved.
4. The application displays the information and its source.
5. The assistant presents recommendations for owner review.

**Application response:**

```text
Care plan created for review.
```

**Owner action:**

The owner reviews the recommendations and approves one.

**Result:**

```text
Daily exercise has been added to Buddy's schedule.
```

The owner can also reject recommendations instead of adding them.

### Example 2: Medical diagnosis request

**Input:**

```text
What is wrong with my dog?
```

**Application output:**

```text
PawPal cannot diagnose medical conditions. A licensed veterinarian can examine your pet and provide an accurate diagnosis. Please contact your veterinarian about your concerns.
```

**Result:**

The diagnosis safety check prevents the application from generating a normal care plan for the request.

### Example 3: Potential veterinary emergency

**Input:**

```text
My dog is having trouble breathing.
```

**Application output:**

```text
This request may describe a veterinary emergency. Please contact an emergency veterinarian or go to the nearest emergency animal hospital immediately. Do not wait for an AI-generated care plan.
```

**Result:**

The emergency safety check displays an urgent warning instead of proceeding with the normal recommendation workflow.

## 7. Knowledge Base and Retrieval

The structured pet-care knowledge base is stored in:

`knowledge_base/pet_care.json`

It contains curated information covering topics such as:
- Dog exercise
- Dog feeding routines
- Veterinary checkups
- Cat feeding routines
- Cat litter box maintenance
- Cat play and mental stimulation
- Veterinary emergencies

The retrieval system uses keyword matching and relevance scoring to identify potentially relevant information.

The scoring approach gives greater weight to topic and category matches than general content matches. Retrieved information includes its topic, content, source, and source URL.

This approach provides a transparent and manageable starting point for retrieving relevant pet-care information.

## 8. Scheduling System

The core scheduling functionality is implemented in `pawpal_system.py`.

| Method | Responsibility |
|---|---|
| `Task.mark_complete()` | Marks a task as completed and handles recurring tasks |
| `Pet.add_task()` | Adds a task to a pet |
| `Pet.get_tasks()` | Retrieves a pet's tasks |
| `Scheduler.sort_by_time()` | Sorts tasks chronologically |
| `Scheduler.filter_tasks()` | Filters tasks by pet or completion status |
| `Scheduler.detect_conflicts()` | Identifies tasks scheduled at the same time |

**Design trade-off:** Conflict detection currently checks for matching scheduled times rather than overlapping task durations. This keeps the implementation simple because tasks do not currently have duration attributes.

## 9. Installation and Setup

### Requirements
- Python 3.12 or a compatible Python version
- pip
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/amugadza4/applied-ai-system-project.git
```

### Step 2: Navigate to the project directory

```bash
cd applied-ai-system-project
```

### Step 3: Create a virtual environment

```bash
python3 -m venv .venv
```

### Step 4: Activate the virtual environment

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

## 10. Running the Application

To launch the Streamlit application, run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL. Open that URL in your browser to use PawPal+.

The repository also includes a command-line entry point:

```bash
python3 main.py
```

## 11. Reliability and Testing

PawPal+ uses Pytest to test the core scheduling functionality, knowledge retrieval, agent workflow, safety checks, and interaction logging.

Run the complete test suite:

```bash
python -m pytest -v
```

Or use the shorter command:

```bash
python -m pytest -q
```

### Test Coverage

| Test file | Functionality tested |
|---|---|
| `tests/test_pawpal_system.py` | Pet management, task management, recurring tasks, sorting, and scheduling conflicts |
| `tests/test_ai_assistant.py` | Knowledge retrieval and handling unrelated requests |
| `tests/test_agent.py` | Care-plan creation, approval, rejection, safety checks, and logging |
| `tests/test_interaction_logger.py` | Log creation, interaction details, and multiple records |

**Previously verified test result:** 35 tests passed.

Run the test command above to verify the current version of the project.

### Reliability Mechanisms

The application includes several mechanisms to improve reliability:

- Input and pet selection checks in the application workflow.
- Keyword-based emergency and diagnosis safeguards.
- Relevance scoring during knowledge retrieval.
- Handling for requests without relevant knowledge-base results.
- Scheduling conflict detection.
- Owner approval before recommendations become scheduled tasks.
- Automated tests for core functionality and safety behavior.
- Interaction logs for reviewing assistant outcomes.

These mechanisms reduce the chance of irrelevant recommendations or unsafe scheduling decisions. However, they do not guarantee that every possible unsafe or inaccurate response will be detected.

## 12. Design Trade-offs and Limitations

PawPal+ was designed to provide a practical, understandable AI-assisted workflow without relying on an external language model.

The current implementation has several limitations:

- **Keyword-based retrieval:** The system may not understand every variation of a user's question.
- **Limited knowledge base:** Recommendations are restricted to the curated information available in the JSON file.
- **Keyword-based safety checks:** The safeguards cannot recognize every possible emergency or medical concern.
- **Scheduling limitations:** Conflict detection does not account for task duration or overlapping time ranges.
- **Limited personalization:** Recommendations do not account for every individual pet characteristic or medical history.
- **Local logging:** Interaction logs are stored locally and are not designed as a secure medical-record system.

Future improvements could include more advanced retrieval, expanded veterinary sources, date-based scheduling, duration-aware conflict detection, more detailed pet profiles, and broader safety evaluation.

## 13. AI Collaboration and Project Reflection

AI tools, including ChatGPT, were used during development to support planning, debugging, code review, testing, and documentation.

AI assistance helped identify potential improvements to the agent workflow and reliability safeguards. One suggestion that was accepted was adding emergency and diagnosis-related checks to prevent the assistant from treating potentially serious medical concerns as ordinary care-planning requests.

Another suggestion involving automatic date-based expansion of recurring tasks was revised rather than adopted because the existing scheduling model did not yet support the date and duration information needed to implement it reliably.

This project reinforced that AI-generated suggestions should be evaluated against the actual codebase and project requirements instead of being accepted automatically.

Building PawPal+ also demonstrated that an AI-assisted system does not necessarily need a generative model to provide useful functionality. Structured retrieval, rule-based decisions, safety checks, and human approval can work together to support a practical application.

For additional details, see:
- `model_card.md` — Responsible-AI considerations, intended use, limitations, and AI collaboration.
- `ai_interactions.md` — Development interactions and AI collaboration notes.
- `reflection.md` — Project development reflection.

## 14. Future Improvements

Potential future enhancements include:

- More advanced natural-language understanding.
- Improved knowledge retrieval and relevance ranking.
- Expanded pet-care knowledge sources.
- More detailed pet profiles and personalized recommendations.
- Date-based scheduling and task-duration support.
- More advanced scheduling conflict detection.
- Expanded safety checks and evaluation tests.
- Improved privacy protections for interaction logs.

---

**PawPal+ demonstrates how Python application development, structured knowledge retrieval, rule-driven agent workflows, scheduling functionality, reliability safeguards, and human approval can be combined into a practical pet-care application.**