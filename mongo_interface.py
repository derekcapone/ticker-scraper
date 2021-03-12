import pymongo
import privdata


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


def find_populated_field(collection, search_dic):
    """
    Searches for a desired populated field, given field name, and value
    :param collection: MongoDB Collection object to search
    :param search_dic: Dictionary to search for
    :return: List of all matching objects
    """
    return list(collection.find(search_dic))


def insert_document(collection, new_dict):
    """
    Inserts a single document into the collection provided
    :param collection: MongoDB Collection object
    :param new_dict: dict to be inserted into collection
    :return: Resulting InsertOneResult object
    """
    return collection.insert_one(new_dict)


if __name__ == "__main__":
    col = connect_to_collection("Test")

    dic = {
        "name": "TestData2",
        "OtherData": {
            "Embedded1": 1,
            "Embedded2": 2
        }
    }

    insert_document(col, dic)
