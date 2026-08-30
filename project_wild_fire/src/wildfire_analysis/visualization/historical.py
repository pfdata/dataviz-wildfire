import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


TARGET_LABELS = {
    "nFires": "Number of fires",
    "area": "Burned area (ha)",
    "nr_predictions": "Predicted fires",
    "area_predictions": "Predicted burned area (ha)",
}


def yearly_summary(frame: pd.DataFrame) -> pd.DataFrame:
    targets = [column for column in ("nFires", "area") if column in frame]
    return frame.groupby("Year", as_index=False)[targets].sum()


def monthly_summary(frame: pd.DataFrame) -> pd.DataFrame:
    targets = [column for column in ("nFires", "area") if column in frame]
    return frame.groupby("Month", as_index=False)[targets].mean()


def build_yearly_trend_figure(frame: pd.DataFrame, target: str) -> Figure:
    summary = yearly_summary(frame)
    return px.line(
        summary,
        x="Year",
        y=target,
        markers=True,
        labels={target: TARGET_LABELS.get(target, target)},
        title=f"Yearly {TARGET_LABELS.get(target, target).lower()}",
        template="plotly_white",
    )


def build_monthly_seasonality_figure(frame: pd.DataFrame, target: str) -> Figure:
    summary = monthly_summary(frame)
    return px.bar(
        summary,
        x="Month",
        y=target,
        labels={target: TARGET_LABELS.get(target, target)},
        title=f"Average monthly {TARGET_LABELS.get(target, target).lower()}",
        template="plotly_white",
    )
