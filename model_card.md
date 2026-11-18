# PawPal+ Model Card and Responsible AI Reflection

## 1. System Overview

**Project:** PawPal+
**System Type:** Retrieval-based, rule-driven pet-care assistant
**Primary Technologies:** Python, Streamlit, JSON, Pytest

PawPal+ is an AI-assisted pet-care scheduling application that helps owners organize their pets' care routines and retrieve relevant pet-care information.

The assistant uses a curated JSON knowledge base, keyword matching, relevance scoring, and a rule-driven agent workflow. It does not use a generative language model or an externally hosted AI model.

## 2. Intended Purpose

PawPal+ is intended to:

- Help pet owners organize everyday care responsibilities.
- Retrieve relevant information from a curated pet-care knowledge base.
- Present informational care recommendations.
- Identify potential scheduling conflicts.
- Keep owners involved in decisions about their pets' schedules.

The system is designed to support organization and general information retrieval, not replace professional veterinary care.

## 3. Intended Users and Use Cases

**Intended users:** Pet owners who want help organizing routine pet-care activities.

**Intended use cases:**
- Asking general questions about pet exercise, feeding, enrichment, and routine care.
- Reviewing retrieved pet-care information.
- Considering suggested care tasks.
- Adding approved recommendations to a pet's schedule.

**Out-of-scope uses:**
- Diagnosing medical conditions.
- Recommending treatment for an illness or injury.
- Replacing a veterinarian's judgment.
- Making emergency medical decisions.
- Guaranteeing that retrieved information is appropriate for every individual animal.

## 4. How the System Works

The application follows a rule-driven workflow:

1. The owner selects a pet and submits a question.
2. The agent checks the request for emergency and diagnosis-related keywords.
3. The retrieval component searches the JSON knowledge base.
4. Relevant information is ranked using keyword-based relevance scoring.
5. The agent organizes retrieved information into recommendations.
6. The system checks for potential scheduling conflicts.
7. The owner reviews and approves or rejects recommendations.
8. Interactions are recorded in a local JSON Lines log.

The system uses deterministic rules and retrieval rather than generating answers with a large language model.

## 5. Data and Knowledge Sources

The application uses a manually curated JSON knowledge base.

Topics include:
- Dog exercise.
- Feeding routines.
- Veterinary checkups.
- Cat litter box maintenance.
- Cat enrichment and play.
- Veterinary emergencies.

The knowledge records include topic information, content, source names, and source URLs.

The quality of the assistant's responses depends on the accuracy, relevance, and coverage of the information in this knowledge base.

## 6. Human Oversight

Human approval is an important part of PawPal+.

The assistant does not automatically add every recommendation to a pet's schedule. Instead, the owner can review recommendations and decide which ones should become scheduled tasks.

This design keeps the owner responsible for decisions about their pet's routine and reduces the risk of treating an automated recommendation as an instruction that must be followed.

## 7. Responsible AI and Safety Measures

PawPal+ includes several basic safeguards:

### Emergency-related requests

The agent checks for predefined emergency-related keywords. When a potential emergency is identified, the application displays a warning directing the owner to contact an emergency veterinarian immediately.

### Diagnosis-related requests

The agent checks for predefined medical diagnosis keywords. These requests receive a message explaining that PawPal+ cannot diagnose medical conditions and that a licensed veterinarian should be contacted.

### Unsupported questions

When the retrieval system cannot find relevant information, it communicates that no relevant information was found rather than presenting unrelated knowledge as a reliable answer.

### Recommendation approval

Owners must review and approve recommendations before they are added to the schedule.

### Interaction logging

The system records interaction details locally to support review and debugging. Logs are excluded from version control.

## 8. System Limitations and Potential Risks

PawPal+ has important limitations:

- **Keyword-based retrieval:** The system does not understand language the way a human or advanced language model does. Different wording may produce incomplete or less relevant results.
- **Limited knowledge coverage:** The assistant can only retrieve information included in its curated knowledge base.
- **Basic safety checks:** Emergency and diagnosis detection relies on predefined keywords and cannot recognize every possible medical concern.
- **No veterinary diagnosis:** The application cannot determine whether an animal has a medical condition.
- **No personalized medical assessment:** Recommendations are not based on a complete veterinary history or examination.
- **Scheduling limitations:** Conflict detection checks matching scheduled times rather than task durations or overlapping time ranges.
- **No generative language model:** The system uses retrieval and predefined rules, so its responses are limited by its existing knowledge and implementation.

Users should consult a licensed veterinarian for medical concerns and seek emergency veterinary care when an animal may be experiencing an emergency.

## 9. Testing and Evaluation

The application was evaluated through automated tests and manual interaction with the Streamlit interface.

The automated tests cover:

- Pet and task management.
- Chronological scheduling.
- Recurring tasks.
- Scheduling conflict detection.
- Knowledge retrieval.
- Agent care-plan creation.
- Recommendation approval and rejection.
- Emergency and diagnosis safeguards.
- Interaction logging.

**Latest verified result: 35 automated tests passed.**

Manual testing also confirmed that:
- A normal pet-care question retrieves relevant information and displays sources.
- Recommendations can be reviewed and approved.
- Approved recommendations are added to the schedule.
- Diagnosis-related requests display a veterinary disclaimer.
- Emergency-related requests display an urgent warning.

Passing tests demonstrate that the implemented behaviors work for the tested scenarios. They do not establish that the system is medically accurate or that every possible safety issue will be detected.

## 10. Responsible AI Reflection

### How I Collaborated with AI

I used ChatGPT throughout development as a programming and problem-solving assistant. It helped me brainstorm implementation approaches, write and improve Python code, debug errors, connect the backend to Streamlit, and create automated tests.

I worked through the application one feature at a time, reviewing the suggested code and testing it before moving forward. This helped me understand how the components connected instead of relying on code that I could not explain.

### One AI Suggestion I Accepted

I accepted the suggestion to include basic safety checks for emergency-related and medical diagnosis requests.

I implemented keyword-based checks so the application could display warnings and direct users to veterinary professionals instead of continuing with a normal care plan. I also tested these behaviors to confirm that the warnings appeared separately and that the application did not present a normal recommendation workflow for those requests.

### One AI Suggestion I Rejected or Revised

One suggestion I did not adopt was expanding recurring tasks into a date-based system that would create a specific occurrence for the following day.

My original `Task` class did not include a date attribute. Adding date-based scheduling would have required changing the existing class structure and expanding the project beyond the design I had established.

Instead, I kept recurring-task behavior focused on creating a new incomplete task for Daily and Weekly tasks when the current task is completed. I verified this behavior through automated tests.

### What I Learned

This project taught me that AI-generated code should not automatically be accepted just because it appears to work. Suggestions need to be evaluated against the project's architecture, requirements, and intended behavior.

I also learned that responsible AI development involves more than implementing a useful feature. It requires considering limitations, testing how the system behaves, keeping people involved in important decisions, and being transparent about what the system can and cannot do.

## 11. Future Improvements

Future development could include:

- More advanced language understanding.
- Improved retrieval accuracy and relevance ranking.
- Expanded and more specific veterinary information sources.
- More comprehensive safety evaluation.
- Date-based scheduling and task-duration support.
- More detailed personalization while protecting user and pet information.
