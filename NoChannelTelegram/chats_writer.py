import json

def update_config(path: str, data):
    with open(path, "w") as file:
        json.dump(data, file)

def update_lang(path: str, data):
    with open(path, "w") as file:
        json.dump(data, file)
