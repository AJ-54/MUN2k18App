import os
import pickle

country_matrix_filename = "countries_unga.txt"

def get_tweets_list():
	abs_file_path = os.getcwd()
	rel_file_path = "data/tweets.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)

	tweets_list = []
	with open(total_file_path, "r") as tweet_file:
		try:
			tweets_list = pickle.load(tweet_file)
		except EOFError:
			pass

	return tweets_list

def write_tweets_list(tweets_list):
	abs_file_path = os.getcwd()
	rel_file_path = "data/tweets.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)

	with open(total_file_path, "w") as tweet_file:
		pickle.dump(tweets_list, tweet_file)

	return

def get_country_list():
	abs_file_path = os.getcwd()
	rel_file_path = "data/%s" %(country_matrix_filename)
	total_file_path = os.path.join(abs_file_path, rel_file_path)
	with open(total_file_path, 'r') as countries_file:
		countries_list = countries_file.readlines()
		for i in xrange(len(countries_list)):
			countries_list[i] = countries_list[i].strip()
	return countries_list

def get_gsl_list():
	abs_file_path = os.getcwd()
	rel_file_path = "data/speakers.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)
	speakers_list = []
	with open(total_file_path, "r") as gsl_file:
		try:
			speakers_list = pickle.load(gsl_file)
		except EOFError:
			pass

	return speakers_list

def write_gsl_list(speakers_list):
	abs_file_path = os.getcwd()
	rel_file_path = "data/speakers.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)
	with open(total_file_path, 'w') as speakers_file:
		pickle.dump(speakers_list, speakers_file)

def get_trending_topics():
	abs_file_path = os.getcwd()
	rel_file_path = "data/trending.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)

	trending = []

	with open(total_file_path, 'r') as trending_file:
		try:
			trending = pickle.load(trending_file)
		except EOFError:
			pass

	return trending

def write_trending_topics(topics):
	abs_file_path = os.getcwd()
	rel_file_path = "data/trending.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)

	with open(total_file_path, 'w') as trending_file:
		pickle.dump(topics, trending_file)

	return

def get_timer_status():
	abs_file_path = os.getcwd()
	rel_file_path = "data/timer.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)

	timer_status = None

	with open(total_file_path, 'r') as timer_file:
		try:
			timer_status = pickle.load(timer_file)
		except EOFError:
			pass

	return timer_status

def write_timer_status(payload):
	abs_file_path = os.getcwd()
	rel_file_path = "data/timer.txt"
	total_file_path = os.path.join(abs_file_path, rel_file_path)

	with open(total_file_path, "w") as timer_file:
		pickle.dump(payload, timer_file)

	return