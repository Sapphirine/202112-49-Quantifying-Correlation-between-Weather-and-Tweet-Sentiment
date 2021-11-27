from datetime import datetime, timedelta
import time

import yfinance as yf
import pandas as pd
import sklearn.linear_model
from pytz import timezone
import tweepy
import sys
import os
from pyowm.owm import OWM
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import pickle
import csv

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


TWITTER_ACCESS_TOKEN = '1449432052495958022-AdDlldx3p4anKH7EPiGwbh34CyB7Sx'
TWITTER_ACCESS_TOKEN_SECRET = 'fqLcHfsr9hTWmbOgdNYWfeJ3lH0nR5ThTXBSpqcmvOHFJ'
TWITTER_CONSUMER_KEY = 'OxzmAILFV6CYdWLuVBBFZTk4n'
TWITTER_CONSUMER_SECRET = 'tKeW8FSLH7VoqCdLDWQU7eqVkhmylrFUrHBdGJW5lXgkUfvtKh'

APIKEY = '3a7810c48a0c9f7c3c38754e4415f7d7'

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

RUNTIME = 780    # Seconds to collect tweets

res = []

pathTweetStorage = 'airflow/project/tweet_storage.csv'
pathWeatherStorage = 'airflow/project/weather_storage.csv'
pathClassifier = 'airflow/project/classifier.csv'

pathLinearRegression = 'airflow/project/LinearRegression.sav'
pathRidgeRegression1 = 'airflow/project/RidgeRegression1.sav'
pathRidgeRegression2 = 'airflow/project/RidgeRegression2.sav'
pathRidgeRegression3 = 'airflow/project/RidgeRegression3.sav'
pathLasso1 = 'airflow/project/Lasso1.sav'
pathLasso2 = 'airflow/project/Lasso2.sav'
pathLasso3 = 'airflow/project/Lasso3.sav'

pathColumns = 'airflow/project/columns.txt'


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'fred',
    'depends_on_past': False,
    'email': ['fca2118@columbia.edu'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}


