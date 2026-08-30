from collections.abc import Sequence
from pathlib import Path
import re

import pandas as pd

from wildfire_analysis.paths import BMEL_DIR


TABLES = {
    "1B": "forest fire areas by stand type",
    "2B": "causes",
    "5B": "monthly number of forest fires",
    "6B": "monthly burned area",
}

MONTHS = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "Mai": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Okt": 10,
    "Nov": 11,
    "Dez": 12,
}


def discover_tables(table_code: str, data_dir: Path = BMEL_DIR) -> list[Path]:
    if table_code not in TABLES:
        raise ValueError(f"Unknown BMEL table {table_code!r}; expected one of {sorted(TABLES)}")
    paths = sorted(data_dir.rglob(f"*{table_code}.csv"))
    if not paths:
        raise FileNotFoundError(f"No *{table_code}.csv files found under {data_dir}")
    return paths


def _year_from_path(path: Path) -> int:
    for part in reversed(path.parts):
        if re.fullmatch(r"(?:19|20)\d{2}", part):
            return int(part)
    raise ValueError(f"Cannot determine year from {path}")


def load_table(table_code: str, data_dir: Path = BMEL_DIR) -> pd.DataFrame:
    frames = []
    for path in discover_tables(table_code, data_dir):
        frame = pd.read_csv(path, index_col=0).reset_index()
        frame["Year"] = _year_from_path(path)
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def reshape_monthly(
    frame: pd.DataFrame,
    value_name: str,
    id_columns: Sequence[str] = ("Land", "Year"),
) -> pd.DataFrame:
    missing = set(id_columns).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing identifier columns: {sorted(missing)}")
    month_columns = [column for column in MONTHS if column in frame.columns]
    if not month_columns:
        raise ValueError("No German month columns found in BMEL data")
    monthly = frame.melt(
        id_vars=list(id_columns),
        value_vars=month_columns,
        var_name="Month",
        value_name=value_name,
    )
    monthly["Month"] = monthly["Month"].map(MONTHS).astype("int64")
    monthly["Year"] = monthly["Year"].astype("int64")
    return monthly.sort_values([*id_columns, "Month"]).reset_index(drop=True)


def load_monthly_fire_counts(data_dir: Path = BMEL_DIR) -> pd.DataFrame:
    return reshape_monthly(load_table("5B", data_dir), "nFires")


def load_monthly_burned_area(data_dir: Path = BMEL_DIR) -> pd.DataFrame:
    return reshape_monthly(load_table("6B", data_dir), "area")


def load_monthly_wildfires(data_dir: Path = BMEL_DIR) -> pd.DataFrame:
    return load_monthly_fire_counts(data_dir).merge(
        load_monthly_burned_area(data_dir),
        on=["Land", "Year", "Month"],
        how="outer",
        validate="one_to_one",
    )
