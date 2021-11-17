# import files and give access to tokens and keys
import tweepy
import datetime
import pandas as pd
import time
import json

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


if __name__ == "__main__":
    print("Start getting tweets...")
    stream = StdOutListener(
        TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.filter(locations=[-74, 40, -73, 41],
                  languages='en',
                  threaded=True)
    time.sleep(RUNTIME)
    stream.disconnect()
    df = pd.json_normalize(res)
    print(df)
    df.to_csv('tweets.csv')
