# AGENTS.md — Business Analytics project: my-analysis

Starter rules (from the course project brief):

1. Never modify anything in `data/raw/`.
2. After every filter, merge or drop, print the number of rows and the reason.
3. Every number in a write-up comes from a file in `results/`; name the script that made it.
4. Follow `plan.md`. Ask before changing anything in it, and list every analysis choice you make.
5. Fix random seeds, and log the prompt, output and model name of every model call.
6. No causal claims unless the design supports them. Say "I am not sure" when you are not.

## Methodological governance

7. **Do not change the research question, hypotheses, unit of analysis, or statistical methodology defined in `plan.md` without explicit approval.** Clearly distinguish confirmatory analyses from exploratory analyses in all outputs. Exploratory findings may not be promoted to confirmatory status after results have been seen.

## Data integrity & privacy

8. `data/raw/` is read-only; no script may ever write to it.
9. Every filter, merge, or drop prints rows before → rows after → rows removed → one-line reason. Proposed cleaning rules are submitted for approval before being applied, never executed silently.
10. **Privacy:** review text can contain personally identifying information (names, locations, health details). Text sent to any hosted AI model must be screened/redacted for PII first. Human labeling and hand-verification are performed on local copies only.

## AI labeling hygiene

11. **The numerical `Score` is never exposed** to the AI model during aspect identification or sentiment classification; labels are built from review `Text` alone.
12. Review `Summary` is treated with care: it often pre-reveals the rating's direction and must not be used as model input in the main labeling pass if it would leak rating information.
13. **Attribute codebook freeze:** the codebook is fixed (and dated) before any statistical examination of its relationship with ratings. Afterwards, no change to codes, categories, or definitions without explicit approval, logged with date and rationale.
14. Every AI call is logged: date, model name and version, exact prompt, input row ids, and raw output.

## Human validation (course requirement)

15. **200 items must be manually labeled by the analyst before seeing any AI-generated labels.** The 200 items are selected in a logged, reproducible way and stored separately from AI outputs to avoid incidental exposure. Human–AI agreement is then computed and reported; disagreements are documented, not silently corrected.

## Verification & attribution

16. At least three factual claims about the data are independently hand-verified per session and recorded with date.
17. Every stated observation, recommendation, or assumption is explicitly labeled as such.

## Mistakes

18. Errors, changed decisions, and abandoned approaches are recorded in `mistakes.md` with what happened, when, impact, and fix — no silent backtracking.

## Version control

19. Every time a file is modified and the change is approved, the change is committed and pushed to the remote repository (`origin`) — not just saved locally. Commit messages state what changed and why.
