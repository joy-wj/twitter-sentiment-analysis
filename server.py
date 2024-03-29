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
import os
from flask import Flask, render_template, send_from_directory
from tweetie import *
from colour import Color

from numpy import median

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
    colors = list(Color("red").range_to(Color("green"), 100))
    OldMax = 1
    OldMin = -1
    NewMax = 100
    NewMin = 0
    OldRange = (OldMax - OldMin)
    NewRange = (NewMax - NewMin)
    for t in tweets:
        score = t['score']
        new_score = (((score - OldMin) * NewRange) / OldRange) + NewMin
        index = round(new_score)
        t['color'] = str(colors[index])
    return tweets


@app.route("/favicon.ico")
def favicon():
    """
    Open and return a 16x16 or 32x32 .png or other image file in binary mode.
    This is the icon shown in the browser tab next to the title.
    """
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/<name>")
def tweets(name):
    "Display the tweets for a screen name color-coded by sentiment score"

    dict_tweets = fetch_tweets(api, name)
    tweets = add_color(dict_tweets['tweets'])
    score_list = []
    for t in tweets:
        score_list.append(t['score'])
    median_score = median(score_list)

    return render_template('tweets.html', records=dict_tweets, tweets=tweets, median=median_score)


@app.route("/following/<name>")
def following(name):
    """
    Display the list of users followed by a screen name, sorted in
    reverse order by the number of followers of those users.
    """
    list_following = fetch_following(api, name)
    sorted_list = sorted(list_following, key=lambda elem: elem['followers'], reverse=True)

    return render_template('following.html', name=name, sorted_list=sorted_list)


i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[i+1] # e.g., "/Users/parrt/Dropbox/licenses/twitter.csv"
#twitter_auth_filename = sys.argv[1]
api = authenticate(twitter_auth_filename)

#app.run(host='0.0.0.0', port=80)
#app.run()
