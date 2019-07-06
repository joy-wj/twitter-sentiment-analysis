# twitter-sentiment-analysis

### Goal

The goal of the project is to pull twitter data on a user's tweets content, using the [tweepy](http://www.tweepy.org/) wrapper around the twitter API, and to perform simple sentiment analysis using the [vaderSentiment](https://github.com/cjhutto/vaderSentiment) library. <br/>

After the sentiment analysis, display the result as the most recent 100 tweets from the given user and the list of users followed by that given user. 

### Data


__About tweets:__
- id: tweet ID
- Tweet creation data
- Num. of tweets
- text of the tweet
- hashtags: lists of hashtags mentioned in the tweet
- urls: list of URLs mentioned in the tweet
- mentions: list of screen names mentioned in the tweet
- score: the "compound" polarity score from vader's `polarity_scores()`

__About users__

- name: real name
- screen_name: Twitter screen name
- followers: number of followers
- created: created date (without time info)
- image: the URL of the profile's image

### Approach


- Load API keys
- Fetch data from the API and generate a polarity score using:
    - `vaderSentiment` - SentimentIntensityAnalyzer
- Add color and map the score to a range of colors: 
    - From "Red" to "Green" according to the score
- Display results onto HTML pages using Flask

### Result

1. `my tweets`:
    - Display 100 recent tweets in a color range from red to green
    - Each of the tweet is hyperlinked to the acutal tweeter content page

2. `my following`:
    - Display 50 of my followers

### Example Output

For [the_antlr_guy](https://twitter.com/the_antlr_guy), `my tweets` will display:

<img src=img/parrt-tweets.png width=800>

`my following` will display:

<img src=img/parrt-follows.png width=320>

Another example: [realdonaldtrump](https://twitter.com/realDonaldTrump), `my tweets` will display:

<img src=img/trump-tweets.png width=800>

`my following` will display:

<img src=img/trump-follows.png width=350>