import tweepy
import csv
import pandas as pd
####input your credentials here
consumer_key = '2dQUEQEPM6JRKnR6r2UJHJcie'
consumer_secret = 'UjSP1SQwQGCaL6vWCQ6DGUJDqSJcV5vyfQHYfMAvcZ0VwRR7se'
access_token = '1047550207406166016-lER8qKONMeWrFTGRIhed0oIsgJk9Ck'
access_token_secret = 'J9qWBLJcY3AqREiB8GOZDWOLcjOQBNaZS80p43wYqP2lv'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('eth.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)
# count the tweets scraped
count = 0

for tweet in tweepy.Cursor(api.search,q="$ETH",count=100,
                           lang="en",
                           since="2017-04-03").items():
    #print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
    count = count + 1
    print (count)
print ("collected in total %d Tweets" % (count))