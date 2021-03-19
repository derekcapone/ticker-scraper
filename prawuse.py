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


def get_hot_posts(sub_name: str, num_posts=10):
    """
    Gets ListGenerator for hot posts in given subreddit. Retrieves "num_posts" posts
    :param sub_name: String holding the subreddit name
    :param num_posts: Number of posts to retrieve
    :return: ListGenerator for hot posts in subreddit
    """
    reddit = get_reddit_instance()
    subreddit = reddit.subreddit(sub_name)
    return subreddit.hot(limit=num_posts)


def get_top_comments(sub_generator, num_comments: int):
    if not isinstance(sub_generator, praw.models.listing.generator.ListingGenerator):
        raise TypeError("Object is not a subreddit ListingGenerator")

    comment_tree = []
    for submission in sub_generator:
        comment_tree.append(submission.comments[:num_comments])

    return comment_tree


if __name__ == "__main__":
    sub_generator = get_hot_posts("wallstreetbets", 5)
    comment_tree = get_top_comments(sub_generator, 100)
