"""
A server that responds with two pages, one showing the most recent
100 tweets for given user and the other showing the people that follow
that given user (sorted by the number of followers those users have).

For authentication purposes, the server takes a commandline argument
that indicates the file containing Twitter data in a CSV file format:

    consumer_key, consumer_secret, access_token, access_token_secret

For example, I pass in my secrets via file name:

    /Users/parrt/Dropbox/licenses/twitter.csv

Please keep in mind the limits imposed by the twitter API:

    https://dev.twitter.com/rest/public/rate-limits

For example, you can only do 15 follower list fetches per
15 minute window, but you can do 900 user timeline fetches.
"""
import sys
from flask import Flask, render_template
from tweetie import *
from colour import Color
import os
from numpy import median
from flask import send_from_directory

app = Flask(__name__)

def add_color(tweets):
    """
    Given a list of tweets, one dictionary per tweet, add
    a "color" key to each tweets dictionary with a value
    containing a color graded from red to green. Pure red
    would be for -1.0 sentiment score and pure green would be for
    sentiment score 1.0.

    Use colour.Color to get 100 color values in the range
    from red to green. Then convert the sentiment score from -1..1
    to an index from 0..100. That index gives you the color increment
    from the 100 gradients.

    This function modifies the dictionary of each tweet. It lives in
    the server script because it has to do with display not collecting
    tweets.
    """
    colors = list(Color("red").range_to(Color("green"), 101))
    total = []
    for t in tweets:
        score = t['score']
        color = colors[int((score + 1) / 0.02)]
        t['color'] = color
        total.append(score)
    m = round(median(total), 4)
    return m, tweets


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    """
    Open and return a 16x16 or 32x32 .png or other image file in binary mode.
    This is the icon shown in the browser tab next to the title.
    """


@app.route("/<name>")
def tweets(name):
    details = fetch_tweets(api, name)
    m, details = add_color(details['tweet'])
    return render_template('tweets.html', m=m, tweet=details, name=name)

    "Display the tweets for a screen name color-coded by sentiment score"


@app.route("/following/<name>")
def following(name):
    followlist = fetch_following(api, name)
    followers = sorted(followlist, key=lambda k: k['followers'], reverse=True)
    return render_template('following.html', followers=followers,name=name)

    """
    Display the list of users followed by a screen name, sorted in
    reverse order by the number of followers of those users.
    """


i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[i+1] # e.g., "/Users/parrt/Dropbox/licenses/twitter.csv"
#twitter_auth_filename = sys.argv[1]
api = authenticate(twitter_auth_filename)


#app.run(host='0.0.0.0', port=5000)
