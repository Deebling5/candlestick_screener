# Import the libraries
from tweepy import Stream
from tweepy import OAuthHandler
#from tweepy.streaming import StreamListener
import tweepy
import json
import pandas as pd
import csv
import re  # regular expression
import string
import preprocessor as p
import os
import time
import datetime

# Authenticating Twitter API
# Obtain your Twitter credentials from your twitter developer account

consumer_key = ''
consumer_secret = ''
access_key = '-'
access_secret = ''

# Pass your twitter credentials to tweepy via its OAuthHandler

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

## Automating Scraping
# Calls API every 15 minutes to prevent overcalling

# 1. define a for-loop
# 2. define search parameter
# 3. define date period
# 4. define no. of tweets to pull


def scraptweets(search_words, date_since, numTweets, numRuns):

    ## Arguments:
    # search_words -> define a string of keywords for this function to extract
    # date_since -> define a date from which to start extracting the tweets
    # numTweets -> number of tweets to extract per run
    # numRun -> number of runs to perform in this program - API calls are limited to once every 15 mins, so each run will be 15 mins apart.
    ##

    # Define a pandas dataframe to store the date:
    #db_tweets = pd.DataFrame(columns=['Text'])
    
    db_tweets = pd.DataFrame(columns=['Text', 'Username', 'Created', 'Retweeted', 'URL'])
    
    # Define a for-loop to generate tweets at regular intervals
    for i in range(numRuns):
        # We will time how long it takes to scrape tweets for each run:
        start_run = time.time()

        # Collect tweets using the Cursor object
        # .Cursor() returns an object that you can iterate or loop over to access the data collected.
        # Each item in the iterator has various attributes that you can access to get information about each tweet
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en",
                               since=date_since, tweet_mode='extended').items(numTweets)

        # Store these tweets into a python list
        tweet_list = [tweet for tweet in tweets]

        # Obtain the following info (methods to call them out):
        # user.screen_name - twitter handle
        # user.description - description of account
        # user.location - where is he tweeting from
        # user.friends_count - no. of other users that user is following (following)
        # user.followers_count - no. of other users who are following this user (followers)
        # user.statuses_count - total tweets by user
        # user.created_at - when the user account was created
        # created_at - when the tweet was created
        # retweet_count - no. of retweets
        # (deprecated) user.favourites_count - probably total no. of tweets that is favourited by user
        # retweeted_status.full_text - full text of the tweet
        # tweet.entities['hashtags'] - hashtags in the tweet

        # Begin scraping the tweets individually:
        noTweets = 0

        for tweet in tweet_list:

            # Pull the values
            username = tweet.user.screen_name
            #acctdesc = tweet.user.description
            #location = tweet.user.location
            #following = tweet.user.friends_count
            #followers = tweet.user.followers_count
            #totaltweets = tweet.user.statuses_count
            #usercreatedts = tweet.user.created_at
            tweetcreatedts = tweet.created_at
            retweetcount = tweet.retweet_count
            #hashtags = tweet.entities['hashtags']

            try:
                text = tweet.retweeted_status.full_text
                url_url = tweet.retweeted_status.extended_entities['media'][0]
                url = url_url['url']
            except AttributeError:  # Not a Retweet
                text = tweet.full_text
                url = pd.NA

            #text = tweet.full_text

            # Add the 11 variables to the empty list - ith_tweet:
            #ith_tweet = [text]
            ith_tweet = [text, username, tweetcreatedts, retweetcount, url]

            # Append to dataframe - db_tweets
            db_tweets.loc[len(db_tweets)] = ith_tweet
    db_tweets = db_tweets.drop_duplicates(subset=['Text'])
    db_tweets = db_tweets.fillna('NO URL')
    return db_tweets
