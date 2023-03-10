from flask import Flask, request, render_template
import tweepy
from textblob import TextBlob

app = Flask(__name__)

# Twitter API credentials
consumer_key = "Get_Your_Own_Key"
consumer_secret = "Get_Your_Own_Key"
access_token = "70369388-Get_Your_Own_Key"
access_token_secret = "Get_Your_Own_Key"
# visit https://developer.twitter.com/en to get your credentials.

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sentiment", methods=["POST"])
def sentiment():
    # Get the hashtag from the form index.html
    hashtag = request.form["hashtag"]

     # Retrieve the latest 200 tweets for the given hashtag
    tweets = api.search_tweets(q="#" + hashtag + '-is:retweet lang:en', count=200)
    #-is:retweet means I don't want retweets
    # lang:en is asking for the tweets to be in english

    # Perform sentiment analysis on each tweet
    sentiments = []
    tweet_sentiments = []
    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        sentiment = analysis.sentiment.polarity
        sentiments.append(sentiment)
        tweet_sentiments.append((tweet.text, sentiment))

    # Determine the overall sentiment for the tweets
    overall_sentiment = sum(sentiments) / len(sentiments)
    if overall_sentiment > 0:
        sentiment = "positive"
    elif overall_sentiment < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    # Render the result in the template
    return render_template("sentiment.html", sentiment=sentiment, hashtag="#" + hashtag, tweet_sentiments=tweet_sentiments)


if __name__ == "__main__":
    app.run()
