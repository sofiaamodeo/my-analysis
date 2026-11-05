# plan.md — my-analysis

## Research Question

Which product attributes are most strongly associated with customer satisfaction in Amazon food reviews?

## Theory

I expect that positive comments about taste and product quality are associated with higher customer ratings, while negative comments about price and packaging are associated with lower ratings.

> Note: this is a hypothesis about *association*, not causation. The data are observational
> (customers chose which products to buy and which reviews to write), so no causal claims
> will be made unless a design element explicitly supports them.

## Test

I will use AI to classify reviews according to the product attributes mentioned
(taste, quality, price, and packaging) and the sentiment expressed toward each attribute
(positive, negative, or neutral).

I will then compare the average star ratings across these categories to examine whether
the observed relationships support my hypotheses.

## Data

- Source: `data/raw/Reviews.csv` (~287 MB, Amazon Fine Food Reviews).
- Read-only. Never modified (rule 1). Any cleaned data goes to `data/derived/`.
- Columns used: `Id`, `ProductId`, `UserId`, `Score` (1–5), `Time`, `Summary`, `Text`.

## Steps

1. **Load & verify.** Load CSV with a real CSV parser; confirm the row count
   accounts for newlines inside quoted review text. Print rows loaded + reason.
2. **Deduplicate.** Same user + same product + same text = duplicate. Drop them.
   Print number of rows removed + reason (rule 2).
3. **Sample.** Classifying all 568k reviews is expensive → use a random sample
   of n = 2,000 (fixed seed 42, rule 5).
4. **Classify.** For each sampled review, ask the model which attributes are mentioned
   (taste / quality / price / packaging) and the sentiment toward each
   (positive / negative / neutral). Log prompt, model name, and raw output for
   every call to `results/` (rule 5). Classifier model: GLM-5.3-Flash Free
   (this session's model).
5. **Compare.** For each attribute × sentiment cell, compute the mean star rating,
   95% CI, and n. Write table to `results/attribute_sentiment_ratings.csv` via
   `src/my_analysis/<script>.py` (rule 3).
6. **Write-up.** Every number in the report cites its `results/` file and script (rule 3).

## Analysis choices (decision log)

- **A. Satisfaction metric** = `Score` (1–5 stars), used as-is (not binarized),
  because "satisfied at ≥4" would discard information; mean + CI is more informative.
- **B. Multi-attribute reviews** = allowed. A review can appear in several
  attribute rows (e.g., taste + price). Sentiment is judged *per attribute*,
  not per review.
- **C. Sample size** = n = 2,000, fixed seed 42. I am not sure n = 2,000 is
  enough for rare cells (e.g., negative packaging); the plan includes checking
  empty/rare cells before drawing conclusions.
- **D. Neutral sentiment** = included as a category but expected to be rare;
  reported for completeness.
- **E. Missing/short reviews** = reviews with empty `Text` are dropped;
  classified from `Text` primarily, `Summary` only as fallback context.

## Caveats

- Reviews mentioning *nothing* in {taste, quality, price, packaging} are excluded
  from the comparison; the excluded share will be reported.
- Reviews mentioning an attribute negatively are a self-selected group of
  (often annoyed) customers, so a lower average score in a cell partly reflects
  selection, not only the attribute. Claimed as association only.
