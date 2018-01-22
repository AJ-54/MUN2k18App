from flask import Flask, render_template, request
import datetime
from dataHandling import *

app = Flask(__name__)

@app.route('/')
def main():
	tweets = get_tweets_list()
	tweet_contents = []
	countries = []
	timestamps = []

	for tweet in tweets:
		tweet_contents.append(tweet['content'])
		countries.append(tweet['country'])
		timestamps.append(tweet['timestamp'])


	speakers_list = get_gsl_list()

	trending_topics = get_trending_topics()

	return render_template('index.html', tweets=tweets, countries=countries, timestamps=timestamps, gsl=speakers_list, trending=trending_topics)

@app.route('/control')
def control():
	tweet = ""
	gsl_speakers_list = get_gsl_list()
	countries = get_country_list()
	trending_topics = get_trending_topics()

	return render_template('control.html', tweet=tweet, speakers_list=gsl_speakers_list, country_list=countries, topics=trending_topics)

@app.route('/handle_tweet', methods=['POST'])
def handle_tweet():
	tweet = request.form['tweet_content']
	country = request.form['tweet_poster']
	current_timestamp = datetime.datetime.now()
	time_str = current_timestamp.strftime("%d-%m-%y %H:%M")

	new_tweet = {"content": tweet,
				 "country": country,
				 "timestamp": time_str
				}

	tweets_list = get_tweets_list()
	tweets_list.append(new_tweet)

	write_tweets_list(tweets_list)

	return render_template('success.html', action="added to", category="tweets", item_added=tweet)

@app.route('/handle_gsl_addition', methods=['POST'])
def handle_gsl_addition():
	speaker = request.form['speaker']
	speakers_list = get_gsl_list()

	if speaker in speakers_list:
		return "SPEAKER ALREADY PRESENT"

	speakers_list.append(speaker)

	write_gsl_list(speakers_list)

	return render_template('success.html', action="added to", category="GSL", item_added=speaker)

@app.route('/handle_gsl_removal', methods=['POST'])
def handle_gsl_removal():
	speaker = request.form['speaker_removed']
	speakers_list = get_gsl_list()

	if speaker in speakers_list:
		speakers_list.remove(speaker)
	else:
		return render_template('fail_gsl_removal.html', speaker=speaker, gsl_list=speakers_list)

	write_gsl_list(speakers_list)

	return render_template('success.html', action="removed from", category="GSL", item_added=speaker)

@app.route('/handle_trending_addition', methods=['POST'])
def handle_trending_addition():
	topic = request.form['topic']

	topics_list = get_trending_topics()
	topics_list.append(topic)

	write_trending_topics(topics_list)

	return render_template('success.html', action="added to", category="trending", item_added=topic)

@app.route('/handle_trending_removal', methods=['POST'])
def handle_trending_removal():
	topic = request.form['trending_removed']

	topics_list = get_trending_topics()
	if topic in topics_list:
		topics_list.remove(topic)
	else:
		return "FAILED TO REMOVE TOPIC, IT'S NOT IN THE LIST"

	write_trending_topics(topics_list)

	return render_template('success.html', action="removed from", category="trending", item_added=topic)

if __name__ == "__main__":
	app.run(debug=True)