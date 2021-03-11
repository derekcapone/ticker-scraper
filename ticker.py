import requests
import json
import logging
import re
import argparse


def get_company_name(ticker):
    """
    Gets company name from Yahoo finance given ticker
    Note: Tickers are case sensitive and must be upper-case
    :param ticker: String holding ticker
    :return: String holding company name
    """
    logging.info("Checking if {} is valid ticker".format(ticker))
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(ticker)
    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        # check response for company (account for appended characters on ticker symbol in result)
        if x['symbol'] == ticker:
            return x['name']


def is_ticker_seen(ticker):
    """
    Checks for whether the ticker has already been tracked
    :param ticker:
    :return: String containing company name if ticker already seen, None otherwise
    """
    logging.info("Checking if {} already in list".format(ticker))
    with open("seen_tickers.json", "r+") as file:
        data = json.load(file)
        try:
            company_name = data[ticker]
        except KeyError:
            company_name = None
        finally:
            return company_name


def update_seen_tickers(new_ticker: dict):
    """
    Updates seen_tickers.json with new ticker
    :param new_ticker: dict holding ticker and company name: {"ticker": "company name"}
    """
    logging.info("Adding {} to ticker list".format(next(iter(new_ticker))))
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
        logging.info("{} is not valid ticker".format(ticker))


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
    for item in re.split('\s|,|\.|!', comment):
        if is_possible_ticker(item):
            logging.info("Found possible ticker: {}".format(item))
            ticker_list.append(item)
    return ticker_list


def parse_possible_tickers(ticker_list: list):
    """
    Goes through ticker_list and checks each string to see if it's a valid ticker
    If ticker is valid, checks seen tickers for this, adds to seen tickers if valid
    :param ticker_list: list of possible tickers with correct structure
    """
    logging.info("Checking ticker_list...")

    for ticker in ticker_list:
        if not isinstance(ticker, str):
            raise TypeError("Given object is not a string: {} is {}".format(ticker, type(ticker)))
            return

        if is_ticker_seen(ticker) != None:
            logging.info("Ticker {} has already been seen".format(ticker))
            # TODO: Add functionality to update how many times ticker has been seen, date seen, etc in json file
        else:
            add_new_ticker(ticker)



if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO) #just for informational purposes

    test_str = "this ADC. string ADM, contains CEO! AMOV a FCAC possible FCST ticker"

    list_of_tickers = check_comment_str(test_str)
    parse_possible_tickers(list_of_tickers)
