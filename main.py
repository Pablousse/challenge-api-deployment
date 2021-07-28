# serialize_model("model.pkl")

# create_random_forest_model("")
# create_random_forest_model("HOUSE")
# create_random_forest_model("APARTMENT")


# class Test(object):
#     def __init__(self, data):
#         self.__dict__ = json.loads(data)


# json_data = '{"data": {"area": "20","property-type": "APARTMENT","rooms-number": "2",
# "zip-code": "1000","building-state": "TO RENOVATE" } }'
# test1 = Test(json_data)
# print(test1.data)

import requests
import json

data = {
    "data": {
        "area": "20",
        "property-type": "APARTMENT",
        "rooms-number": "2",
        "zip-code": "1000",
        "building-state": "TO_RENOVATE",
        "facade-count": 2
    }
}

response = requests.post('https://arnaud-durieux-api-deployment.herokuapp.com/predict', json=data)

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
# print(response.json())
print(str(response.content))
