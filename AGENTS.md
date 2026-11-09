# AGENTS.md — Business Analytics project: my-analysis

Starter rules (from the course project brief):

1. Never modify anything in `data/raw/`.
2. After every filter, merge or drop, print the number of rows and the reason.
3. Every number in a write-up comes from a file in `results/`; name the script that made it.
4. Follow `plan.md`. Ask before changing anything in it, and list every analysis choice you make.
5. Fix random seeds. Log in `calls/` every Build-mode turn that executes
   or defines analysis work (scripts, data preparation, reports).
   Do not log Plan-mode discussion, git pushes, or one-off clarifications.
   Log each qualifying turn BEFORE responding to the next request.
   Its structure should be
calls/
├── call_001_initial_exploration/
│   ├── prompt.md
│   ├── model.md
│   └── output.md
│
├── call_002_data_preparation/
│   ├── prompt.md
│   ├── model.md
│   └── output.md
│
├── call_003_descriptive_analysis/
│   ├── prompt.md
│   ├── model.md
│   └── output.md
6. No causal claims unless the design supports them. Say "I am not sure" when you are not.
7. Drop or replace names, emails, IDs, phone numbers columns before reading anything else.

