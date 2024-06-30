import wetter_api as wt
import waldbrand
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import common_paths
import logging

# Configure logging
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )


def fetch_and_process_weather_data(parameter, state):
    try:
        weather_data = wt.fetch_observation_data(parameter, state)
        weather_data["date"] = pd.to_datetime(weather_data["date"])
        weather_data["Year"] = weather_data["date"].dt.year
        weather_data["Month"] = weather_data["date"].dt.month
        weather_data.sort_values(by=["Month", "Year"], inplace=True)
        weather_data.drop(
            columns=["station_id", "dataset", "date", "quality", "parameter"],
            inplace=True,
        )
        weather_data["Year"] = weather_data["Year"].astype(int)
        weather_data["Month"] = weather_data["Month"].astype(int)
        parameter_column_name = f"{parameter}"
        weather_data.rename(columns={"value": parameter_column_name}, inplace=True)
        # weather_data = weather_data.groupby(["Year", "Month"]).mean().reset_index()
        return weather_data
    except Exception as e:
        logging.error(
            f"Error fetching or processing weather data for parameter {parameter}: {e}"
        )
        return pd.DataFrame()


def prepare_data(parameters, state):
    weather_data_list = [
        fetch_and_process_weather_data(param, state) for param in parameters
    ]
    combined_weather_data = weather_data_list[0]

    for additional_data in weather_data_list[1:]:
        combined_weather_data = pd.merge(
            combined_weather_data, additional_data, on=["Year", "Month"]
        )

    wildfire_obj = waldbrand.WildFire()
    wildfire_df = wildfire_obj.get_montly_numbers()
    state_wildfire_data = wildfire_df.loc[[state]]
    state_wildfire_data = wildfire_obj.melt_and_map_months(state_wildfire_data)
    state_wildfire_data["Year"] = state_wildfire_data["Year"].astype(int)
    state_wildfire_data["Month"] = state_wildfire_data["Month"].astype(int)
    merged_data = pd.merge(
        combined_weather_data, state_wildfire_data, on=["Year", "Month"]
    )

    weather_columns = combined_weather_data.columns.tolist()
    weather_columns.remove("Year")
    weather_columns.remove("Month")
    new_column_order = ["Year", "Month"] + weather_columns + ["nFires"]
    merged_data = merged_data[new_column_order]
    merged_data.dropna(inplace=True)
    return merged_data


def prepare_wildfire_data(state: str):
    wildfire_obj = waldbrand.WildFire()
    wildfire_df = wildfire_obj.get_montly_numbers()
    state_wildfire_data = wildfire_df.loc[[state]]
    state_wildfire_data = wildfire_obj.melt_and_map_months(state_wildfire_data)
    state_wildfire_data["Year"] = state_wildfire_data["Year"].astype(int)
    state_wildfire_data["Month"] = state_wildfire_data["Month"].astype(int)
    return state_wildfire_data


def prepare_weather_data(parameters, state):
    weather_data_list = [
        fetch_and_process_weather_data(param, state) for param in parameters
    ]
    combined_weather_data = weather_data_list[0]

    for additional_data in weather_data_list[1:]:
        combined_weather_data = pd.merge(
            combined_weather_data, additional_data, on=["Year", "Month"]
        )

    return weather_data_list


def evaluate_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(),
        "Decision Tree Regression": DecisionTreeRegressor(),
        "Random Forest Regression": RandomForestRegressor(),
        "Support Vector Regression": SVR(),
        "Gradient Boosting Regression": GradientBoostingRegressor(),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        results[name] = {"model": model, "mse": mse, "r2_score": r2}
        # logging.info(f"{name} - MSE: {mse}, R2: {r2}")

    return results


def evaluate_model(X_train, X_test, y_train, y_test, model_name):
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(),
        "Decision Tree Regression": DecisionTreeRegressor(),
        "Random Forest Regression": RandomForestRegressor(),
        "Support Vector Regression": SVR(),
        "Gradient Boosting Regression": GradientBoostingRegressor(),
    }

    if model_name not in models:
        raise ValueError(
            f"Model {model_name} not recognized. Available models: {list(models.keys())}"
        )

    model = models[model_name]
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    result = {"model": model, "mse": mse, "r2_score": r2}
    # logging.info(f"{model_name} - MSE: {mse}, R2: {r2}")

    return result


