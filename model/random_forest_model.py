from typing import Optional

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

from data_cleaners import clean_df, remove_outliers, transform_categorical_feature


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
    create_blueprint_dataframe(ndf)
    x = ndf.to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=1, test_size=0.2)
    reg = RandomForestRegressor(random_state=0).fit(X_train, y_train)
    # print(f"Score = {reg.score(X_test,y_test)}")

    return reg


def serialize_model(model_name: str, dataset_type: Optional[str] = "") -> None:
    reg = create_random_forest_model(dataset_type)
    joblib.dump(reg, f"api/{model_name}")


def create_blueprint_dataframe(df: pd.DataFrame) -> None:

    mandatory_column = ["area", "room_number", "facade_count", ]

    new_df_mean = df.mean()
    new_df = df.iloc[[0]].replace(1, 0)

    for column in mandatory_column:
        new_df[column] = new_df_mean[column].astype(float)

    new_df.to_csv("api/model_blueprint.csv", index=False, header=True)
