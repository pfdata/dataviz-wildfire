import pandas as pd
import plotly.graph_objects as go


def build_year_comparison_figure(
    historical: pd.DataFrame,
    predictions: pd.DataFrame,
    historical_year: int,
    future_year: int,
) -> go.Figure:
    history = historical.loc[historical["Year"] == historical_year]
    future = predictions.loc[predictions["Year"] == future_year]
    if history.empty:
        raise ValueError(f"No historical data for {historical_year}")
    if future.empty:
        raise ValueError(f"No predictions for {future_year}")

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=history["Month"],
            y=history["nFires"],
            mode="markers+lines",
            marker={"size": history["area"].clip(lower=0).pow(0.5) * 3 + 6},
            name=f"Observed {historical_year}",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=future["Month"],
            y=future["nr_predictions"],
            mode="markers+lines",
            marker={
                "size": future["area_predictions"].clip(lower=0).pow(0.5) * 3 + 6
            },
            name=f"Predicted {future_year}",
        )
    )
    figure.update_layout(
        title="Monthly wildfire comparison",
        xaxis_title="Month",
        yaxis_title="Number of fires",
        template="plotly_white",
    )
    return figure


def build_future_timeline_figure(predictions: pd.DataFrame) -> go.Figure:
    frame = predictions.copy()
    frame["Date"] = pd.to_datetime(
        {"year": frame["Year"], "month": frame["Month"], "day": 1}
    )
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=frame["Date"],
            y=frame["nr_predictions"],
            name="Number of fires",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=frame["Date"],
            y=frame["area_predictions"],
            name="Burned area",
            yaxis="y2",
        )
    )
    figure.update_layout(
        title="Future monthly wildfire projections",
        yaxis={"title": "Number of fires"},
        yaxis2={"title": "Burned area (ha)", "overlaying": "y", "side": "right"},
        template="plotly_white",
    )
    return figure
