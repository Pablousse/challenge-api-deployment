from preprocessing.data_cleaners import transform_categorical_feature
from typing import Any, Dict, List
import pandas as pd


def preprocess(json_data: Dict[str, Any]) -> pd.DataFrame:
    print(json_data)
    data = json_data["data"]
    int_variables = ["rooms-number", "zip-code", "facade-count"]
    float_variables = ["area"]
    building_state_enum = ["NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"]

    convert_dict_value(data, float_variables, "float")
    convert_dict_value(data, int_variables, "int")

    if not (data["building-state"] in building_state_enum):
        raise ValueError("Wrong building-state value")

    df = pd.json_normalize(data)
    df = transform_categorical_feature(df, "property-type", "is_subtype_")
    df = transform_categorical_feature(df, "zip-code", "zipcode_")
    df = transform_categorical_feature(df, "building-state", "is_building_condition_")
    print(df)

    return df


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
    except Exception as e:
        raise e
