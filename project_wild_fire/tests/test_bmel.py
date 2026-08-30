from pathlib import Path

import pandas as pd

from wildfire_analysis.data.bmel import load_monthly_fire_counts


def test_load_monthly_fire_counts(tmp_path: Path) -> None:
    year_dir = tmp_path / "2001"
    year_dir.mkdir()
    pd.DataFrame(
        {"Jan": [2], "Feb": [3]}, index=pd.Index(["Brandenburg"], name="Land")
    ).to_csv(year_dir / "5B.csv")

    result = load_monthly_fire_counts(tmp_path)

    assert result[["Land", "Year", "Month", "nFires"]].to_dict("records") == [
        {"Land": "Brandenburg", "Year": 2001, "Month": 1, "nFires": 2},
        {"Land": "Brandenburg", "Year": 2001, "Month": 2, "nFires": 3},
    ]
