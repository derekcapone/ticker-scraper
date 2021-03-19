import requests
import logging
import re
import datetime
import mongo_interface as mng


class TickerInfo:
    def __init__(self, ticker):
        self.ticker = ticker
        self.company_name = None
        self.company_seen = None
        self.valid_ticker = None
        self.date_last_accessed = None
        self.data_type = "company"

        self.init_company_details()

    def init_company_details(self):
        """
        Initialize company details
        """
        self.company_name = None
        self.company_seen = False
        self.valid_ticker = False
        self.date_last_accessed = datetime.date.today()
        # TODO: once more details about seen companies are stored, add those details here
        name = get_existing_company(self.ticker)
        if name != None:
            # Valid stock ticker we've already seen
            self.company_name = name['company_name']
            self.company_seen = True
            self.valid_ticker = True
            return
        name = get_company_name(self.ticker)
        if name != None:
            # Valid stock ticker we haven't seen
            self.company_name = name
            self.valid_ticker = True

        return

    def generate_company_dict(self):
        # TODO: Figure out how to do this part with pre-defined schema
        new_dict = {
            "ticker": self.ticker,
            "company_name": self.company_name,
            "date_accessed": self.date_last_accessed.strftime("%d-%m-%Y"),
            "data_type": self.data_type
        }
        return new_dict


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


def insert_company_info(company: TickerInfo):
    """
    Inserts the company info as a dict into MongoDB
    :param company:
    :return:
    """
    mng.insert_single_document(company.generate_company_dict())


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


def parse_possible_tickers(ticker_list: list, active_companies):
    """
    Goes through ticker_list and checks each string to see if it's a valid ticker
    If ticker is valid, checks seen tickers for this, adds to seen tickers if valid
    :param ticker_list: list of possible tickers with correct structure
    """
    logging.info("Checking ticker_list...")
    company_list = []
    for ticker in ticker_list:
        if not isinstance(ticker, str):
            raise TypeError("Given object is not a string: {} is {}".format(ticker, type(ticker)))
            return

        if not any(active.ticker == ticker for active in active_companies):
            new_company = TickerInfo(ticker)
            if new_company.valid_ticker:
                company_list.append(new_company)
        else:
            logging.info("{} already in active companies.".format(ticker))

    return company_list


def get_existing_company(ticker: str):
    """
    Search for company in database
    :param collection: MongoDB collection holding company information
    :param ticker: Ticker symbol
    :return: Company object
    """
    search_dic = {"ticker": ticker}
    ret_list = mng.find_populated_field(search_dic)

    if len(ret_list) == 0:
        return None
    elif len(ret_list) == 1:
        return ret_list[0]
    else:
        raise mng.StoredDuplicate("Duplicate item found: {}".format(ticker))
        return None


def delete_all_company_data():
    """
    Deletes the entire collection of company data
    """
    col = mng.connect_to_collection()
    col.delete_many(filter={"data_type": "company"})


def test_add_tickers_from_string():
    """
    Test function to display how this module can be used to parse strings, query database, hold active company objects etc.
    """
    active_companies = []
    test_str = "this ADC. string ADM, contains CEO! AMOV a FCAC possible FCST ticker"

    list_of_tickers = check_comment_str(test_str)
    active_companies += parse_possible_tickers(list_of_tickers, active_companies)

    for company in active_companies:
        # insert company info to database if this is the first time we've seen this company
        if not company.company_seen:
            insert_company_info(company)


if __name__ == "__main__":
    test_add_tickers_from_string()
