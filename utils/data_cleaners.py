import pandas as pd


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    a function that will perform initial cleaning tasks
    """
    # columns that have a lot of missing values
    # and the columns are not really necessary
    df = df.drop(
        columns=[
            "terrace_area",
            "garden_area",
            "terrace_area",
            "land_surface",
            "furnished",
        ]
    )

    # removes duplicates that are same in these 4 features
    df = df.drop_duplicates(subset=["location", "price", "area", "building_condition"])

    # removing any row that contains empty area and price information because it's a key feature
    # also removing rows with NaN in facade_count because there are a lot
    df = df.dropna(subset=["area", "facade_count", "price"])

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    finds interquartile range in order to calculate outliers and removes them
    explanation: https://towardsdatascience.com/ways-to-detect-and-remove-the-outliers-404d16608dba
    """

    # finding the 50%
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1

    df_outliers_removed = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

    return df_outliers_removed


def transform_categorical_feature(df: pd.DataFrame, column_name: str, column_prefix: str = "") -> pd.DataFrame:
    """
    creates columns of binary values from categorical textual information
    """

    df1 = pd.get_dummies(df[column_name].astype(str))
    if column_prefix != "":
        df1.columns = ["is_type_" + col for col in df1.columns]

    new_df = pd.concat([df, df1], axis=1)

    # we don't need transformed column anymore
    new_df = new_df.drop(columns=[column_name])

    return new_df