class StdOutListener(tweepy.Stream):
    def on_status(self, status):
        global res
        try:
            now = datetime.now(timezone('EST'))
            tweetTime = f'{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}'
            box = [v for v in status.place.bounding_box.coordinates[0]]

            if status.lang == 'en':
                res.append({'Date': tweetTime, 'Text': status.text, 'Box': box})
            return True
        except BaseException as e:
            print("Error on _data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)


def countdown(t):
    for i in range(t, -1, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining...".format(i))
        sys.stdout.flush()
        time.sleep(1)


def atRemover(text):
    words = text.split()
    while words[0][0] == '@':
        words.pop(0)
    return ' '.join(words)


def analyzeSentiment(text):
    sentimentAnalyzerVader = SIA().polarity_scores(text)['compound']        
    sentimentAnalyzerTextBlob = TextBlob(text).sentiment[0]
    
    if sentimentAnalyzerTextBlob > 0 and sentimentAnalyzerVader > 0:
        return 'Positive'
    elif sentimentAnalyzerTextBlob < 0 and sentimentAnalyzerVader < 0:
        return 'Negative'
    return 'Cannot analyze'


def sumTuples(t1, t2):
    a, b = t1
    c, d = t2
    return (a + c, b + d)


def collectTweets():  
    stream = StdOutListener(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    stream.filter(locations=[-74, 40, -73, 41], threaded=True)

    countdown(RUNTIME)
    stream.disconnect()

    with open(pathTweetStorage, 'w', encoding='utf-8') as storage:
        writer = csv.DictWriter(storage, fieldnames=['Date','Text','Box'], lineterminator = '\n')
        writer.writeheader()
        for data in res:
            writer.writerow(data)


def processTweets():
    drops = []
    tweets = pd.read_csv(pathTweetStorage)

    for tweet in range(tweets.shape[0]):
        text = tweets.iloc[tweet, 1]
        tweets.iloc[tweet, 1] = atRemover(text)
        if len(text) < 4:
            drops.append(tweet)

    tweets = tweets.drop(drops)
    tweets.to_csv(pathTweetStorage, encoding='UTF-8', index=False)
    
        
def collectWeather():
    weatherList = []
    owm = OWM(APIKEY)
    mgr = owm.weather_manager()

    for i in range(13):
        now = datetime.now(timezone('EST'))
        weatherTime = f'{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}'
        
        weather = mgr.weather_at_place('New York').weather
        weather_status = weather.status
        temperature = weather.temperature('celsius')['temp']

        weatherList.append({'Time': weatherTime, 'Status': weather_status, 'Temperature': temperature})
        time.sleep(60)

    with open(pathWeatherStorage, 'w', encoding='utf-8') as storage:
        writer = csv.DictWriter(storage, fieldnames=['Time', 'Status', 'Temperature'], lineterminator = '\n')
        writer.writeheader()
        for data in weatherList:
            writer.writerow(data)


def combineAndClassify():
    tweets = pd.read_csv(pathTweetStorage)
    weather = pd.read_csv(pathWeatherStorage)
    weatherDate = [date for date in weather.iloc[:, 0]]

    combined = []

    for tweetInd in range(tweets.shape[0]):
        tweetDate = tweets.iloc[tweetInd, 0]
        try:
            weatherInd = weatherDate.index(tweetDate)
            sentiment = analyzeSentiment(tweets.iloc[tweetInd, 1])
            if sentiment != 'Cannot analyze':
                combined.append({'Date': tweetDate, 'Text': tweets.iloc[tweetInd, 1], 'Box': tweets.iloc[tweetInd, 2],
                                 'Status': weather.iloc[weatherInd, 1], 'Temperature': weather.iloc[weatherInd, 2], 
                                 'Sentiment': sentiment})
        except ValueError:
            pass

    combinedDF = pd.DataFrame.from_dict(combined)
    if os.path.exists(pathClassifier):
        combinedDF.to_csv(pathClassifier, mode='a', index=False, header=False)
    else:
        combinedDF.to_csv(pathClassifier, mode='a', index=False, header=True)


def regression():
    data = pd.read_csv(pathClassifier)
    dataDict = {}
    for dataPointInd in range(data.shape[0]):
        dataKey = (data.iloc[dataPointInd, 3], data.iloc[dataPointInd, 4])

        if data.iloc[dataPointInd, 5] == 'Positive':
            dataDict[dataKey] = sumTuples(dataDict.get(dataKey, (0, 0)), (1, 0))
        else:
            dataDict[dataKey] = sumTuples(dataDict.get(dataKey, (0, 0)), (0, 1))

    dataDictRatio = {}
    for k in dataDict.keys():
        dataDictRatio[k] = dataDict[k][0] / (dataDict[k][0] + dataDict[k][1])

    dataFrList = []
    for k in dataDictRatio.keys():
        dataFrDict = {}
        dataFrDict['Status'] = k[0]
        dataFrDict['Temperature'] = k[1]
        dataFrDict['Positive Ratio'] = dataDictRatio[k]
        dataFrList.append(dataFrDict)

    dataFr = pd.DataFrame.from_dict(dataFrList)
    x = dataFr.drop('Positive Ratio', axis=1)
    y = dataFr.drop(['Status', 'Temperature'], axis=1)
    x = pd.get_dummies(x)

    with open(pathColumns, 'w') as columnFile:
        for col in x.columns:
            columnFile.write(col + ',')

    LR = sklearn.linear_model.LinearRegression()
    LR.fit(x, y)
    pickle.dump(LR, open(pathLinearRegression, 'wb'))

    reg1 = sklearn.linear_model.Ridge(alpha=0.1)
    reg1.fit(x, y)
    pickle.dump(reg1, open(pathRidgeRegression1, 'wb'))

    reg2 = sklearn.linear_model.Ridge(alpha=0.5)
    reg2.fit(x, y)
    pickle.dump(reg2, open(pathRidgeRegression2, 'wb'))

    reg3 = sklearn.linear_model.Ridge(alpha=1)
    reg3.fit(x, y)
    pickle.dump(reg3, open(pathRidgeRegression3, 'wb'))

    lasso1 = sklearn.linear_model.Lasso(alpha=0.1)
    lasso1.fit(x, y)
    pickle.dump(lasso1, open(pathLasso1, 'wb'))

    lasso2 = sklearn.linear_model.Lasso(alpha=0.5)
    lasso2.fit(x, y)
    pickle.dump(lasso2, open(pathLasso2, 'wb'))

    lasso3 = sklearn.linear_model.Lasso(alpha=1)
    lasso3.fit(x, y)
    pickle.dump(lasso3, open(pathLasso3, 'wb'))
    


with DAG(
    'project',
    default_args=default_args,
    description='Project',
    schedule_interval=timedelta(minutes=15),
    start_date=datetime.now(),
    catchup=False,
    tags=['Project'],
) as dag:

    # t* examples of tasks created by instantiating operators

    
    t1 = PythonOperator(
        task_id='t1',
        python_callable=collectTweets,
    )

    t2 = PythonOperator(
        task_id='t2',
        python_callable=processTweets,
    )

    t3 = PythonOperator(
        task_id='t3',
        python_callable=collectWeather,
    )

    t4 = PythonOperator(
        task_id='t4',
        python_callable=combineAndClassify,
    )

    t5 = PythonOperator(
        task_id='t5',
        python_callable=regression,
    )
    

    # task dependencies 

    t1 >> t2
    [t2, t3] >> t4
    t4 >> t5
    
