# import files and give access to tokens and keys
import tweepy
import pandas as pd
import time
import json
import sys
from textblob import TextBlob
import logging
from datetime import datetime


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


def update_tweets():
    """Get a slice of tweets in a given timeframe. """
    logging.info("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  languages=['en'],
                  threaded=True)
    countdown(RUNTIME)
    stream.disconnect()
    df = pd.json_normalize(res).loc[:, ["created_at", "id", "text"]]
    df[['polarity', 'subjectivity']] = df['text'].apply(lambda x: pd.Series(TextBlob(x).sentiment))
    df.to_csv("updated_tweets.csv")
    return 0


def get_all_tweets(timer=10):
    """Get all tweets without slicing in a given timeframe. """
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
    with_senti = pd.read_csv("tweetsexample_with_sentiment.csv", index_col=0)
    # print(with_senti.iloc[0, :]["created_at"])
    # print(type(with_senti.iloc[0, :]["created_at"]))
    # datetime_object = datetime.strptime(with_senti.iloc[0, :]["created_at"],
    #                                     '%a %b %d %H:%M:%S %z %Y')
    # print(datetime_object)
    with_senti["inferred"] = pd.to_datetime(with_senti["created_at"], infer_datetime_format=True)
    # print(with_senti.head())
    with_senti["Time"] = with_senti["inferred"].dt.tz_localize("utc").dt.tz_convert("US/Eastern").dt.tz_localize(None)
    # res = with_senti["inferred"].dt.tz_localize("utc").dt.tz_convert("US/Eastern")
    # print(res)
    # print(res.dt.tz_localize(None))
    # s = with_senti.loc[:, ["inferred", "local_time"]]
    # print(s.head())
    # print(with_senti.head())
    with_senti = with_senti.rename(columns={"id": "Id",
                                            "text": "Text",
                                            "polarity": "Polarity",
                                            "subjectivity": "Subjectivity"})
    with_senti = with_senti.loc[:, ["Time", "Id", "Text", "Polarity", "Subjectivity"]]
    with_senti.to_csv("tweet_with_sentiment_local.csv")

