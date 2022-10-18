import pandas as pd
import tweepy

# saving environment variables in a variable so that it is easy to acces
from settings import API_KEY, API_KEY_SECRET, API_TOKEN_SECRET,API_ACCESS_TOKEN


class twitterSpider():
    def __init__(self, consumerKey, consumerSecret, accessKey, accessSecret, searchTerm, searchDate, numberOfTweets):
        # search date mus be in yyyy-mm--dd. Example: 2022-10-17
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessKey, accessSecret)
        self.api = tweepy.API(auth)
        self.searchTerm = searchTerm
        self.searchDate = searchDate
        self.numberOfTweets = numberOfTweets

        # will allow us to run the script indefinitely
        # without fear of passing the API rate limit
        self.api.wait_on_rate_limit = True

    # main method that will call the twitter api to retrieve tweets
    def fetchTweets(self):
        # create a database/DataFrame
        database = pd.DataFrame(columns=[
        "username",
        "description",
		"location",
		"following",
		"followers",
		"totaltweets",
		"retweetcount",
		"text",
		"hashtags",
		"accountID",
		"accountCreatedAt",
		"tweetID" 
    ])
    # .Cursor() will search throught twitter and automatically paginate the results
    # so that we do not have to manually fetch more tweets
        tweets = tweepy.Cursor(self.api.search_tweets, self.searchTerm,
         since_id=self.searchDate, tweet_mode="extended").items(self.numberOfTweets)

        # the .cursor()  method returns an object we can iterate over. This object has
        # various attributes that can tell us mroe about a tweet
        allTweets = [tweet for tweet in tweets]

        # must initialise a counter to maintain the tweet count
        n = 1

        for tweet in allTweets:
            username = tweet.user.screen_name
            description = tweet.user.description
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            retweetcount = tweet.retweet_count
            hashtags = tweet.entities['hashtags']
            accountCreatedAt = tweet.user.created_at
            accountID = tweet.user.id_str
            tweetID = tweet.id

            # Retweets can be distinguished by a retweeted_status attribute,
            # if there is an invalid reference, then an except block will be executed

            try:
                text = tweet.retweeted_status.full_text
            
            except AttributeError:
                text = tweet.full_text
            hashText = list() #save hastags in here
            for h in range(0, len(hashtags)):
                hashText.append(hashtags[h]["text"])
            
            # append all extracted information into the dataFrame
            nthTweet = [
                        username, description,
                        location, following,
                        followers, totaltweets,
                        retweetcount, text, hashText,
                        accountCreatedAt,accountID,tweetID
                        ]
            
            database.loc[len(database)] = nthTweet

            print(str(n) +"th tweet downloaded")
            n += 1 # move onto the next tweet in the list
        
        filename = "data.csv"

        # save dataframe into a csv file
        database.to_csv(filename)
        print("saved all tweets 🎉✨")

if __name__ == '__main__':
        # when run as a solo module, you can search for a tweet from the terminal
        print("Input a hashTag  or term to search twitter for")
        searchTerm = input()

        print("Input a  date to search from in the form yyyy-mm--dd")
        searchTimeFrame = input()

        print("How many tweets do you want to get back")
        tweetNum = input()
        tweetNum = int(tweetNum)

        # i am going to limit this to 50 for performance reasons 
        if tweetNum >= 51:
            print("================================================")
            print("================================================")
            print("Hmmm 😗😗😗 ...")
            print("Slow down buddy 🐌.")
            print("My overlord has instructed me to return only 50 tweets 😗")
            print("================================================")
            print("================================================")
            tweetNum = 50


        # use keys and credentials from twitter API
        consumerKey = API_KEY
        consumerSecret = API_KEY_SECRET
        accessKey = API_ACCESS_TOKEN
        accessSecret = API_TOKEN_SECRET

        spider = twitterSpider(consumerKey, consumerSecret, accessKey, accessSecret, searchTerm, searchTimeFrame, tweetNum)

        spider.fetchTweets()
