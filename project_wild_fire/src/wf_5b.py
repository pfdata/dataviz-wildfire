import wetter_api as wt
import waldbrand
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_and_process_weather_data(parameter, state):
    """
    Fetches and processes weather data for a given parameter and state.
    """
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
        weather_data = weather_data.groupby(["Year", "Month"]).mean().reset_index()
        return weather_data
    except Exception as e:
        logging.error(
            f"Error fetching or processing weather data for parameter {parameter}: {e}"
        )
        return pd.DataFrame()


def prepare_data(parameters, state):
    """
    Prepares merged weather and wildfire data for a given list of parameters and state.
    """
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

    return merged_data


def prepare_data_for_ml(
    merged_data, features, test_size=0.2, random_state=42, train_model=False
):
    """
    Prepares data for machine learning by splitting into training and testing sets,
    and optionally trains a linear regression model.
    """
    X = merged_data[features]
    y = merged_data["nFires"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    results = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }

    if train_model:
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        results.update({"model": model, "mse": mse, "r2_score": r2})

    return results


if __name__ == "__main__":
    parameter_list = [
        wt.DwdObservationParameter.MONTHLY.PRECIPITATION_HEIGHT,
        wt.DwdObservationParameter.MONTHLY.TEMPERATURE_AIR_MEAN_200,
        wt.DwdObservationParameter.MONTHLY.SUNSHINE_DURATION,
    ]
    state = "Bayern"
    merged_data = prepare_data(parameter_list, state)
    str_parameter_list = [str(param) for param in parameter_list]
    feature_list = ["Year", "Month"] + str_parameter_list
    prepared_data = prepare_data_for_ml(merged_data, feature_list, train_model=True)

    print("Training data shape:", prepared_data["X_train"].shape)
    print("Testing data shape:", prepared_data["X_test"].shape)

    if "model" in prepared_data:
        print("\nModel Coefficients:", prepared_data["model"].coef_)
        print("Mean Squared Error:", prepared_data["mse"])
        print("R-squared Score:", prepared_data["r2_score"])
