import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    from wildfire_analysis.data.preparation import load_historical_state_month
    from wildfire_analysis.paths import DWD_DIR
    from wildfire_analysis.visualization.comparisons import (
        build_future_timeline_figure,
        build_year_comparison_figure,
    )
    from wildfire_analysis.visualization.historical import (
        build_monthly_seasonality_figure,
        build_yearly_trend_figure,
    )
    from wildfire_analysis.visualization.relationships import (
        build_relationship_figure,
        correlation_table,
    )

    return (
        DWD_DIR,
        build_future_timeline_figure,
        build_monthly_seasonality_figure,
        build_relationship_figure,
        build_year_comparison_figure,
        build_yearly_trend_figure,
        correlation_table,
        load_historical_state_month,
        mo,
        pd,
    )


@app.cell
def _(mo):
    mo.md("""
    # Wildfires and weather in Brandenburg

    This report combines monthly BMEL wildfire records with DWD weather
    observations. Weather stations are aggregated to one state-level row per
    month before analysis. Future projections use climate-grid monthly means
    and models validated in chronological order.

    Associations shown below do not establish that weather alone caused the
    observed fires. Predictions are exploratory and should not be interpreted
    as an operational fire-risk forecast.
    """)
    return


@app.cell
def _(DWD_DIR, load_historical_state_month, pd):
    historical_data = load_historical_state_month()
    future_predictions = pd.read_csv(DWD_DIR / "final_predictions.csv")
    future_predictions = future_predictions.drop(
        columns=[column for column in future_predictions if column.startswith("Unnamed")]
    )
    return future_predictions, historical_data


@app.cell
def _(future_predictions, historical_data, mo):
    target_control = mo.ui.dropdown(
        options={"Number of fires": "nFires", "Burned area": "area"},
        value="Number of fires",
        label="Historical measure",
    )
    feature_control = mo.ui.dropdown(
        options={
            "Precipitation": "pr",
            "Wind speed": "sfcWind",
            "Maximum temperature": "tasmax",
        },
        value="Precipitation",
        label="Weather variable",
    )
    historical_year_control = mo.ui.dropdown(
        options=historical_data["Year"].astype(int).unique().tolist(),
        value=int(historical_data["Year"].max()),
        label="Historical year",
    )
    future_year_control = mo.ui.dropdown(
        options=future_predictions["Year"].astype(int).unique().tolist(),
        value=int(future_predictions["Year"].min()),
        label="Future year",
    )
    mo.hstack(
        [
            target_control,
            feature_control,
            historical_year_control,
            future_year_control,
        ],
        justify="space-between",
    )
    return (
        feature_control,
        future_year_control,
        historical_year_control,
        target_control,
    )


@app.cell
def _(
    build_monthly_seasonality_figure,
    build_yearly_trend_figure,
    historical_data,
    mo,
    target_control,
):
    mo.md("## Historical patterns")
    historical_figures = mo.hstack(
        [
            mo.ui.plotly(
                build_yearly_trend_figure(historical_data, target_control.value)
            ),
            mo.ui.plotly(
                build_monthly_seasonality_figure(
                    historical_data, target_control.value
                )
            ),
        ]
    )
    historical_figures
    return


@app.cell
def _(
    build_relationship_figure,
    correlation_table,
    feature_control,
    historical_data,
    mo,
    target_control,
):
    mo.md("## Weather relationships")
    relationship_figure = mo.ui.plotly(
        build_relationship_figure(
            historical_data, feature_control.value, target_control.value
        )
    )
    mo.vstack([relationship_figure, correlation_table(historical_data)])
    return


@app.cell
def _(
    build_year_comparison_figure,
    future_predictions,
    future_year_control,
    historical_data,
    historical_year_control,
    mo,
):
    mo.md("## Observed and projected months")
    mo.ui.plotly(
        build_year_comparison_figure(
            historical_data,
            future_predictions,
            historical_year_control.value,
            future_year_control.value,
        )
    )
    return


@app.cell
def _(build_future_timeline_figure, future_predictions, mo):
    mo.md("## Future projections")
    mo.ui.plotly(build_future_timeline_figure(future_predictions))
    return


if __name__ == "__main__":
    app.run()
