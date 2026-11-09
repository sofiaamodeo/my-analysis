# AGENTS.md — Business Analytics project: my-analysis

Starter rules (from the course project brief):

1. Never modify anything in `data/raw/`.
2. After every filter, merge or drop, print the number of rows and the reason.
3. Every number in a write-up comes from a file in `results/`; name the script that made it.
   Trace it to that output file and to its producing script.
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
7. The hosted model never reads or exposes patient or encounter identifiers.
   Identifier-removal scripts are written by the agent and executed locally by
   Sofia (see "Privacy and access boundaries" below). This rephrases the
   earlier wording "drop or replace names, emails, IDs, phone numbers columns
   before reading anything else" to make it compatible with those boundaries.

## Privacy and access boundaries (hosted model)

- The hosted model must never see original patient or encounter identifiers.
- Never read, preview, search, or expose the contents of `data/raw/`.
- Never access files containing identifiers or patient-level mappings.
- The agent may analyse only verified identifier-free exports.
- The agent may inspect source code that references raw-file paths.
- The agent may write local preprocessing scripts, but must not execute
  scripts that access the original dataset; Sofia runs those scripts herself.
- Never include identifier values or replacement patient identifiers in
  reports, logs, tool outputs, or error messages.

## mistakes.md

`mistakes.md` is maintained exclusively by Sofia. No agent may create, edit,
overwrite, or append to it. Suspected errors are reported in the conversation.

## Current stage and data-use rules

- Current stage: descriptive exploration (EDA). No data cleaning, no
  hypothesis testing, no predictive modelling, and no train/validation/test
  splitting is performed until Sofia explicitly opens the later stages
  described in `plan.md`.
- Read `data/README.md` before analysing the dataset.
- Meaningful categories must not automatically become missing values.
- Identical rows in an identifier-free dataset are not necessarily duplicate
  encounters and must not be removed automatically.
