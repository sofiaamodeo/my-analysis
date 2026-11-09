"""Synthetic-data checks for the two local data-preparation scripts.

Executed by the agent on synthetic data ONLY: none of the checks below reads
data/raw/ or any identifier-bearing real file. The script generates a small
synthetic dataset in a temporary directory, runs the real code paths of
- src/create_identifier_free_export.py  and
- src/patient_level_checks.py
and verifies the required properties. All data used here is synthetic.

Checks covered (per the 2026-11-09 setup instructions):
- preservation of literal values ("None", "?"), empty fields, and diagnosis codes
- correct removal of ONLY encounter_id and patient_nbr
- preservation of row count and encounter order
- absence of identifier values in exported data and captured script output
- correct aggregate patient-level checks

The script does not print individual data rows or identifier values; its own
output is scanned to verify that the fake synthetic identifiers never leak
into printed output.
"""

from __future__ import annotations

import csv
import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from create_identifier_free_export import create_identifier_free_export, validate_saved_output  # noqa: E402
from patient_level_checks import build_patient_level_report  # noqa: E402

REPORT_PATH = Path("results/local_checks/synthetic_data_check_report.txt")

HEADER = [
    "encounter_id", "patient_nbr", "race", "gender", "age", "weight",
    "admission_type_id", "discharge_disposition_id", "admission_source_id",
    "time_in_hospital", "payer_code", "medical_specialty", "num_lab_procedures",
    "num_procedures", "num_medications", "number_outpatient", "number_emergency",
    "number_inpatient", "diag_1", "diag_2", "diag_3", "number_diagnoses",
    "max_glu_serum", "A1Cresult", "change", "diabetesMed", "readmitted",
]

# Synthetic rows. Cells include: literal "?", literal "None", empty cells,
# a comma inside a quoted field ("Internal, Medicine"), ICD-like codes.
# Rows 3 and 4 share the same encounter_id and patient_nbr (repetition case).
# Row 5 has an empty patient_nbr; row 6 has an empty encounter_id.
# time_in_hospital doubles as an ORDER MARKER (values 3, 4, 5, 2, 1, 11).
ROWS = [
    ["900000100", "700000101", "Caucasian", "Female", "[10-20)", "?", "1", "1", "7", "3", "MC", "Internal, Medicine", "41", "0", "1", "0", "0", "0", "250.83", "V45", "250.83", "1", "None", "None", "No", "No", "NO"],
    ["900000108", "700000109", "African American", "Male", "[30-40)", "?", "2", "1", "5", "4", "?", "Miami", "0", "0", "0", "1", "1", "0", "V45", "?", "", "3", "None", "None", "Ch", "Yes", ">30"],
    ["900000110", "700000111", "?", "Unknown/Invalid", "[70-80)", "?", "1", "1", "7", "5", "PP", "?", "73", "1", "15", "0", "0", "1", "V45", "250.83", "?", "9", "None", "None", "No", "No", "NO"],
    ["900000110", "700000111", "Hispanic", "Male", "[80-90)", "?", "2", "6", "6", "2", "CP", "?", "8", "0", "2", "1", "0", "0", "", "", "", "3", "None", "None", "Ch", "Yes", ">30"],
    ["900000115", "", "Caucasian", "Female", "[40-50)", "?", "3", "1", "3", "1", "PX", "Surgery-Cardiovascular", "5", "5", "31", "0", "0", "0", "820", "?", "?", "9", "None", "None", "No", "No", "NO"],
    ["", "700000116", "Caucasian", "Male", "[70-80)", "?", "1", "1", "7", "11", "SP", "?", "8", "0", "14", "0", "1", "0", "437", "254", "437", "5", "None", "None", "No", "No", "NO"],
]

FAKE_IDS = {row[0] for row in ROWS if row[0]} | {row[1] for row in ROWS if row[1]}


def write_synthetic_csv(path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADER)
        writer.writerows(ROWS)


