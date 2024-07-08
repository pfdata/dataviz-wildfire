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
            columns=["dataset", "date", "quality", "parameter"],
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
            combined_weather_data, additional_data, on=["Year", "Month", "station_id"], how ='outer'
        )

    wildfire_obj = waldbrand.WildFire()

    #dataframes = [get_monthly_area(), get_montly_numbers()]
    #for df in dataframes:
    area_fire = wildfire_obj.get_monthly_area()
    nr_fire = wildfire_obj.get_montly_numbers()

    nr_fire = nr_fire.loc[[state]]
    area_fire = area_fire.loc[[state]]
    
    area_fire = wildfire_obj.melt_and_map_months_area(area_fire)
    nr_fire = wildfire_obj.melt_and_map_months_nr(nr_fire)
    
    area_fire["Year"] = area_fire["Year"].astype(int)
    nr_fire["Year"] = nr_fire["Year"].astype(int)
    area_fire["Month"] = area_fire["Month"].astype(int)
    nr_fire["Month"] = nr_fire["Month"].astype(int)

    merged = pd.merge(area_fire, nr_fire, on=['Year', 'Month'], how='outer')
    
    merged_data = pd.merge(
        combined_weather_data, merged, on=["Year", "Month"]
    )
    
    weather_columns = combined_weather_data.columns.tolist()
    weather_columns.remove("Year")
    weather_columns.remove("Month")
    new_column_order = ["Year", "Month"] + weather_columns + ["nFires", "area"]
    merged_data = merged_data[new_column_order]
    
    rename_params(merged_data)
    transform_windspeed(merged_data)
    merged_data.dropna(inplace=True)
    merged_data.to_csv(common_paths.DATA.joinpath("dwd/data_Brandenburg.csv"))
    
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
            combined_weather_data, additional_data, on=["Year", "Month", ]
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

    result = {"model": model, "mse": mse, "r2_score": r2, "y_pred": y_pred}
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


'''def hyperparameter_tuning(
    merged_all, parameter_list, target_column=merged_all[-1], test_size=0.2, random_state=42
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
'''
'''
def compute_statistics(df, parameters):
    for param in parameters:
        mean = df[param].sum()/df[param].count()
        variance = 0
        str = {'param: ' param ' mean: ' mean ' variance: ' variance}
    return str'''

def setYears(df):
    df = df.where(df.Year>=1995).where(df.Year<=2022)
    return df

def rename_params(df):
    df.rename(columns={'CLIMATE_SUMMARY.PRECIPITATION_HEIGHT':'pr', 'CLIMATE_SUMMARY.WIND_FORCE_BEAUFORT':'sfcWind', 'CLIMATE_SUMMARY.TEMPERATURE_AIR_MAX_200':'tasmax'}, inplace=True)
    return df

def transform_windspeed(df):
    df['sfcWind'] =  0.836 * (df['sfcWind'] ** 1.5)
    return df

def station_means(df):
    df.dropna(inplace=True)
    dep_var = df.columns[-1]
    weather_var = df[['pr', 'sfcWind', 'tasmax']]
    df = df.groupby(['Year', 'Month', dep_var]).agg({
        'pr': 'mean',
        'sfcWind': 'mean',
        'tasmax': 'mean'
    }).reset_index()
    
    new_column_order = ['Year', 'Month', 'pr', 'sfcWind', 'tasmax',  dep_var]
    df = df[new_column_order]
    
    return df

def grid_means(df):
    df.dropna(inplace=True)
    weather_var = df[['pr', 'sfcWind', 'tasmax']]
    date_var = df[['Year', 'Month']]
    df = df.groupby(['Year', 'Month']).agg({
        'pr': 'mean',
        'sfcWind': 'mean',
        'tasmax': 'mean'
    }).reset_index()
    new_column_order = ['Year', 'Month', 'pr', 'sfcWind', 'tasmax']
    df = df[new_column_order]
    return df

# if __name__ == "__main__":
#     pass

#%%
