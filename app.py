from flask import Flask, render_template, request
import datetime
from dataHandling import *

app = Flask(__name__)

def adjust_status(timer_status):
	return timer_status 

@app.route('/')
def main():
	tweets = get_tweets_list()
	tweet_contents = []
	countries = []
	country_filenames = []
	timestamps = []

	for tweet in tweets:
		tweet_contents.append(tweet['content'])
		countries.append(tweet['country'])
		timestamps.append(tweet['timestamp'])

	tweet_filenames = convert_to_filename(countries)
	for i in xrange(len(tweet_filenames)):
		tweets[i]['filename'] = tweet_filenames[i]

	speakers_list = get_gsl_list("speakers.txt")
	speakers_filenames = convert_to_filename(speakers_list)

	for i in xrange(len(speakers_list)):
		speakers_list[i] = {"country": speakers_list[i],
							"filename": speakers_filenames[i]
							}

	trending_topics = get_trending_topics()

	timer_status = get_timer_status()
	timer_status = adjust_status(timer_status)

	first_gsl = None
	first_trending = None
	first_speaker_filename = None

	if len(speakers_filenames) > 0:
		first_speaker_filename = speakers_list[0]['filename']
		speakers_filenames = speakers_list[1:]

	if len(speakers_list) > 0:
		first_gsl = speakers_list[0]['country']
		speakers_list = speakers_list[1:]

	if len(trending_topics) > 0:
		first_trending = trending_topics[0]
		trending_topics = trending_topics[1:]

	print(speakers_list)
	return render_template('index.html', tweets=reversed(tweets),
							countries=countries, timestamps=timestamps,
							gsl=speakers_list, gsl_top=first_gsl, trending=trending_topics,
							trending_top=first_trending, timer_status=timer_status,
							gsl_top_filename=first_speaker_filename, gsl_filenames=speakers_filenames,
							)

@app.route('/control')
def control():
	gsl_speakers_list = get_gsl_list("speakers.txt")
	gsl_speakers_list_total = get_gsl_list("speakers_total.txt")
	countries = get_country_list()
	trending_topics = get_trending_topics()
	tweets = get_tweets_list()

	return render_template('control.html', tweets=tweets, speakers_list=gsl_speakers_list, country_list=countries, topics=trending_topics, events=timer_events, speakers_total=gsl_speakers_list_total)

@app.route('/handle_tweet', methods=['POST'])
def handle_tweet():
	tweet = request.form['tweet_content']
	country = request.form['tweet_poster']
	current_timestamp = datetime.datetime.now()
	time_str = current_timestamp.strftime("%H:%M %d-%m-%y")

	tweets_list = get_tweets_list()

	new_tweet = {"content": tweet,
				 "country": country,
				 "timestamp": time_str,
				 "number": len(tweets_list) + 1
				}

	tweets_list.append(new_tweet)

	write_tweets_list(tweets_list)

	return render_template('success.html', action="added to", category="tweets", item_added=tweet)

@app.route('/handle_gsl_addition', methods=['POST'])
def handle_gsl_addition():
	speaker = request.form['gsl_speaker']
	speakers_list = get_gsl_list("speakers.txt")

	if speaker in speakers_list:
		return "SPEAKER ALREADY PRESENT"

	speakers_list.append(speaker)

	write_gsl_list(speakers_list, "speakers.txt")
	write_gsl_list(speakers_list, "speakers_total.txt")

	return render_template('success.html', action="added to", category="GSL", item_added=speaker)

@app.route('/handle_gsl_removal', methods=['POST'])
def handle_gsl_removal():
	print(dict(request.form))
	speaker = request.form['speaker_removed']
	speakers_list = get_gsl_list("speakers.txt")

	if speaker in speakers_list:
		speakers_list.remove(speaker)
	else:
		return render_template('fail_gsl_removal.html', speaker=speaker, gsl_list=speakers_list)

	write_gsl_list(speakers_list, "speakers.txt")

	return render_template('success.html', action="removed from", category="GSL", item_added=speaker)

@app.route('/handle_gsl_removal_total', methods=['POST'])
def handle_gsl_removal_total():
	speaker = request.form['speaker_removed_total']
	speakers_list = get_gsl_list("speakers_total.txt")

	if speaker in speakers_list:
		speakers_list.remove(speaker)
	else:
		return render_template('fail_gsl_removal.html', speaker=speaker, gsl_list=speakers_list)

	write_gsl_list(speakers_list, "speakers_total.txt")

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

@app.route('/handle_timer', methods=['POST'])
def handle_timer():
	duration = request.form['timer_time']
	event = request.form['event']

	end_time = datetime.datetime.now() + datetime.timedelta(minutes=float(duration))
	time_str = end_time.strftime("%b %d, %Y %H:%M:%S")

	payload = {"exists": True,
			   "end_time": time_str,
			   "event": event
			   }

	write_timer_status(payload)	

	return render_template('timer_success.html', duration=duration, event=event)

@app.route('/handle_timer_removal', methods=['POST'])
def handle_timer_removal():
	payload = {"exists": False,
			   "end_time": "lorem_ipsum",
			   "event": "Lorem ipsum"
			   }

	write_timer_status(payload)

	return render_template('success.html', action="removed", category="timer")

@app.route('/delete_tweets', methods=['POST'])
def delete_tweets():
	write_tweets_list([])

	return render_template('success.html', action="deleted", category='tweets')

@app.route('/handle_tweet_removal', methods=['POST'])
def handle_tweet_removal():
	tweet = request.form['tweet_removed']

	tweets = get_tweets_list()

	for item in tweets:
		if item['content'] == tweet:
			tweets.remove(item)
			write_tweets_list(tweets)
			return render_template('success.html', action="removed from", category="tweets", item_added=tweet)

	return "This should never happen"

@app.route('/modify_gsl', methods=['GET'])
def modify_gsl():
	gsl = get_gsl_list("speakers.txt")
	country_list = get_country_list()

	return render_template('modify_gsl.html', gsl=gsl, country_list=country_list)

@app.route('/modify_gsl', methods=['POST'])
def modify_gsl_post():
	form = dict(request.form)
	print(form)

	gsl = get_gsl_list("speakers.txt")

	if 'remove' in form.keys():
		speaker = form['remove'][0]
		if speaker in gsl:
			gsl.remove(str(speaker))
			write_gsl_list(gsl, 'speakers.txt')

	elif 'modify' in form.keys():
		if 'country' in form.keys():
			gsl = form['country']
			write_gsl_list(gsl, 'speakers.txt')

	elif 'add' in form.keys():
		if 'countries_list_add' in form.keys():
			gsl.append(form['countries_list_add'][0])
		else:
			gsl.append('None')
		write_gsl_list(gsl, 'speakers.txt')

	country_list = get_country_list()

	return render_template('modify_gsl.html', gsl=gsl, country_list=country_list)

if __name__ == "__main__":
	app.run(debug=True)