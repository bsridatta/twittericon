import json
import time

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from PyFiles import sentiment_mod as s

#consumer key, consumer secret, access token, access secret.
ckey="gCeMwFwN1u3bo9CzaXc0zduAS"
csecret="X8TaFLsZuonYPxu34jmqytZsRaf1IfA2lbU0HEnb8iBjxRSkTN"
atoken="353491492-LmBWiM4m0W68Sy3BQwv4NKgYSNbNtIdmo9iWQ3ZD"
asecret="w1G4BW3qfXmQ90MLv37jgPoLoXTBV0ryqQZ38zIgGdxhj"

class listener(StreamListener):

	def __init__(self, time_limit=200):
		self.start_time = time.time()
		self.limit = time_limit
		super(listener, self).__init__()


	def on_data(self, data):
		if (time.time() - self.start_time) < self.limit:
			all_data = json.loads(data)
			tweet = all_data["text"]
			sentiment_value, confidence = s.sentiment(tweet)
			print(tweet, sentiment_value, confidence)
			if confidence * 100 >= 80:
				output = open("twitter-out.txt", "a")
				output.write(sentiment_value)
				output.write('\n')
				output.close()
			else:
				return False
			# defde
			return True

		else:
			return False


	def on_error(self, status):
		print(status)




def stream(para):
	print "parameter -"+para
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=[para])