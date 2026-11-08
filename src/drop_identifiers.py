"""Drop identification variables (encounter_id, patient_nbr) from the raw dataset.

Per AGENTS.md rule 7, identifier columns must be dropped before using the data.
Per AGENTS.md rule 2, we print row counts after each drop, with the reason.

Output: data/derived/diabetic_data_no_ids.csv
Rule 6: no causal claims are made in this script; it is purely a data operation.
"""

from pathlib import Path

import pandas as pd

RAW = Path("data/raw/diabetic_data.csv")
OUT = Path("data/derived")
TARGET = OUT / "diabetic_data_no_ids.csv"

ID_COLUMNS = ["encounter_id", "patient_nbr"]


def main() -> None:
    df = pd.read_csv(RAW)
    print(f"Loaded {len(df)} rows (all rows present in data/raw; nothing dropped yet).")

    missing_ids = [c for c in ID_COLUMNS if c not in df.columns]
    if missing_ids:
        print(f"WARNING: expected identifier columns not found: {missing_ids}")

    df_no_ids = df.drop(columns=ID_COLUMNS)
    print(
        f"Dropped identifier columns {ID_COLUMNS} and kept {len(df_no_ids)} rows "
        f"and {df_no_ids.shape[1]} columns. Reason: AGENTS.md rule 7 requires "
        "identifier columns to be dropped before any other use; the row count is "
        "unchanged because dropping columns does not discard encounters."
    )

    assert len(df_no_ids) == len(df), "Row count must not change when dropping columns."

    OUT.mkdir(parents=True, exist_ok=True)
    df_no_ids.to_csv(TARGET, index=False)
    print(f"Saved {len(df_no_ids)} rows to {TARGET}. data/raw/ remains unchanged.")


if __name__ == "__main__":
    main()
