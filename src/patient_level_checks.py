"""Aggregate patient-level identifier checks for the diabetes encounters dataset.

Written by the agent on 2026-11-09; meant to be RUN LOCALLY BY SOFIA, because
by default it reads the identifier-bearing file data/raw/diabetic_data.csv.
The hosted model must never execute it.

What it reports (aggregates only; no identifier values are printed):
- Number of distinct VALID patient identifiers (rows with an empty/
  whitespace patient_nbr are excluded and reported separately; missing
  identifiers are NEVER counted as one patient).
- Number of patients with multiple encounters.
- Distribution of encounters per patient (counts and share of distinct
  valid patients).
- Rows with missing patient and encounter identifiers.
- Repeated encounter-ID counts (IDs assigned to more than one row, rows
  carrying those IDs, and surplus rows), reported as aggregates.
- Fully duplicated records across ALL columns, explicitly distinguished
  from legitimately repeated patients.

Counting definitions and denominators are printed explicitly in the report.
No rows are removed, no partitions are created, and no IDs or mappings are
exported.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data/raw/diabetic_data.csv")
REPORT_PATH = Path("results/local_checks/patient_level_checks.txt")

ID_COLUMNS = ["encounter_id", "patient_nbr"]

READ_KWARGS = dict(dtype=str, keep_default_na=False, na_filter=False)


def _is_missing(cell: str) -> bool:
    """Definition: an identifier value is missing when it is empty or only
    whitespace. (No other token is assumed to mean 'missing' here.)"""
    return cell.strip() == ""


def build_patient_level_report(input_csv: Path) -> tuple[str, dict[str, float]]:
    df = pd.read_csv(input_csv, **READ_KWARGS)
    n_rows = len(df)
    n_enc_missing = int(df[ID_COLUMNS[0]].map(_is_missing).sum())
    n_pat_missing = int(df[ID_COLUMNS[1]].map(_is_missing).sum())

    valid = df[~df[ID_COLUMNS[1]].map(_is_missing)]
    n_distinct_patients = int(valid[ID_COLUMNS[1]].nunique())

    enc_per_patient = valid.groupby(ID_COLUMNS[1]).size()
    n_patients_multi = int((enc_per_patient >= 2).sum())

    distribution = (
        enc_per_patient.value_counts().sort_index().to_dict()
    )  # encounters -> patients

    valid2 = df[
        ~df[ID_COLUMNS[0]].map(_is_missing) & ~df[ID_COLUMNS[1]].map(_is_missing)
    ]
    id_counts = valid2.groupby(ID_COLUMNS[0]).size()
    n_repeated_encounter_ids = int((id_counts > 1).sum())
    n_rows_sharing_repeated_id = int(id_counts[id_counts > 1].sum())
    n_surplus_rows = n_rows_sharing_repeated_id - n_repeated_encounter_ids

    full_dup_mask = df.duplicated(keep=False)
    n_rows_fully_duplicated = int(full_dup_mask.sum())
    n_full_dup_groups = int(df[full_dup_mask].groupby(list(df.columns)).ngroups)

    denominators = {
        "distinct_valid_patients": n_distinct_patients,
        "encounters_with_valid_ids": len(valid2),
        "total_rows": n_rows,
    }

    lines = [
        "Patient-level identifier checks (aggregate only)",
        f"Input file: {input_csv.name}",
        f"Denominator - total encounter rows: {n_rows}",
        "",
        "Definitions:",
        "- A patient identifier is VALID when its cell is not empty/only whitespace; "
        "rows with empty or whitespace identifiers are excluded from patient counts "
        "and reported separately. Missing identifiers are never treated as one patient.",
        "- Flexible: no other token is interpreted as 'missing'.",
        "",
        "Results:",
        f"- Encounter rows total: {n_rows}",
        f"- Rows with MISSING encounter_id: {n_enc_missing}",
        f"- Rows with MISSING patient_nbr: {n_pat_missing}",
        f"- Distinct valid patients: {n_distinct_patients} "
        f"(denominator: patients with a valid patient_nbr)",
        f"- Patients with MULTIPLE encounters: {n_patients_multi} "
        f"(denominator: distinct valid patients) = "
        f"{n_patients_multi / n_distinct_patients:.4%} of patients",
        f"- Distribution of encounters per patient (encounters: patients, "
        f"share of distinct valid patients): "
        + "; ".join(
            f"{k}: {v} ({v / n_distinct_patients:.4%})" for k, v in distribution.items()
        ),
        "",
        "Encounter-ID repetition (denominator: encounters with both IDs valid):",
        f"- encounter_id values assigned to more than one row: "
        f"{n_repeated_encounter_ids}",
        f"- rows carrying a repeated encounter_id: {n_rows_sharing_repeated_id}",
        f"- surplus rows from repeated encounter_ids: {n_surplus_rows}",
        "",
        "Full-row duplication (denominator: all encounter rows;",
        "an identical row across ALL columns is required):",
        f"- rows that belong to fully duplicated groups: {n_rows_fully_duplicated}",
        f"- fully duplicated groups: {n_full_dup_groups}",
        "",
        (
            "Note: fully duplicated rows and repeated patients are different "
            "phenomena. A patient having several encounters can produce rows that "
            "differ legitimately in encounter-level fields only; such rows are NOT "
            "duplicates and must not be removed automatically (AGENTS.md)."
        ),
    ]

    aggregates = dict(denominators)
    aggregates.update(
        {
            "missing_encounter_rows": n_enc_missing,
            "missing_patient_rows": n_pat_missing,
            "patients_multiple_encounters": n_patients_multi,
            "repeated_encounter_ids": n_repeated_encounter_ids,
            "rows_sharing_repeated_id": n_rows_sharing_repeated_id,
            "rows_fully_duplicated": n_rows_fully_duplicated,
            "full_dup_groups": n_full_dup_groups,
            "feature_counts": str(distribution),
        }
    )
    report_text = "\n".join(lines) + "\n"
    return report_text, aggregates


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate patient-level checks (run locally by Sofia)."
    )
    parser.add_argument("--input", type=Path, default=RAW_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    report_text, _ = build_patient_level_report(args.input)
    print(report_text)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report_text, encoding="utf-8")
    print(f"Aggregate report saved to: {args.report}")


if __name__ == "__main__":
    main()
