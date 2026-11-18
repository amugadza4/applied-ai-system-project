# PawPal+ Project Reflection

## 1. System Design

PawPal+ began as a pet-care scheduling application built around four main classes: Owner, Pet, Task, and Scheduler.

The Owner class represents the person using the application and manages their pets. The Pet class stores information about each pet and its tasks. The Task class represents individual pet-care activities, including their descriptions, scheduled times, frequencies, and completion status. The Scheduler organizes tasks, sorts them, filters them, and detects scheduling conflicts.

As the project developed, I expanded the original scheduling application by adding a retrieval-based pet-care assistant, a rule-driven agent, safety checks, and interaction logging.

## 2. Scheduling Logic and Trade-offs

The scheduler prioritizes organizing tasks by their scheduled times. It also supports task completion, recurring tasks, filtering, and conflict detection.

One trade-off is that conflict detection currently uses exact scheduled-time matches instead of considering task durations. This keeps the implementation simple, but it means the system cannot identify every possible scheduling overlap.

Another limitation is that recurring tasks do not use a date-based scheduling system. Instead, completing a Daily or Weekly task creates a new incomplete task.

## 3. AI-Assisted Functionality

The AI-assisted portion of PawPal+ uses a curated JSON knowledge base and keyword-based retrieval.

The agent coordinates the process by checking requests for certain safety-related keywords, retrieving relevant information, organizing recommendations, checking for conflicts, and waiting for owner approval.

I chose this approach because it allowed me to build an AI-assisted workflow without depending on an external language model or API. It also made the retrieval and decision-making process easier to test.

## 4. Testing and Verification

I used Pytest to verify the core application, knowledge retrieval, agent workflow, safety checks, and interaction logging.

The latest verified test run completed with 35 passing tests.

I also tested the Streamlit application manually. I verified that normal pet-care questions could retrieve information and display sources, that recommendations could be reviewed, and that approved recommendations were added to the schedule.

I tested diagnosis-related and emergency-related requests separately to confirm that the appropriate warnings appeared.

## 5. What Went Well

The part of this project I am most satisfied with is how it developed from a basic class design into a working application with scheduling and AI-assisted functionality.

I was able to connect the Owner, Pet, Task, and Scheduler classes to the Streamlit interface and expand the application without replacing its original purpose.

I am also satisfied that I implemented automated tests and used them to verify the behavior of the different components.

## 6. What I Would Improve

If I had another iteration, I would improve the scheduling system by adding dates, task durations, and priorities. This would allow PawPal+ to create more realistic schedules and identify conflicts beyond tasks with matching start times.

I would also improve the knowledge retrieval system so that it could better understand different ways of asking the same question. Additional knowledge sources and more comprehensive safety testing would also improve the application.

For the interface, I would like to add more options for editing and deleting tasks and managing scheduling preferences.

## 7. Key Takeaway

One important thing I learned is that building a working application involves more than writing code. I needed to consider how the classes, methods, tests, AI components, and user interface connected to each other.

I also learned to use AI as a development tool. I needed to understand the suggestions, evaluate whether they fit the project, and test the results.

PawPal+ helped me develop a better understanding of application architecture, debugging, testing, and the importance of human oversight when building AI-assisted systems.