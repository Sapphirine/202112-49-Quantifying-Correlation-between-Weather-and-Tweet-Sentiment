# import files and give access to tokens and keys
import tweepy
import pandas as pd
import time
import json
import sys
from textblob import TextBlob


TWITTER_ACCESS_TOKEN = '1086889183388479488-yr5yewh0PpZUO66c5QzwLGeShZo5Gj'
TWITTER_ACCESS_TOKEN_SECRET = 'HTAtrSypgnMldkeIHxg1KDF2XFHb9pwnYGfiFoElRVzct'
TWITTER_CONSUMER_KEY = 'A59Dr8cri4JCcJDQ9CJ9IJi2h'
TWITTER_CONSUMER_SECRET = 'p4SyvWpii39n3ERJHze2LWWrfHZFWYMOAsx6y1x2fAsXudASzi'

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

RUNTIME = 10

res = []


class StdOutListener(tweepy.Stream):
    def on_data(self, data):
        try:
            msg = json.loads(data)
            res.append(msg)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)


def countdown(t):
    for i in range(t, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining...".format(i))
        sys.stdout.flush()
        time.sleep(1)
    print()


def stream_tweets():
    """Stream tweet data.

    Returns:
        A slice of df.
    """
    print("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  languages=['en'],
                  threaded=True)
    countdown(RUNTIME)
    stream.disconnect()
    df = pd.json_normalize(res)
    cols = ["created_at", "id", "text"]
    return df.loc[:, cols]


def get_historic_tweets():
    return 0


def get_all_tweets(timer=10):
    """Get all tweets without slicing.

    Returns:
        A slice of df.
    """
    print("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  languages=['en'],
                  threaded=True)
    countdown(timer)
    stream.disconnect()
    df = pd.json_normalize(res)
    df.to_csv("tweetsexample.csv")


if __name__ == "__main__":
    # dic = stream_tweets()
    # print(dic)
    # get_all_tweets(600)
    # df.to_csv('tweets.csv')
    twitter_df = pd.read_csv("tweetsexample.csv").loc[:, ["created_at", "id", "text"]]
    twitter_df[['polarity', 'subjectivity']] = twitter_df['text'].apply(lambda x: pd.Series(TextBlob(x).sentiment))
    twitter_df.to_csv('tweetsexample_with_sentiment.csv')