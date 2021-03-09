import requests
import json
import argparse


def get_company_name(ticker):
    """
    Gets company name from Yahoo finance given ticker
    Note: Tickers are case sensitive and must be upper-case
    :param symbol: String holding ticker
    :return: String holding company name
    """
    print("Checking if {} is valid ticker".format(ticker))
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
    print("Checking if {} already in list")
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
    print("Adding {} to ticker list".format(next(iter(new_ticker))))
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


if __name__ == "__main__":
    tick = "AMOV"
    add_new_ticker(tick)
