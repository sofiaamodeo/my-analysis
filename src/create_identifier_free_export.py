"""Create a VERIFIED identifier-free export from the diabetes encounters dataset.

Written by the agent on 2026-11-09; meant to be RUN LOCALLY BY SOFIA.
The hosted model must never execute this script, because by default it reads
data/raw/diabetic_data.csv, which contains identifiers.

Correctness requirements (per the 2026-11-09 setup instructions):
- Leave data/raw/ unchanged (this script only reads the input once).
- Remove ONLY encounter_id and patient_nbr.
- Preserve all remaining cell values exactly, including literal "None", "?",
  empty fields, category labels and diagnosis codes: the file is read with
  dtype=str, keep_default_na=False, na_filter=False, so pandas performs no
  missing-value detection and no numeric conversion.
- Preserve encounter order (no sorting, no reindexing).
- Verify the SAVED output (not only the in-memory frame): re-read it and
  compare columns, row count and every retained cell value cell-by-cell.
- Save the export WITHOUT silently overwriting an existing file (a timestamp
  suffix is added if the target path already exists).
- Produce an aggregate PASS/FAIL validation report; never print individual
  rows or identifier values.

The script is importable so that synthetic-data checks (src/synthetic_data_checks.py)
can run the same code paths without touching data raw/.
Rule 2 of AGENTS.md: row counts are printed after the only transformation here
(column drop), with the reason.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data/raw/diabetic_data.csv")
OUT_DIR = Path("data/derived")
BASE_NAME = "diabetic_data_no_ids_verified.csv"
REPORT_PATH = Path("results/local_checks/identifier_free_export_validation.txt")

ID_COLUMNS = ["encounter_id", "patient_nbr"]

READ_KWARGS = dict(dtype=str, keep_default_na=False, na_filter=False)


def _non_overwriting_path(base: Path) -> Path:
    """Return base, or base with a timestamp suffix if base already exists."""
    if base.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return base.with_name(f"{base.stem}_{stamp}{base.suffix}")
    return base


def create_identifier_free_export(input_csv: Path, output_csv: Path) -> tuple[pd.DataFrame, list[str]]:
    """Load the input, drop the two identifier columns, and save the export.

    Checks are aggregated; no individual rows are printed. Identifier columns
    are removed from the frame used for output, and no identifier VALUES are
    printed at any point.
    """
    df = pd.read_csv(input_csv, **READ_KWARGS)
    print(f"Loaded input file. Rows: {len(df)}. Columns: {df.shape[1]}.")

    missing_ids = [c for c in ID_COLUMNS if c not in df.columns]
    if missing_ids:
        raise SystemExit(f"FAIL: input is missing expected identifier column(s) named: {missing_ids}")

    extra_check = [c for c in df.columns if c not in ID_COLUMNS]
    retained_columns = list(extra_check)

    # The only transformation: drop the two identifier columns.
    export_df = df.drop(columns=ID_COLUMNS)
    assert list(export_df.columns) == retained_columns, (
        "FAIL: retained-column order changed while dropping identifiers."
    )
    print(
        f"Dropped exactly the identifier columns {ID_COLUMNS} (reason: privacy "
        f"boundary); rows unchanged: {len(export_df)}; retained columns: "
        f"{len(retained_columns)}."
    )

    output_csv = _non_overwriting_path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    export_df.to_csv(output_csv, index=False)
    print(f"Saved export without overwriting any existing file: {output_csv.name}.")
    return export_df, retained_columns


def validate_saved_output(
    export_df: pd.DataFrame, retained_columns: list[str], input_path: Path, output_path: Path
) -> str:
    """Re-read the saved export and verify it cell-by-cell. Returns the report text."""
    raw_df = pd.read_csv(input_path, **READ_KWARGS)
    rb = pd.read_csv(output_path, **READ_KWARGS)

    # Non-blank identifiers only: the empty string is not an identifier value
    # (missing identifiers legitimately coincide with empty exported cells).
    identifier_values = set(
        value for value in raw_df[ID_COLUMNS[0]].tolist() + raw_df[ID_COLUMNS[1]].tolist()
        if value.strip() != ""
    )

    checks: list[tuple[str, bool]] = []
    checks.append(
        (
            f"1. Identifier columns removed: output header contains exactly {len(retained_columns)} "
            f"retained columns and none of {ID_COLUMNS}",
            list(rb.columns) == retained_columns
            and not set(rb.columns) & set(ID_COLUMNS),
        )
    )
    checks.append(
        (
            f"2. Row count preserved between raw file and export "
            f"(both {len(raw_df)})",
            len(rb) == len(raw_df) == len(export_df),
        )
    )
    checks.append(
        (
            "3. All retained cell values identical cell-by-cell, and encounter "
            "order preserved (row-by-row frame equality on string values)",
            rb.reset_index(drop=True).equals(export_df.reset_index(drop=True)),
        )
    )

    output_unique = set()
    for col in rb.columns:
        output_unique.update(pd.unique(rb[col]).tolist())
    leaked = identifier_values & output_unique
    checks.append(
        (
            f"4. No identifier VALUES leak into any saved cell "
            f"({len(leaked)} leaked value(s), 0 expected)",
            len(leaked) == 0,
        )
    )

    lines = [
        "Identifier-free export validation report",
        f"Input file: {input_path}",
        f"Output file: {output_path}",
        f"Rows (input): {len(raw_df)}",
        f"Rows (export): {len(rb)}",
        f"Columns (input): {raw_df.shape[1]}",
        f"Columns (export): {rb.shape[1]}",
        "Checks:",
    ]
    for name, ok in checks:
        lines.append(f"- [{'PASS' if ok else 'FAIL'}] {name}")
    all_pass = all(ok for _, ok in checks)
    lines.append(f"ALL CHECKS {'PASSED' if all_pass else 'FAILED'}")

    report_text = "\n".join(lines) + "\n"
    print(report_text)
    return report_text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a verified identifier-free export (run locally by Sofia)."
    )
    parser.add_argument("--input", type=Path, default=RAW_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()

    output_csv = args.out_dir / BASE_NAME
    export_df, retained_columns = create_identifier_free_export(args.input, output_csv)
    report = validate_saved_output(export_df, retained_columns, args.input, output_csv)

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(f"Validation report saved to: {args.report}")


if __name__ == "__main__":
    main()
