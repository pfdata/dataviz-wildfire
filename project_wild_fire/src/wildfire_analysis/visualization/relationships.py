import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


FEATURE_LABELS = {
    "pr": "Monthly precipitation (mm)",
    "sfcWind": "Wind speed (m/s)",
    "tasmax": "Maximum air temperature (K)",
}


def correlation_table(frame: pd.DataFrame) -> pd.DataFrame:
    columns = [
        column
        for column in ("pr", "sfcWind", "tasmax", "nFires", "area")
        if column in frame
    ]
    return frame[columns].corr(numeric_only=True).round(3)


def build_relationship_figure(
    frame: pd.DataFrame, feature: str, target: str
) -> Figure:
    return px.scatter(
        frame,
        x=feature,
        y=target,
        color="Month",
        trendline="ols",
        labels={feature: FEATURE_LABELS.get(feature, feature)},
        title=f"{target} in relation to {FEATURE_LABELS.get(feature, feature).lower()}",
        template="plotly_white",
    )