def run_all_checks() -> tuple[list[tuple[str, bool, str]], str]:
    checks: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory(prefix="synthetic_privacy_") as tmp:
        tmp_dir = Path(tmp)
        raw_path = tmp_dir / "synthetic.csv"
        write_synthetic_csv(raw_path)

        # ---- Export: basic properties --------------------------------------
        out1 = tmp_dir / "export.csv"
        export_df, retained = create_identifier_free_export(raw_path, out1)

        checks.append((
            "A1. Only encounter_id/patient_nbr removed (columns and order kept)",
            list(export_df.columns) == [c for c in HEADER if c not in ("encounter_id", "patient_nbr")],
            f"{len(export_df.columns)} columns retained",
        ))
        checks.append((
            "A2. Row count preserved",
            len(export_df) == len(ROWS),
            f"{len(export_df)} rows",
        ))
        checks.append((
            "A3. Encounter order preserved (time_in_hospital sequence kept)",
            export_df["time_in_hospital"].tolist() == [row[9] for row in ROWS],
            "order matched",
        ))
        checks.append((
            "A4. Literal '?', literal 'None', empty cells, comma field, ICD codes preserved",
            (
                export_df["weight"].tolist()[:4] == ["?", "?", "?", "?"]
                and export_df["max_glu_serum"].tolist() == ["None"] * len(ROWS)
                and export_df["diag_1"].tolist()[3] == ""
                and export_df["diag_2"].tolist()[1] == "?"
                and export_df["medical_specialty"].tolist()[0] == "Internal, Medicine"
                and export_df["diag_1"].tolist()[0] == "250.83"
                and export_df["diag_1"].tolist()[4] == "820"
            ),
            "special/empty/quoted cells identical",
        ))
        checks.append((
            "A5. No identifier values leak into the saved export",
            not any(fake_id in out1.read_text(encoding="utf-8") for fake_id in FAKE_IDS),
            "0 fake IDs found in the exported file text",
        ))
        self_report = validate_saved_output(export_df, retained, raw_path, out1)
        script_pass_lines = [line for line in self_report.splitlines() if "- [" in line]
        checks.append((
            "A6. Script's own saved-output validation is all PASS",
            len(script_pass_lines) == 4 and all("[PASS]" in line for line in script_pass_lines),
            f"{len(script_pass_lines)}/4 script self-checks PASS",
        ))

        # No-overwrite behaviour: run the export again into an existing path.
        create_identifier_free_export(raw_path, out1)
        written = list(tmp_dir.glob("export*.csv"))
        checks.append((
            "A7. Export never silently overwrites an existing file",
            len(written) == 2,
            "second run produced a separate timestamped file",
        ))

        # ---- Patient-level checks ------------------------------------------
        captured = io.StringIO()
        with redirect_stdout(captured):
            report_text, agg = build_patient_level_report(raw_path)

        # Expected aggregates on the synthetic file:
        # valid patients: 700000101(1), 700000109(1), 700000111(2), 700000116(1)
        expected = {
            "total_rows": len(ROWS),
            "missing_encounter_rows": 1,
            "missing_patient_rows": 1,
            "distinct_valid_patients": 4,
            "patients_multiple_encounters": 1,
            "repeated_encounter_ids": 1,
            "rows_sharing_repeated_id": 2,
            "rows_fully_duplicated": 0,
            "full_dup_groups": 0,
        }
        for name, expected_value in expected.items():
            checks.append((
                f"B1. Patient-level aggregate correct: {name} == {expected_value}",
                agg[name] == expected_value,
                f"got {agg[name]}",
            ))

        checks.append((
            "B2. Encounter-per-patient distribution correct",
            agg["feature_counts"] == "{1: 3, 2: 1}",
            f"got {agg['feature_counts']}",
        ))

        # ---- No identifiers in captured stdout of the checked scripts ------
        printed = captured.getvalue()
        checks.append((
            "C1. No identifier values appear in captured script output",
            not any(fake_id in printed for fake_id in FAKE_IDS),
            "0 fake IDs found in captured stdout",
        ))

        all_pass = all(ok for _, ok, _ in checks)
        summary = [
            "Synthetic-data check report (no real data accessed)",
            "Executed with a synthetic temporary CSV generated inside this run",
            "",
        ]
        for name, ok, detail in checks:
            summary.append(f"- [{'PASS' if ok else 'FAIL'}] {name} ({detail})")
        summary.append("")
        summary.append(
            f"ALL SYNTHETIC CHECKS {'PASSED' if all_pass else 'FAILED'}: "
            f"{sum(ok for _, ok, _ in checks)}/{len(checks)} checks passed."
        )
        report = "\n".join(summary) + "\n"
        return checks, report


if __name__ == "__main__":
    checks, report = run_all_checks()
    print(report)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report, encoding="utf-8")
    if not all(ok for _, ok, _ in checks):
        raise SystemExit(2)
