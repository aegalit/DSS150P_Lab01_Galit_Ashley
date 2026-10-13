import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
EVIDENCE = ROOT / "data" / "evidence"
REPORT_PATH = EVIDENCE / "profile_report.txt"

READERS = {
    "customers.csv": lambda path: pd.read_csv(path),
    "orders.json": lambda path: pd.read_json(path, convert_dates=False),
    "products.parquet": lambda path: pd.read_parquet(path),
}
DATE_HINTS = ("date", "time", "_at")


def is_nested(value):
    return isinstance(value, (dict, list))


def nested_columns(df):
    return [column for column in df.columns if df[column].map(is_nested).any()]


def to_hashable(df):
    out = df.copy()
    for column in nested_columns(df):
        out[column] = out[column].map(
            lambda value: json.dumps(value, sort_keys=True) if is_nested(value) else value
        )
    return out


def profile(name, df):
    path = RAW / name
    size = path.stat().st_size
    safe = to_hashable(df)
    nested = nested_columns(df)
    numeric = df.select_dtypes(include="number").columns

    lines = [f"=== {name} ==="]
    lines.append(f"file size: {size} bytes ({size / 1024:.1f} KB)")
    lines.append(f"rows: {df.shape[0]}")
    lines.append(f"columns: {df.shape[1]}")
    lines.append(f"column names: {list(df.columns)}")

    lines.append("inferred data types:")
    for column in df.columns:
        lines.append(f"  {column}: {df[column].dtype}")

    lines.append("missing values per column:")
    for column in df.columns:
        lines.append(f"  {column}: {int(df[column].isna().sum())}")

    lines.append(f"fully duplicated rows: {int(safe.duplicated().sum())}")

    lines.append("distinct values per column:")
    for column in safe.columns:
        lines.append(f"  {column}: {int(safe[column].nunique(dropna=True))}")

    nested_text = ", ".join(nested) if nested else "none"
    lines.append(f"nested columns (dict or list values): {nested_text}")

    lines.append("numeric min and max:")
    if len(numeric) == 0:
        lines.append("  none")
    for column in numeric:
        lines.append(f"  {column}: min={df[column].min()}, max={df[column].max()}")

    lines.append("date/time-like columns:")
    found = False
    for column in df.columns:
        if column in nested or column in numeric:
            continue
        if not any(hint in column.lower() for hint in DATE_HINTS):
            continue
        parsed = pd.to_datetime(df[column], errors="coerce", format="mixed")
        present = int(df[column].notna().sum())
        valid = int(parsed.notna().sum())
        if present == 0 or valid / present < 0.9:
            continue
        found = True
        lines.append(
            f"  {column}: earliest={parsed.min()}, latest={parsed.max()}, unparseable={present - valid}"
        )
    if not found:
        lines.append("  none")

    lines.append("first five records:")
    lines.append(df.head(5).to_string())
    lines.append("")
    return lines


def main():
    report = []
    for name, reader in READERS.items():
        path = RAW / name
        if not path.exists():
            print(f"Missing file: {path}")
            sys.exit(1)
        report.extend(profile(name, reader(path)))
    text = "\n".join(report)
    print(text)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")
    print(f"report saved to {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()