def prepare_data_for_ml(merged_data, features, test_size=0.2, random_state=42):
    X = merged_data[features]
    y = merged_data["nFires"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    results = evaluate_models(X_train, X_test, y_train, y_test)

    return results


def hyperparameter_tuning(
    merged_data, parameter_list, target_column="nFires", test_size=0.2, random_state=42
):
    # Convert parameter list to string format for feature selection
    str_parameter_list = [str(param) for param in parameter_list]
    feature_list = ["Year", "Month"] + str_parameter_list

    # Extract features and target variable, excluding the "State" column
    X = merged_data[feature_list]
    y = merged_data[target_column]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Define the hyperparameter grid
    param_grid = {
        "max_depth": list(range(5, 21, 5)),  # Smaller range for max depth
        "max_features": [1, 2, 3],  # Only up to the number of features you have
    }

    # Initialize the RandomForestRegressor
    rf = RandomForestRegressor(random_state=random_state)

    # Initialize GridSearchCV
    grid_search = GridSearchCV(
        estimator=rf, param_grid=param_grid, cv=3, scoring="neg_mean_squared_error"
    )

    # Fit GridSearchCV
    grid_search.fit(X_train, y_train)

    # Get the best parameters and model
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_

    return best_params, best_model


if __name__ == "__main__":
    parameter_list = [
        wt.DwdObservationParameter.MONTHLY.PRECIPITATION_HEIGHT,
        wt.DwdObservationParameter.MONTHLY.WIND_FORCE_BEAUFORT,
        wt.DwdObservationParameter.MONTHLY.SUNSHINE_DURATION,
    ]
    state = "Baden-Württemberg"
    weather_data = prepare_weather_data(parameter_list, state)
    state_wildfire_data = prepare_wildfire_data(state)
    combined_weather_data = weather_data[0]

    for additional_data in weather_data[1:]:
        combined_weather_data = pd.merge(
            combined_weather_data, additional_data, on=["Year", "Month"]
        )
    merged_data = pd.merge(
        combined_weather_data, state_wildfire_data, on=["Year", "Month"]
    )

    weather_columns = combined_weather_data.columns.tolist()
    weather_columns.remove("Year")
    weather_columns.remove("Month")
    new_column_order = ["Year", "Month"] + weather_columns + ["nFires"]
    merged_data = merged_data[new_column_order]
    merged_data.dropna(inplace=True)
    merged_data["state"] = state
    merged_data.to_csv(common_paths.DATA.joinpath(f"dwd/{state}.csv"))
    # merged_data = prepare_data(parameter_list, state)
# str_parameter_list = [str(param) for param in parameter_list]
# feature_list = ["Year", "Month"] + str_parameter_list
# model_results = prepare_data_for_ml(merged_data, feature_list)

# for model_name, metrics in model_results.items():
#     print(f"{model_name} - MSE: {metrics['mse']}, R2: {metrics['r2_score']}")
#     if model_name == "Linear Regression":
#         print("Coefficients:", metrics["model"].coef_)
# shortname_to_state = {
#     "BW": "Baden-Württemberg",
#     "BY": "Bayern",
#     "BE": "Berlin",
#     "BB": "Brandenburg",
#     "HB": "Bremen",
#     "HH": "Hamburg",
#     "HE": "Hessen",
#     "MV": "Mecklenburg-Vorpommern",
#     "NI": "Niedersachsen",
#     "NW": "Nordrhein-Westfalen",
#     "RP": "Rheinland-Pfalz",
#     "SL": "Saarland",
#     "SN": "Sachsen",
#     "ST": "Sachsen-Anhalt",
#     "SH": "Schleswig-Holstein",
#     "TH": "Thüringen",
# }
