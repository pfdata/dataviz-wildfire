from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler


def build_regressors(random_state: int = 42) -> dict[str, object]:
    return {
        "Linear regression": make_pipeline(RobustScaler(), LinearRegression()),
        "Ridge regression": make_pipeline(RobustScaler(), Ridge(alpha=1.0)),
        "Random forest": RandomForestRegressor(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
        ),
        "Gradient boosting": GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.03,
            max_depth=2,
            loss="huber",
            random_state=random_state,
        ),
    }
