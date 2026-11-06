# Business Analytics Project — Idea 2: "Reviews into drivers"

**Research question.** To what extent can AI-extracted aspect-level sentiment explain variation in customer ratings, and which product attributes are most strongly associated with these ratings?

**Unit of analysis.** Primary: the individual review — the association between aspect-level sentiment expressed in a review and the rating (Score) given in that same review. Product-level aggregation may be used later as a secondary robustness check; it does not replace the main analysis.

**Theory.** A rating is a summary judgment formed from evaluations of multiple distinct product attributes (multi-attribute attitude framework). The attributes themselves, and their relative salience, are treated as an empirical rather than assumed question: candidate attributes are first explored in review text, then frozen into a fixed codebook of ~6–10 categories **before** any statistical examination of their relationship with ratings. No attribute is assumed ex ante to matter more than another; claims of relative importance must be grounded in the data or in literature.

**Hypotheses.**

- **H1 — Overall association:** AI-extracted aspect-level sentiment is jointly associated with customer ratings. Test the joint null that all aspect-sentiment coefficients equal zero using an appropriate joint F-test (or Wald test). Report model fit and examine coefficient signs separately. A significant joint association with consistent coefficient signs supports H1; changes in model fit relative to an intercept-only baseline summarize "to what extent."

- **H2 — Heterogeneity across attributes:** The strength of the association between aspect-level sentiment and ratings differs across product attributes. Test equality of comparable coefficients using appropriate linear contrasts and joint tests.

- **(Exploratory, optional — H3 candidate).** Positive and negative sentiment about a given attribute may show asymmetric associations with ratings. This hypothesis will be formalized **before** results are examined if pursued; it is not part of the confirmatory set above.

**Main analysis.** A multiple regression including all selected aspect-sentiment variables simultaneously. **OLS** is the primary, interpretable starting point: rating (Score) regressed on all aspect-sentiment variables, so that each attribute-level association is estimated conditional on the others. **Ordinal (proportional-odds) regression** is a pre-planned robustness check, reflecting that Score is a 5-point ordinal outcome. Note that OLS and ordinal-regression coefficients are on different scales (OLS reports a linear rating-point change; ordinal regression reports a change in the log-odds of higher rating categories), so the two specifications are compared in terms of direction, significance, and relative magnitude across attributes — never of raw coefficient size.

**Falsification / non-support criteria (pre-committed).**

- **H1 is not supported if** the joint null (all aspect-sentiment coefficients = 0) cannot be rejected by the pre-specified joint test, or if the coefficients carry signs systematically opposite to prediction (positive sentiment associated with lower ratings, negative sentiment with higher ratings). Failure here does not establish that the theory is false; it means the evidence in these data is insufficient to support it.
- **H2:** rejecting the joint equality restrictions (the linear contrasts across attributes) supports H2. Failure to reject provides **insufficient evidence of heterogeneity**, not proof of equivalence, and will be reported as such. Cases where an aspect provides too few labeled observations to estimate a comparable coefficient are treated as a **measurement or estimation limitation**, not as evidence about heterogeneity.
- Any **exploratory** analysis (including the asymmetry idea) is labeled as such in outputs and cannot be promoted to confirmatory status after results are seen.

**Data-quality facts found so far (observed, nothing deleted).**

- One CSV, `data/raw/Reviews.csv`: 568,454 reviews; columns `Id, ProductId, UserId, ProfileName, HelpfulnessNumerator, HelpfulnessDenominator, Score, Time, Summary, Text`; no missing values in `Text` or `Score`.
- Score distribution (1/2/3/4/5 = 52,268 / 29,769 / 42,640 / 80,655 / 363,122; mean 4.183, median 5). Rating skew is an observed fact; its implications for explanatory power are treated as an empirical outcome, not assumed.
- 1,185 rows share identical (UserId, ProductId, Score, Time, Text); 7,650 rows share a (ProductId, UserId) pair with differing text/time.
- 20+ reviews carry identical "tea bags…got pregnant" text across different ProductIds; all 27 rows with missing `Summary` trace to this cluster.
- 2 rows (Ids 44737, 64422) violate the rule `HelpfulnessNumerator > HelpfulnessDenominator`.

**Privacy.** Review text may embed personal information (names, addresses, health information, etc.). Text sent to any hosted AI model must be screened/redacted for such information first; verification and human labeling run locally.

**Human validation (course requirement).** 200 items are manually labeled by the analyst **before** any AI-generated labels are seen. Agreement between human and AI labels is then computed and reported; disagreements are documented, not silently corrected.

**Pipeline outline (kept high level; decisions deferred).** Load → data-quality audit and approved cleaning rules → sampling strategy → AI aspect/sentiment labeling with Score hidden → feature construction → OLS main regression (ordinal robustness check) → robustness checks (including product-level secondary) → interpretation under confirmatory/exploratory labels.

**Open items for later sessions.** Cleaning-rule details; sampling plan for the ~568k reviews; AI-labeling budget/technology; the exact set of coefficients compared in H2.
