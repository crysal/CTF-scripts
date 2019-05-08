#!/usr/bin/env python
# encoding: utf-8
# easy_install tweepy

import sys
try:
	import tweepy #https://github.com/tweepy/tweepy
except ImportError:
	print "You'll need tweepy instaled on your system. try easy_install tweepy"
	sys.exit()
try:
	import csv
except ImportError:
	print "You'll need the python csv module instaled on your system. try pip install opencv-python"
	sys.exit()

#Twitter API credentials - https://apps.twitter.com/
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

def get_all_tweets(screen_name):

	if (consumer_key == ""):
		print "You need to set up the script first. Edit it and add your keys."
		return

	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.text.encode("utf-8"),tweet.created_at,tweet.id_str,tweet.source,tweet.in_reply_to_status_id_str,tweet.in_reply_to_screen_name,tweet.user,tweet.coordinates,tweet.place,tweet.is_quote_status,tweet.favorite_count,tweet.entities,tweet.favorited,tweet.retweeted,tweet.lang] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["text.encode","tweet.created_at","id_str","source","in_reply_to_status_id_str","in_reply_to_screen_name","user","coordinates","place","is_quote_status","favorite_count","entities","favorited","retweeted","lang"])
		writer.writerows(outtweets)
    print "Be wary of , and TAB in the text"
	
	pass


if __name__ == '__main__':
	if (len(sys.argv) == 2):
		get_all_tweets(sys.argv[1])
	else:
	    print "Please add the twitter account you want to back up as an argument."
