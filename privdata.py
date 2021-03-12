import json


def get_private_value(val_name):
    """
    Gets a value from the private
    :param val_name: name of private value to retrieve
    :return: string containing private value
    """
    f = open("PrivateValues.json")
    priv_str = f.read()
    f.close()
    ret_dict = json.loads(priv_str)
    return ret_dict[val_name]