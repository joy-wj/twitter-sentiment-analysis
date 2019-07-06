import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


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
    keys_list = loadkeys(twitter_auth_filename)
    consumer_key = keys_list[0]
    consumer_secret = keys_list[1]
    key = keys_list[2]
    secret = keys_list[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

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
    analyser = SentimentIntensityAnalyzer()

    user = api.get_user(name)
    user_tweets = api.user_timeline(id=name, count=100)
    list_tweets = []

    for tweet in user_tweets:
        d = {}
        d['id'] = tweet.id
        d['created'] = "{:%Y-%m-%d}".format(tweet.created_at)
        d['retweeted'] = tweet.retweet_count
        d['text'] = tweet.text

        list_hashtags = []
        for dict_item in tweet.entities['hashtags']:
            list_hashtags.append(dict_item['text'])
        d['hashtags'] = list_hashtags

        list_urls = []
        for dict_item in tweet.entities['urls']:
            list_urls.append(dict_item['url'])
        d['urls'] = list_urls

        list_mentions = []
        for dict_item in tweet.entities['user_mentions']:
            list_mentions.append(dict_item['screen_name'])
        d['mentions'] = list_mentions

        d['score'] = analyser.polarity_scores(tweet.text)['compound']

        list_tweets.append(d)

    dict_tweets = {
        'user': user.screen_name,
        'count': len(list_tweets),
        'tweets': list_tweets
    }

    return dict_tweets


def fetch_following(api, name):
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
    list_following = []

    friends_ids = api.friends_ids(screen_name=name)
    for id in friends_ids:
        user = api.get_user(id)
        d = {}
        d['name'] = user.name
        d['screen_name'] = user.screen_name
        d['followers'] = user.followers_count
        d['created'] = "{:%Y-%m-%d}".format(user.created_at)
        d['image'] = user.profile_image_url

        list_following.append(d)

    return list_following
