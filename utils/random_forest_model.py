from typing import Optional

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from utils.data_cleaners import clean_df, remove_outliers, transform_categorical_feature


def create_random_forest_model(
    dataset_type: Optional[str] = "",
) -> RandomForestRegressor:
    """The aim of this function is to create and train the model that we are gonna use for the predictions

    Args:
        dataset_type (Optional[str], optional): This parameter can't be either "", "HOUSE" or "APARTMENT"
        it determines which dataset we are using to train or model in case of "", it trains it with the complete dataset

    Returns:
        RandomForestRegressor: returns the model
    """
    df = pd.read_csv("assets/houses.csv")
    df = clean_df(df)
    df = remove_outliers(df)
    if dataset_type != "":
        df = df.loc[df["type"] == dataset_type]
    df = df.query(" 999 < location < 1300")
    df = df.drop(
        [
            "id",
            "type",
            "kitchen_equipped",
            "fireplace",
            "terrace",
            "garden",
            "swimming_pool",
        ],
        axis=1,
    )
    ndf = transform_categorical_feature(df, "subtype", "is_subtype_")
    ndf = transform_categorical_feature(ndf, "building_condition", "is_building_condition_")
    ndf = transform_categorical_feature(ndf, "location", "zipcode_")
    y = ndf.price.to_numpy().reshape(-1, 1)
    ndf = ndf.drop(["price"], axis=1)
    x = ndf.to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)
    reg = RandomForestRegressor(random_state=0).fit(X_train, y_train)
    df["predicted_price"] = reg.predict(x)
    df = df.sort_values(by="location")
    df.to_csv("Brussels-price-predictions.csv", index=False, float_format="%.0f")
    print(f"Score = {reg.score(X_test,y_test)}")

    return reg
