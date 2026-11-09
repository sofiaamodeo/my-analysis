# Prompt

Review and update the project setup according to the instructions below.
Implement these changes in Build mode.

CURRENT STAGE

We are preparing the first exploratory data report.
Do not perform data cleaning, hypothesis testing, predictive modelling,
or train/validation/test splitting in this task.

1. PRIVACY AND DATA ACCESS

The hosted model must never see original patient or encounter identifiers.

- Do not read, preview, search, or expose the contents of data/raw/.
- Do not access files containing identifiers or patient mappings.
- The agent may analyse only verified identifier-free exports.
- You may inspect source code that references raw-file paths.
- You may write local preprocessing scripts, but do not execute scripts
  that access the original dataset. I will run them myself.
- Never include identifier values or replacement patient identifiers
  in reports, logs, tool outputs, or error messages.

2. CORRECT THE IDENTIFIER-REMOVAL PROCEDURE

Review src/drop_identifiers.py.

Create a corrected, clearly named version that I can run locally.
Preserve the previous version.

The corrected script must:
- Leave data/raw/ unchanged.
- Remove only encounter_id and patient_nbr.
- Preserve all remaining cell values, including literal "None", "?",
  empty fields, category labels, and diagnosis codes.
- Avoid automatic missing-value and numeric-type conversions.
- Preserve encounter order.
- Verify that the output contains exactly the expected retained columns,
  the same number of encounters, and identical retained cell values.
- Validate the saved output, not only the in-memory dataframe.
- Save a new identifier-free export without silently overwriting an
  existing file.
- Produce an aggregate validation report with clear PASS/FAIL checks.
- Never print individual rows or identifiers.

Do not claim that the existing derived dataset is corrupted:
its fidelity has not yet been checked.

3. LOCAL PATIENT-LEVEL CHECKS

Prepare a separate script for me to run locally that reports:
- Number of distinct patients with a valid patient identifier.
- Number of patients with multiple encounters.
- Distribution of encounters per patient.
- Missing patient and encounter identifier counts.
- Repeated encounter-ID counts.
- Fully duplicated records, distinguished from repeated patients.

State the counting definitions and denominators explicitly.
Do not treat missing patient identifiers as one patient.

Output aggregate results only. Do not export identifier values or mappings.
Do not remove records or create dataset partitions.

4. ALIGN PROJECT INSTRUCTIONS

Update AGENTS.md to state:
- The privacy and access boundaries above.
- The current stage is descriptive exploration.
- Read data/README.md before analysing the dataset.
- Meaningful categories must not automatically become missing values.
- Identical rows in an identifier-free dataset are not necessarily
  duplicate encounters and must not be removed automatically.
- Every numerical claim must be traceable to an output and its script.

Preserve other existing rules unless they conflict with these decisions.
Flag unresolved conflicts rather than silently rewriting them.

Update plan.md to:
- Preserve the existing business question, theory, and falsifying result.
- Separate current EDA from later inference and predictive modelling.
- Explain that patient-level checks require local processing that keeps
  identifiers outside the model context.
- Retain patient-grouped validation and clustered inference only as
  future requirements needing an agreed local procedure.
- Do not replace them with encounter-level random splitting or assume
  encounters are independent.
- State that removing direct identifiers alone does not establish
  complete anonymity.

5. AUDITOR

Update .opencode/agents/auditor.md to:
- Prohibit access to raw data and files containing identifiers.
- Review only authorised identifier-free data, aggregate local-check
  outputs, scripts, tables, figures, and reports.
- Distinguish confirmed discrepancies, suspected problems, and limitations.
- State clearly what was inspected versus independently recomputed.
- Never claim full reproduction without actually reproducing results.
- Keep the auditor read-only and check configuration compatibility
  against the installed OpenCode version where possible.

The auditor reports findings in the conversation.
mistakes.md is maintained exclusively by me.
No agent may create, edit, overwrite, or append to it.

Apply this mistakes.md rule consistently in AGENTS.md, plan.md,
and the auditor instructions.

6. DATA DICTIONARY

Create or update data/README.md with only a table containing:
- Every column in the identifier-free dataset.
- What each column means.
- Its units.

Use exactly these headers:
Column | Meaning | Units

Include every medication column individually.
Use "Not applicable" for variables without units.
Use "Not documented" when the meaning or units cannot be verified.
Use available authorised documentation; do not guess or access data/raw/.

Add a reference to data/README.md in AGENTS.md so the agent reads it
before analysing the dataset.

Ensure .gitignore allows data/README.md to be tracked while keeping
datasets excluded.

Do not modify the root README.md in this task.

7. VERIFICATION AND STOP CONDITION

Check script syntax without running scripts against real data.
Use small synthetic data to verify:
- Preservation of literal values, empty fields, and diagnosis codes.
- Correct removal of the two identifier columns.
- Preservation of row count and order.
- Absence of identifier values in exported data and captured script output.
- Correct aggregate patient-level checks.

Do not alter existing calls or historical outputs.
Follow the existing logging instructions for this task, clearly
distinguishing code written from code actually executed.

Finish with:
- Files changed and why.
- Checks actually completed.
- Missing documentation and unresolved questions.
- Exact commands I must run locally.
- Aggregate output files I can safely share afterwards.

Do not execute EDA or cleaning, access the original dataset, run the
auditor, or modify mistakes.md.

Stop after completing the setup changes and synthetic-data checks.
