
The goal of this project is to learn how to pull twitter data, using the tweepy wrapper around the twitter API, and how to perform simple sentiment analysis using the vaderSentiment library. The tweepy library hides all of the complexity necessary to handshake with Twitter's server for a secure connection.

We also produce a web server running at AWS to display the most recent 100 tweets from a given user and the list of users followed by a given user. For example, in response to URL /the_antlr_guy the web server will respond with a tweet list color-coded by sentiment, using a red to green gradient:

![alt text](https://github.com/AditiSharmaUSFCA/Twitter-Sentiment-Analysis/blob/master/twitter.png)
