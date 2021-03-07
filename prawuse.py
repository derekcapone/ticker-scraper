import json
import praw
import datetime


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


def get_reddit_instance():
    """
    Retrieves private values and instantiates an instance of praw.Reddit
    :return: Instance of praw.Reddit
    """
    c_id = get_private_value("client_id")
    c_secret = get_private_value("client_secret")
    ua = get_private_value("user_agent")
    user = get_private_value("username")
    pw = get_private_value("password")

    r = praw.Reddit(
        client_id=c_id,
        client_secret=c_secret,
        user_agent=ua,
        username=user,
        password=pw
    )
    return r


if __name__ == "__main__":
    reddit = get_reddit_instance()
    subreddit = reddit.subreddit("wallstreetbets")

    for submission in subreddit.hot(limit=3):
        comment_queue = submission.comments[:100]  # Get first 100 comments
        info_string = "{} has {} comments".format(submission.title, len(comment_queue))
        print(info_string)