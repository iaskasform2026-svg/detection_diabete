from __future__ import annotations

from pathlib import Path
import json
import pandas as pd

BASELINE_PATH = Path("monitoring/reference_dataset.csv")
CURRENT_PATH = Path("monitoring/current_dataset.csv")
OUTPUT_PATH = Path("monitoring/report.json")
TARGET_COL = "diabetes_risk"
NUMERIC_COLS = [
    "age", "bmi", "glucose_level", "hba1c", "blood_pressure",
    "cholesterol", "triglycerides", "retinopathy_score"
]


def population_stability_index(expected: pd.Series, actual: pd.Series, bins: int = 10) -> float:
    expected = expected.dropna()
    actual = actual.dropna()
    breaks = pd.qcut(expected.rank(method="first"), q=bins, duplicates="drop", retbins=True)[1]
    expected_bins = pd.cut(expected.rank(method="first"), bins=breaks, include_lowest=True)
    actual_bins = pd.cut(actual.rank(method="first"), bins=breaks, include_lowest=True)
    expected_dist = expected_bins.value_counts(normalize=True).sort_index().replace(0, 0.0001)
    actual_dist = actual_bins.value_counts(normalize=True).sort_index().replace(0, 0.0001)
    psi = ((actual_dist - expected_dist) * (actual_dist / expected_dist).apply(lambda x: pd.np.log(x))).sum()
    return float(round(psi, 4))


def compute_report() -> dict:
    baseline = pd.read_csv(BASELINE_PATH)
    current = pd.read_csv(CURRENT_PATH)

    report = {
        "baseline_rows": int(len(baseline)),
        "current_rows": int(len(current)),
        "target_rate_baseline": round(float(baseline[TARGET_COL].mean()), 4) if TARGET_COL in baseline else None,
        "target_rate_current": round(float(current[TARGET_COL].mean()), 4) if TARGET_COL in current else None,
        "drift": {},
    }

    for col in NUMERIC_COLS:
        if col in baseline.columns and col in current.columns:
            report["drift"][col] = {
                "mean_baseline": round(float(baseline[col].mean()), 4),
                "mean_current": round(float(current[col].mean()), 4),
                "psi": population_stability_index(baseline[col], current[col]),
            }

    return report


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = compute_report()
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Monitoring report generated: {OUTPUT_PATH}")
