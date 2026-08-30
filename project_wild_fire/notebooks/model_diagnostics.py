import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    from wildfire_analysis.data.preparation import load_historical_state_month
    from wildfire_analysis.modeling.evaluation import (
        evaluate_regressors,
        summarize_evaluation,
    )
    from wildfire_analysis.visualization.relationships import correlation_table

    return (
        correlation_table,
        evaluate_regressors,
        load_historical_state_month,
        mo,
        summarize_evaluation,
    )


@app.cell
def _(mo):
    mo.md("""
    # Wildfire model diagnostics

    Models are evaluated with expanding-window temporal cross-validation.
    Each sample represents one state-month, preventing observations from the
    same month from appearing in both training and validation data.
    """)
    return


@app.cell
def _(load_historical_state_month):
    diagnostic_data = load_historical_state_month()
    return (diagnostic_data,)


@app.cell
def _(mo):
    diagnostic_target = mo.ui.dropdown(
        options={"Number of fires": "nFires", "Burned area": "area"},
        value="Number of fires",
        label="Prediction target",
    )
    fold_control = mo.ui.slider(3, 8, value=5, step=1, label="Temporal folds")
    mo.hstack([diagnostic_target, fold_control], justify="start")
    return diagnostic_target, fold_control


@app.cell
def _(correlation_table, diagnostic_data, mo):
    date_min = f"{int(diagnostic_data['Year'].min())}-{int(diagnostic_data['Month'].min()):02d}"
    date_max = f"{int(diagnostic_data['Year'].max())}-{int(diagnostic_data['Month'].max()):02d}"
    quality_summary = mo.md(
        f"""
        ## Dataset quality

        - **Period:** {date_min} to {date_max}
        - **State-month rows:** {len(diagnostic_data):,}
        - **Missing cells after preparation:** {int(diagnostic_data.isna().sum().sum())}
        """
    )
    mo.vstack([quality_summary, correlation_table(diagnostic_data)])
    return


@app.cell
def _(diagnostic_data, diagnostic_target, evaluate_regressors, fold_control):
    fold_scores = evaluate_regressors(
        diagnostic_data,
        ["pr", "sfcWind", "tasmax"],
        diagnostic_target.value,
        n_splits=fold_control.value,
    )
    return (fold_scores,)


@app.cell
def _(fold_scores, mo, summarize_evaluation):
    mo.md("## Model comparison")
    mo.ui.table(summarize_evaluation(fold_scores), selection=None)
    return


@app.cell
def _(fold_scores, mo):
    import plotly.express as px

    score_figure = px.line(
        fold_scores,
        x="Fold",
        y="MAE",
        color="Model",
        markers=True,
        title="Validation error through time",
        template="plotly_white",
    )
    mo.ui.plotly(score_figure)
    return


if __name__ == "__main__":
    app.run()
