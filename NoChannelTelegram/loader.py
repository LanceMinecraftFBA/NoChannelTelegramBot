import os
import json

def load_lang(sl: str, path: str):
    if os.path.isfile(path + "/" + sl + ".json"):
        with open(path + "/" + sl + ".json") as data:
            lang_data = json.load(data)
            return lang_data
    else:
        raise FileNotFoundError(path + " not found")
    
def load_chats(path: str):
    if os.path.isfile(path):
        with open(path) as data:
            chats_data = json.load(data)
            return chats_data
    else:
        raise FileNotFoundError(path + " not found")

def load_config(path: str):
    if os.path.isfile(path):
        with open(path) as data:
            b_data = json.load(data)
            return b_data
    else:
        raise FileNotFoundError(path + " not found")
    
def load_save(path: str):
    if os.path.isfile(path):
        with open(path) as data:
            save_data = json.load(data)
            return save_data
    else:
        raise FileNotFoundError(path + " not found")
