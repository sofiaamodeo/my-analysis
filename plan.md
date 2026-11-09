# Project plan: Auditable Analysis of Diabetes Readmissions

## Question
Are prior inpatient visits associated with recorded readmission in less than
30 days, and can discharge-time information help rank encounters for further review?

## Theory
Prior inpatient use may capture persistent illness and continuing care needs.
I therefore expect encounters with number_inpatient >= 1 to have a higher
recorded '<30' rate than encounters with number_inpatient = 0.
This explanation is a hypothesis; an association would not establish causality.

## Current stage (set 2026-11-09)

The current stage is descriptive exploration (EDA) only. No data cleaning,
hypothesis testing, predictive modelling, or train/validation/test splitting
is performed yet. Later inference and predictive-modelling stages are
described below and require Sofia explicitly opening them.

Patient-level checks (distinct patients, encounters per patient, repeated
identifiers) require local processing that keeps identifiers outside the
agent's model context: the hosted agent prepares the scripts, Sofia runs them
locally, and only aggregate outputs are shared back.

Removing direct identifiers alone does not establish complete anonymity;
datasets like this can still be re-identified when age, race, and gender
remain. Treat the identifier-free export as reduced-circulation working data,
not as fully anonymous data.

## Data and unit
Use the supplied diabetes hospital encounters CSV and its documentation.
The primary unit is an encounter. Preserve patient grouping for uncertainty
estimation and train/test splitting; this is retained as a future requirement
that needs an agreed local procedure, because patient identifiers must stay
outside the hosted agent's context. Encounters are not treated as independent
and encounter-level random splitting is not an acceptable substitute.
Do not use IDs as model predictors.
Record the actual filename, dimensions, and documentation after inspection.

## Outcome and cohort
Positive: readmitted = '<30'. Negative: readmitted = '>30' or 'NO'.
Missing or unexpected target values require an explicit, logged decision.
Before the main analysis, use discharge-code documentation to agree on a
cohort policy for deaths, hospice, and transfers. Record all exclusions and
counts. Keep raw-file descriptive checks separate from this analysis cohort.

## Primary test
Compare the '<30' proportion between number_inpatient >= 1 and = 0.
Primary effect: rate in the first group minus rate in the second group,
reported in percentage points with a 95% patient-clustered confidence interval.
A bootstrap, if used, must resample patients with all their encounters.
Document missing or invalid number_inpatient values before creating groups.

## What would prove my theory wrong?
A zero or negative observed risk difference would contradict the predicted
direction in this sample. A confidence interval entirely below zero would
provide stronger evidence against the directional theory.
An interval spanning zero is inconclusive; it does not prove equality.
A positive difference alone would not prove the proposed mechanism or show
that prior inpatient use is sufficient for useful prediction.

## Secondary analysis
Explore age, length of stay, prior emergency visits, and medication changes.
Label these analyses exploratory and report all comparisons attempted.
Do not search repeatedly for a significant result and present it as planned.

## Later prediction stage
Decision time: discharge. Audit feature availability at that time.
Start with a prevalence baseline and logistic regression.
Use patient-disjoint training, validation, and test partitions with fixed seeds.
Fit all preprocessing on training data and select thresholds using validation
data only. Evaluate the locked model once on the untouched test set.
Report average precision, calibration, and precision and recall among the
highest-risk 10% of test encounters, with the selection/tie rule documented.
The 10% capacity is an illustrative assumption. Report the test prevalence.
Add complexity only if the simpler model leaves a clear question unresolved.

## Agent evaluation
Preserve prompts, model/version, outputs, and analysis decisions.
Run the main analysis once step by step and once in a fresh autonomous run
under the same agreed specification. Compare choices and results.
Use a fresh critic session to audit the scripts and conclusions.
An auditor's criticism is a claim to verify, not proof of an error.
mistakes.md is maintained exclusively by Sofia; no agent may create, edit,
overwrite, or append to it. Suspected errors are reported in the conversation;
Sofia records confirmed mistakes there herself, with how they were detected,
corrections, and remaining limitations. Do not invent mistakes to fill the log.

## Verification
Manually check three claims from the first report using the original CSV:
encounter row count, raw '<30' proportion, and raw weight-missing proportion.
Later, independently recompute the primary two-group risk difference in a
spreadsheet, without relying on the agent's summary table or generated code.
Record formulas, counts, cohort rules, evidence, and discrepancies.

## Outputs and boundaries
Keep data/raw/ unchanged. Put derived data in data/derived/, scripts in src/,
and computed tables and figures in results/.
Trace every final numerical claim to its results file and producing script.
Log row counts and reasons after every filter, merge, or drop.
This is a retrospective educational analysis. The data cannot establish that
a proposed review process prevents readmissions or produces financial savings.