import json
import os

def write_json(path_json, dictionary):
    """
    A generic JSOn writing function with file exist check.
    :param path_json:
    :param dictionary:
    :return:
    """
    if os.path.exists(path_json):
        raise FileExistsError(f"{path_json}")
    with open(path_json, 'w') as outfile:
        json.dump(dictionary, outfile)


def read_json(path_json):
    """
    Load JSON and return it as a dictionary.
    :param path_json:
    :return:
    """
    if not os.path.exists(path_json):
        return None

    json_file = open(path_json, "r")
    json_dictionary = json.loads(json_file)
    return json_dictionary