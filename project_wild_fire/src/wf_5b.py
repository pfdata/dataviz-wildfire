import wetter_api as wt
import waldbrand
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def prepare_data(parameter, state):
    # Fetch and process weather data
    weather_data = wt.fetch_observation_data(parameter, state)
    weather_data["date"] = pd.to_datetime(weather_data["date"])
    weather_data["Year"] = weather_data["date"].dt.year
    weather_data["Month"] = weather_data["date"].dt.month
    weather_data.sort_values(by=["Month", "Year"], inplace=True)
    weather_data.drop(
        columns=["station_id", "dataset", "date", "quality", "parameter"], inplace=True
    )
    weather_data["Year"] = weather_data["Year"].astype(int)
    weather_data["Month"] = weather_data["Month"].astype(int)
    # Aggregate weather data by taking the mean across stations for each year and month
    weather_data = weather_data.groupby(["Year", "Month"]).mean().reset_index()

    # Fetch and process wildfire data
    wildfire_obj = waldbrand.WildFire()
    wildfire_df = wildfire_obj.get_montly_numbers()
    state_wildfire_data = wildfire_df.loc[[state]]
    state_wildfire_data = wildfire_obj.melt_and_map_months(state_wildfire_data)
    state_wildfire_data["Year"] = state_wildfire_data["Year"].astype(int)
    state_wildfire_data["Month"] = state_wildfire_data["Month"].astype(int)

    # Merge weather and wildfire data
    merged_data = pd.merge(weather_data, state_wildfire_data, on=["Year", "Month"])

    # Desired column order
    new_column_order = ["Year", "Month", "value", "nFires"]

    # Reindex the DataFrame
    merged_data = merged_data[new_column_order]

    return merged_data


def prepare_data_for_ml(merged_data, test_size=0.2, random_state=42, train_model=False):
    # Split into features (X) and target (y)
    X = merged_data[["Year", "Month", "value"]]
    y = merged_data["nFires"]

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Initialize an empty dictionary to store results
    results = {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }

    # Optionally train a linear regression model
    if train_model:
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions on the test data
        y_pred = model.predict(X_test)

        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Add model and metrics to results dictionary
        results["model"] = model
        results["mse"] = mse
        results["r2_score"] = r2

    return results


if __name__ == "__main__":

    # Example usage
    parameter = wt.DwdObservationParameter.MONTHLY.PRECIPITATION_HEIGHT
    state = "Bayern"
    merged_data = prepare_data(parameter, state)
    # print(merged_data)

    # Call the function to prepare data for ML
    prepared_data = prepare_data_for_ml(merged_data, train_model=True)

    # Print results (optional)
    print("Training data shape:", prepared_data["X_train"].shape)
    print("Testing data shape:", prepared_data["X_test"].shape)

    if "model" in prepared_data:
        print("\nModel Coefficients:", prepared_data["model"].coef_)
        print("Mean Squared Error:", prepared_data["mse"])
        print("R-squared Score:", prepared_data["r2_score"])
