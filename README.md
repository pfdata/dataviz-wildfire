# Wildfire Data Analysis and Visualization

This repository explores wildfire patterns in Germany, with a focus on Brandenburg. It combines historical wildfire statistics with weather observations to investigate how precipitation, wind speed, temperature, and other climate variables relate to the number of forest fires and the area burned.

The project uses wildfire records from the German Federal Ministry of Food and Agriculture (BMEL) and historical weather observations from the German Weather Service (DWD). The available BMEL records cover 1995-2022 and include monthly fire counts, burned areas, fire causes, and affected forest types. Future exploratory projections use regional climate-model data.

## What The Project Does

- Loads and reshapes annual BMEL wildfire tables.
- Retrieves and normalizes monthly DWD station observations.
- Aggregates weather to one state-level record per month.
- Evaluates regression models with chronological cross-validation.
- Produces nonnegative exploratory projections of fire counts and burned area.
- Presents historical patterns, weather relationships, and model diagnostics in Marimo notebooks.

Associations and projections in this repository are exploratory. They are not an operational wildfire-risk forecast and should not be interpreted as evidence that weather alone caused individual fires.

## Repository Structure

```text
project_wild_fire/
├── data/                    # Raw and derived BMEL, DWD, GIS, and climate data
├── notebooks/               # Marimo presentation and diagnostics applications
├── output/                  # Generated charts and analysis artifacts
├── scripts/                 # Data acquisition commands
├── src/wildfire_analysis/   # Reusable data, modeling, and visualization code
└── tests/                   # Automated tests
```

The notebooks contain presentation and reactive controls only. Reusable loading, transformation, modeling, and plotting functions are defined under `project_wild_fire/src/wildfire_analysis/`.

## Installation

Python 3.12 or newer is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[test]"
```

The same editable installation can be started with `python3 -m pip install -r requirements.txt`.

## Marimo Applications

Start the narrative wildfire report:

```bash
marimo edit project_wild_fire/notebooks/wildfire_story.py
```

Start the model diagnostics report:

```bash
marimo edit project_wild_fire/notebooks/model_diagnostics.py
```

Use `marimo run` instead of `marimo edit` to serve either notebook in read-only application mode.

## Model Workflow

Historical DWD station observations are averaged to one row for each state, year, and month before they are joined with BMEL targets. This prevents the same monthly wildfire target from being repeated as independent samples for multiple stations.

Models are evaluated with expanding-window temporal splits rather than random row splits. Preprocessing is encapsulated in fitted scikit-learn pipelines and reused for validation and future prediction. Predicted counts and areas are clipped at zero because negative wildfire activity is not meaningful.

Future precipitation is converted from flux to a monthly total using the actual number of days in each calendar month. Climate-grid values are then averaged to one state-month record before prediction.

## Data Acquisition

Existing BMEL PDFs are preserved by default. Download missing annual PDFs with:

```bash
python3 project_wild_fire/scripts/download_bmel_pdfs.py
```

Pass `--force` only when existing PDFs should be replaced.

## Tests

```bash
python3 -m pytest
```

## References

- [BMEL statistics](https://www.bmel-statistik.de/)
- [DWD Open Data](https://opendata.dwd.de/)
- [Wetterdienst DWD coverage](https://wetterdienst.readthedocs.io/en/latest/data/coverage/dwd/observation.html)
