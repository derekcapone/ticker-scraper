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
    """
    Checks if ticker corresponds to actual company, adds to seen_tickers.json if so, discard otherwise
    :param ticker: String holding possible ticker
    :return:
    """
    company = get_company_name(ticker)

    if company is not None:
        new_company = {ticker: company}
        update_seen_tickers(new_company)
    else:
        logging.debug("{} is not a known ticker".format(ticker))


def is_possible_ticker(tick_str: str):
    """
    Parse tick_str to check if string is between 1 and 6 characters and is uppercase (structure of ticker symbols)
    :param tick_str: String holding possible ticker
    :return: True if possible ticker, false otherwise
    """
    if tick_str.isupper() and 1 <= len(tick_str) <= 6:
        return True
    else:
        return False


def check_comment_str(comment: str):
    """
    Parses through a comment string to check for possible tickers
    Generates list of possible tickers to check
    :param comment: String holding comments
    :return: List of possible tickers
    """
    if not isinstance(comment, str):
        raise TypeError("Given object is not a string: {} is {}".format(comment, type(comment)))

    ticker_list = []
    for item in comment.split(" "):
        if is_possible_ticker(item):
            logging.debug("Found possible ticker: {}".format(item))
            ticker_list.append(item)
    return ticker_list


if __name__ == "__main__":
    test_str = "this ADC string ADM contains CEO AMOV a FCAC possible FCST ticker"

    list_of_tickers = check_comment_str(test_str)
    print(list_of_tickers)
