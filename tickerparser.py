import string
import logging


def is_possible_ticker(tick_str: str):
    """
    Parse tick_str to check if it string is between 1 and 6 characters and is uppercase
    :param tick_str: String holding possible ticker
    :return: True if possible ticker, false otherwise
    """
    if not isinstance(tick_str, str):
        raise TypeError("Not a string")

    if tick_str.isupper() and 1 <= len(tick_str) <= 6:
        return True
    else:
        return False


if __name__ == "__main__":
    test_str = "This is a test string"

    for item in test_str.split(" "):
        is_possible_ticker(item)

    try:
        is_possible_ticker(4)
    except TypeError:
        logging.exception("Testing")