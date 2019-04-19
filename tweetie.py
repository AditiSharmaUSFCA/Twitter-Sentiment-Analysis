import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from collections import defaultdict

def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    customer_key, customer_secretkey, token_key, token_secret_key = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(customer_key, customer_secretkey)
    auth.set_access_token(token_key, token_secret_key)
    api = tweepy.API(auth)
    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """

    tweetlist = []
    analyzer = SentimentIntensityAnalyzer()
    user = api.get_user(name)
    for status in tweepy.Cursor(api.user_timeline, id=name).items(100):
        tweet = defaultdict()
        tweet['id'] = status._json['id']
        tweet['created'] = time.strftime('%Y-%m-%d',time.strptime(status._json['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
        tweet['retweeted'] = status._json['retweet_count']
        tweet['text'] = status._json['text']
        tweet['hashtags'] = status.entities['hashtags']
        tweet['url'] = [i['url'] for i in status.entities['urls']]
        tweet['mentions'] = [i["screen_name"] for i in status.entities['user_mentions']]
        tweet = dict(tweet)
        tweet['score'] = analyzer.polarity_scores(tweet['text'])['compound']
        tweetlist.append(tweet)

    tweetdata = {"user": user.screen_name, "count": user.statuses_count, "tweet": tweetlist}
    return tweetdata

def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    friends = []
    for i in api.friends_ids(name):
        details = dict()
        user=api.get_user(i)
        details['name'] = user.name
        details['screen_name'] = user.screen_name
        details['followers'] = user.followers_count
        details['created'] = time.strftime('%Y-%m-%d', time.strptime(str(user.created_at), "%Y-%m-%d %H:%M:%S"))
        details['image'] = user.profile_image_url_https
        friends.append(details)
    return friends
