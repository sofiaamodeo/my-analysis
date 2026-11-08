# Prompt

Create a first exploratory data report for my Business Analytics project using the diabetes hospital encounters dataset in data/raw/.

Start in Plan mode: inspect the available files, explain your proposed checks. Do not create files, run analysis scripts, install packages, or switch modes yourself. Do not invent statistics that you cannot compute in Plan mode.

Keep this first report descriptive. Do not train predictive models or perform hypothesis tests.

Cover the following:

1. Dataset structure
- Identify the dataset file and the unit of observation.
- Report the number of rows and columns.
- Describe column types and distinguish identifiers, numerical variables, categorical variables, and the target.
- Check actual values rather than relying only on the data dictionary.

2. Missing values
- Identify how missing values are encoded, including "?", empty cells, and other documented tokens.
- Report missing counts and percentages for every column, sorted from highest to lowest.
- Distinguish a missing value from meaningful categories such as "test not performed."
- Flag unexpected categories or invalid values.
- Suggest possible handling strategies, but do not delete or impute anything.

3. Duplicates and repeated patients
- Count fully duplicated rows.
- Check whether encounter_id is unique and report missing identifiers.
- Count distinct patients using patient_nbr.
- Report how many patients have multiple encounters and show the distribution of encounters per patient.
- Explain why repeated encounters for the same patient are not automatically duplicates.
- Do not remove any rows or print individual identifier values.

4. Basic descriptive statistics
- For numerical variables, report nonmissing count, mean, standard deviation, median, quartiles, minimum, and maximum.
- For categorical variables, report category counts and percentages. Summarise high-cardinality variables clearly.
- Show the distribution of readmitted using its actual category labels.
- State whether each percentage refers to encounters or unique patients, and give its denominator.
- Flag unusual values without assuming they are errors.

5. Visualisations
Propose and, once Build mode is authorised, create these six plots:
- Missing-value percentage by column.
- Counts of the readmitted categories.
- Encounter counts by age group, ordered by age.
- Distribution of time_in_hospital.
- Distribution of number_inpatient.
- Distribution of encounters per patient.

Use readable titles, axis labels, and units. Distinguish zero from missing values. If you limit an axis or omit categories for readability, explain what was omitted.

6. Initial observations and limitations
- Summarise up to five observations supported by computed results.
- Distinguish verified findings from questions for further investigation.
- Do not make causal claims or clinical recommendations.
- List analytical choices and unresolved data-quality questions.

7. Three claims for me to verify by hand
Select:
- Total number of encounter rows.
- Number and percentage of encounters labelled "<30".
- Number and percentage of missing weight values, or another column if weight is absent.

For each claim, provide the exact value, numerator and denominator where relevant, missing-value rules, and an independent spreadsheet procedure I can follow.
Mark any uncomputed value as NOT YET COMPUTED.
Do not claim that I have completed these checks.

For now, present your inspection findings and proposed execution plan, then stop for my review.
