import requests
import json
import logging
import argparse


def get_company_name(ticker):
    """
    Gets company name from Yahoo finance given ticker
    Note: Tickers are case sensitive and must be upper-case
    :param symbol: String holding ticker
    :return: String holding company name
    """
    logging.debug("Checking if {} is valid ticker".format(ticker))
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(ticker)
    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        # check response for company (account for appended characters on ticker symbol in result)
        if x['symbol'] == ticker:
            return x['name']


def ticker_seen(ticker):
    """
    Checks seen_tickers.json for whether the ticker has already been tracked
    :param ticker:
    :return:
    """
    logging.debug("Checking if {} already in list")
    with open("seen_tickers.json", "r+") as file:
        data = json.load(file)
        if data[ticker]:
            print("Found")
        else:
            print("Not found")



def update_seen_tickers(new_ticker: dict):
    """
    Updates seen_tickers.json with new ticker
    :param new_ticker: dict holding ticker and company name: {"ticker": "company name"}
    """
    logging.debug("Adding {} to ticker list".format(next(iter(new_ticker))))
    with open("seen_tickers.json", "r+") as file:
        data = json.load(file)
        data.update(new_ticker)
        file.seek(0)
        json.dump(data, file, indent=4)


def add_new_ticker(ticker: str):
    company = get_company_name(ticker)

    if company is not None:
        new_company = {ticker: company}
        update_seen_tickers(new_company)
    else:
        print("{} is not a known ticker".format(ticker))


def is_possible_ticker(tick_str: str):
    """
    Parse tick_str to check if it string is between 1 and 6 characters and is uppercase
    :param tick_str: String holding possible ticker
    :return: True if possible ticker, false otherwise
    """
    if not isinstance(tick_str, str):
        raise TypeError("Given object is not a string: {} is {}".format(tick_str, type(tick_str)))

    if tick_str.isupper() and 1 <= len(tick_str) <= 6:
        return True
    else:
        return False


def check_comment_str(comment: str):
    """
    Parses through a comment string to check for possible tickers
    Adds actual tickers to the seen_tickers.json file
    :param comment:
    :return:
    """
    print("Checking comment string")


if __name__ == "__main__":
    test_str = "this string contains AMOV a possible ticker"

    for item in test_str.split(" "):
        is_possible_ticker(item)

    try:
        is_possible_ticker(4)
    except TypeError as err:
        logging.exception(err.args)

    add_new_ticker(test_str)
