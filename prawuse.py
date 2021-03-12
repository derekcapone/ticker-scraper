import json
import praw
import privdata


def get_reddit_instance():
    """
    Retrieves private values and instantiates an instance of praw.Reddit
    :return: Instance of praw.Reddit
    """
    c_id = privdata.get_private_value("client_id")
    c_secret = privdata.get_private_value("client_secret")
    ua = privdata.get_private_value("user_agent")
    user = privdata.get_private_value("username")
    pw = privdata.get_private_value("reddit_pw")

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