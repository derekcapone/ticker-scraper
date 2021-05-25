import pymongo
import privdata


class StoredDuplicate(Exception):
    """
    Error class for stored duplicate item in MongoDB database
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'StoredDuplicate, {0} '.format(self.message)
        else:
            return "StoredDuplicate error is raised"


def connect_to_database():
    """
    Connects to database
    :return: Database object
    """
    pw = privdata.get_private_value("mongo_pw")
    db_name = privdata.get_private_value("db_name")
    conn_str = "mongodb+srv://derekcapone7:{}@cluster0.pjhgg.mongodb.net/{}?retryWrites=true&w=majority".format(pw, db_name)
    client = pymongo.MongoClient(conn_str)
    return client[db_name]


def connect_to_collection():
    """
    Connect to desired collection within database
    :return: collection object
    """
    db = connect_to_database()

    col_name = privdata.get_private_value("collection")
    return db[col_name]


def find_top_layer_obj(collection, obj_name):
    """
    Takes collection and searches it for the top layer object named "obj_name"
    :param collection: MongoDB Collection object to search
    :param obj_name: String containing the top layer object name
    :return: Dict containing the entire top layer object of name "obj_name"
    """
    search_dic = {obj_name: {"$exists": True}}
    return list(collection.find(search_dic))


def find_populated_field(search_dic):
    """
    Searches for a desired populated field, given field name, and value
    :param search_dic: Dictionary to search for
    :return: List of all matching objects
    """
    collection = connect_to_collection()
    return list(collection.find(search_dic))


def insert_single_document(new_dict):
    """
    Inserts a single document into the collection provided
    :param new_dict: dict to be inserted into collection
    :return: Resulting InsertOneResult object
    """
    collection = connect_to_collection()
    return collection.insert_one(new_dict)


if __name__ == "__main__":
    dic = {
        "ticker": "ABCD",
        "company_name": "Testing",
        "Test": True,
    }

    insert_single_document(dic)
