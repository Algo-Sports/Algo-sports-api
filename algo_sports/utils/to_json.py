import json


def to_json(string):
    return json.dumps(string, separators=[",", ":"])
