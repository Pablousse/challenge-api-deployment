from typing import Any, Dict, List
import pandas as pd


def preprocess(json_data: Dict[str, Any]) -> pd.DataFrame:

    data = json_data["data"]

    if isinstance(data, list):
        new_data = []
        for line in data:
            line = clean_json_line(line)
            new_data.append(line)

        data = new_data

    else:
        data = clean_json_line(data)

    df = pd.json_normalize(data)
    print(data)
    if "building-state" in list(df.columns):
        df = transform_categorical_feature(df, "building-state", "is_building_condition_")

    if "property-type" in list(df.columns):
        df = transform_categorical_feature(df, "property-type", "is_subtype_")

    df = transform_categorical_feature(df, "zip-code", "zipcode_")
    df = df.rename(columns={'rooms-number': 'room_number', 'facade-count': 'facade_count'})
    df = apply_blueprint(df)

    # To check the result
    # df.to_csv("prediction_fit-2.csv", index=False, header=True)

    return df


def clean_json_line(json_line: Dict[str, Any]) -> Dict[str, Any]:

    int_variables = ["rooms-number", "zip-code", "facade-count"]
    float_variables = ["area"]
    building_state_enum = ["AS_NEW", "GOOD", "JUST_RENOVATED", "TO_BE_DONE_UP", "TO_RENOVATE", "TO_RESTORE"]

    clean_json_line = {}

    for k, v in json_line.items():
        if str(v).upper() not in ["None".upper(), "Nan".upper(), "Null".upper()]:
            clean_json_line[k] = v

    json_line = clean_json_line
    
    if "area" not in json_line:
        raise Exception("Area is mandatory")
    if "zip-code" not in json_line:
        raise Exception("Zip-code is mandatory")

    convert_dict_value(json_line, float_variables, "float")
    convert_dict_value(json_line, int_variables, "int")

    if "building-state" in json_line:
        json_line["building-state"] = str.upper(json_line["building-state"]).strip().replace(" ", "_")
        if not (json_line["building-state"] in building_state_enum):
            raise ValueError("Wrong building-state value")
    print(json_line)
    return json_line


def convert_dict_value(data: Dict[str, Any], key_dict: List[str], variable_type: str) -> None:
    try:
        for variable in key_dict:
            if variable in data:
                if variable_type == "float":
                    data[variable] = float(data[variable])
                elif variable_type == "int":
                    data[variable] = int(data[variable])
    except ValueError:
        raise ValueError(f"Could not convert {data[variable]} to {variable_type} (key = {variable})")


def apply_blueprint(data: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame(data)

    df_blueprint = pd.read_csv("model_blueprint.csv")

    columns_order = df_blueprint.columns

    columns_to_drop = list(set(df.columns) - set(df_blueprint.columns))

    df["area"] = df["area"].fillna(df_blueprint["area"].iloc[0])
    if "room_number" in list(df.columns):
        df["room_number"] = df["room_number"].fillna(df_blueprint["room_number"].iloc[0])
    if "facade_count" in list(df.columns):
        df["facade_count"] = df["facade_count"].fillna(df_blueprint["facade_count"].iloc[0])

    df_test = df.fillna(0)

    df_test = df_test.drop(columns_to_drop, axis=1)
    df_blueprint = df_blueprint.drop(list(df_test.columns), axis=1)

    df_test["true_column"] = 1
    df_blueprint["true_column"] = 1

    df_merged = pd.merge(df_test, df_blueprint, on='true_column').drop("true_column", axis=1)

    df_merged = df_merged[list(columns_order)]

    return df_merged


def transform_categorical_feature(df: pd.DataFrame, column_name: str, column_prefix: str = "") -> pd.DataFrame:
    """
    creates columns of binary values from categorical textual information
    """

    df1 = pd.get_dummies(df[column_name].astype(str))
    if column_prefix != "":
        df1.columns = [column_prefix + col for col in df1.columns]

    new_df = pd.concat([df, df1], axis=1)

    # we don't need transformed column anymore
    new_df = new_df.drop(columns=[column_name])

    return new_df