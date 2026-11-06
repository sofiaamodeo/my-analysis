# AGENTS.md — Business Analytics project: my-analysis

Read `plan.md` first. Never change it without asking Sofia.

## Data and privacy

1. Never modify or write to `data/raw/`. Everything you make goes in `data/derived/`.
2. Before reading anything else, drop `ProfileName` and replace `UserId` with a hash. Work only from that cleaned copy.
3. Text sent to a hosted model must be screened for personal information first. Use only the models allowed in the course brief.
4. Never commit or push `data/`, human-labeled files, or `.env`. Check `.gitignore` before every commit.

## Method

5. Do not change the research question, hypotheses, unit of analysis or methods in `plan.md` without Sofia's approval. Label every output "confirmatory" or "exploratory"; exploratory results never become confirmatory.
6. Cleaning rules need approval before they are applied. After every filter, merge or drop, print rows before → after → removed, and the reason.
7. Fix random seeds. List every analysis choice made, including ones Sofia did not ask about.
8. No causal claims unless the design supports them. Say "I am not sure" when not sure.

9. Label every statement as an observation, an assumption or a recommendation.
10. After each data report, list three claims that can be checked by hand, and how.

## AI labeling

11. Never show `Score` to a model that labels text. Labels come from `Text` only; `Summary` is not model input in the main pass.
12. The codebook is frozen and dated before any analysis of its relation with `Score`. Later changes need approval, logged with date and reason.
13. The 200 human-labeled items are chosen reproducibly, stored apart from AI output, and labeled from `Text` only. Never open AI labels for them until Sofia says the labeling is done.

## Traceability

14. Every number in a write-up comes from a file in `results/`; name the script that made it. Each table or figure comes from one script in `src/`, numbered in run order.
15. For every model call and every output produced, log: date, model name and version, exact prompt, input row ids, raw output.

## Mistakes and version control

16. Record errors, changed decisions and abandoned approaches in `mistakes.md`: what happened, when, impact, fix. No silent backtracking.
17. Commit approved changes to code and text files with a message saying what and why; push only when Sofia asks.
