from model.random_forest_model import serialize_model


# create_random_forest_model("")
serialize_model("model.pkl")
# create_random_forest_model("HOUSE")
# create_random_forest_model("APARTMENT")


# class Test(object):
#     def __init__(self, data):
#         self.__dict__ = json.loads(data)


# json_data = '{"data": {"area": "20","property-type": "APARTMENT","rooms-number": "2","zip-code": "1000","building-state": "TO RENOVATE" } }'
# test1 = Test(json_data)
# print(test1.data)
