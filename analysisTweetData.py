import csv
import tweepy
import re

consumer_key = "comsumerKey"
consumer_secret = "consumerSecret"
access_token = "accessToken"
access_token_secret = "accessTokenSecret"


# define our function: what are we doing, what arguments do we need to do it?
def search_for_hashtags(
    consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase
):

    # create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # initialize Tweepy API
    api = tweepy.API(auth)

    # make the name of the spreadsheet we will write to
    # it will be named whatever we search
    fname = "_".join(re.findall(r"#(\w+)", hashtag_phrase))

    # open the spreadsheet we will write to
    with open("%s.csv" % (fname), "w", encoding="utf-8") as file:

        w = csv.writer(file)

        # write header row to spreadsheet
        w.writerow(
            ["timestamp", "tweet_text", "username", "all_hashtags", "followers_count"]
        )

        # 50000 tweet olarak belirledim fakat limit ne kadar izin verirse o kadar tweet getirebiliyoruz ve burada aradığımız konuda atılan tweet sayısı da önemli
        for tweet in tweepy.Cursor(
            api.search_tweets,
            q=hashtag_phrase + " -filter:retweets",
            lang="en",
            tweet_mode="extended",
            result_type="recent",
        ).items(50000):
            w.writerow(
                [
                    tweet.created_at,
                    tweet.full_text.replace("\n", " ").encode("utf-8"),
                    tweet.user.screen_name.encode("utf-8"),
                    [e["text"] for e in tweet._json["entities"]["hashtags"]],
                    tweet.user.followers_count,
                ]
            )


# this creates input boxes where you will input your keys given to you by twitter


hashtag_phrase = input(
    "Hashtag Phrase "
)  # you'll enter your search terms in the form "#xyz" ; use logical operators AND/OR

if __name__ == "__main__":
    search_for_hashtags(
        consumer_key, consumer_secret, access_token, access_token_secret, hashtag_phrase
    )
