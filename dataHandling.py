import os
import pickle

timer_events = ["Unmoderated Caucus", 
				"Moderated Caucus", 
				"Conference", 
				"Current Session",
				"Lunch Break"]

country_matrix_filename = "const_loksabha.txt"
country_to_filename = {"Electronic Frontier Foundation":"eff",
					   "Democratic Republic of Congo":"Democratic-Republic-of-the-Congo",
					   "Human Rights Watch":"hrw",
					   "Dominican Republic":"Dominican-Republic",
					   "Democratic People's Republic of Korea": "North-Korea",
					   "DPRK":"North-Korea",
					   "Republic of Korea":"South-Korea",
					   "Russian Federation":"Russia",
					   "Amnesty International":"amnesty",
					   "Burkina Faso":"Burkina-Faso",
					   "South Africa":"South-Africa",
					   "Saudi Arabia":"Saudi-Arabia",
					   "South Korea":"South-Korea",
					   "North Korea":"North-Korea",
					   "UAE":"United Arab Emirates",
					   "New Zealand":"New-Zealand",
					   "United Kingdom":"United-Kingdom",
					   "United States of America":"United-States",
					   "Antigua and Barbuda":"Antigua-and-Barbuda",
					   "Trinidad and Tobago":"Trinidad-and-Tobago",
					   "European Union":"European-Union",
					   "Marshall Islands":"Marshall-Islands",
					   "Sri Lanka":"Sri-Lanka",
					   "International Press":"IP",
					   "Aleut International Association":"aleut",
					   "Arctic Athabaskan Council":"arctic_atha",
					   "Inuit Circumpolar Council":"inuit",
					   "Gwich'in Council International":"gwich",
					   "Russian Association of Indegenous peoples of the North (RAIPON)":"raipon",
					   "Saami Council":"saami",
					   "World Wildlife Fund":"wwf",
					   "International Labor Organization":"ilo",
					   "UAE":"United-Arab-Emirates",
					   "United Arab Emirates":"United-Arab-Emirates",
					   "Sierra Leone":"Sierra-Leone",
					   "DPRK(North Korea)":"North-Korea",
					   "South Sudan":"South-Sudan",
					   "Czech Republic":"Czech-Republic",
					   "Bosnia and Herzegovina":"Bosnia-and-Herzegovina",
					   "Scottish Fair Trade Forum":"scottish-fair-trade-forum",
					   "Consular Association of Northern Ireland":"ca-ni",
					   }

party_status = {"AITC":['Balurghat (West Bengal)', 'Bangaon (SC)(West Bengal)', 'Howrah (West Bengal)'],
				"AIADMK":['Chennai Central (Tamilnadu)', 'Chennai South (Tamilnadu)', 'Coimbatore (Tamilnadu)', 'Salem (Tamilnadu)', 'Tenkasi (Tamilnadu)', 'Vellore (Tamilnadu)', 'Tiruvannamalai (Tamilnadu)', 'Ramanathapuram(Tamilnadu)', 'Erode(Tamilnadu)', 'Chennai North(Tamilnadu)', 'Madurai(Tamilnadu)', 'Namakkal(Tamilnadu)'],
				"BJP":['Agra (Uttar Pradesh)', 'Ahmedabad East (Gujarat)', 'Aligarh (Uttar Pradesh)', 'Andaman and Nicobar Islands (Andaman and Nicobar Islands)', 'Arunachal West (Arunachal Pradesh)', 'Bareilly (Uttar Pradesh)', 'Beed (Maharashtra)', 'Chandigarh (Chandigarh)', 'Dadra and Nagar Haveli (ST)(Dadra and Nagar Haveli)', 'Dibrugarh (Assam)', 'Gandhinagar (Gujarat)', 'Gwalior (Madhya Pradesh)', 'Jamshedpur (Jharkhand)', 'Janjgir-Champa (SC)(Chhattisgarh)', 'Lucknow (Uttar Pradesh)', 'Mathura (Uttar Pradesh)', 'Meerut (Uttar Pradesh)', 'North East Delhi (NCT of Delhi)', 'Pilibhit (Uttar Pradesh)', 'Pune (Maharashtra)', 'Ranchi (Jharkhand)', 'Tezpur (Assam)', 'Ujjain (SC)(Madhya Pradesh)', 'Kanpur (Uttar Pradesh)'],
				"INC":['Alappuzha (Kerala)', 'Amethi (Uttar Pradesh)', 'Autonomous District (ST)(Assam)', 'Gulbarga (Karnataka)', 'Inner Manipur (Manipur)', 'Jalandhar (Punjab)', 'Kaliabor (Assam)', 'Kishanganj (Bihar)', 'Ludhiana (Punjab)', 'Rae Bareli (Uttar Pradesh)', 'Thiruvananthapuram (Kerala)'],
				"Independent":"Kokrajhar (Assam)",
				}

home_dir = os.getcwd()
current_data_dir = os.path.join(home_dir, "data/current/")
static_data_dir = os.path.join(home_dir, "data/static/")


def convert_constituency(constituency):
	for party in party_status.keys():
		if constituency in party_status[party]:
			return party

def search_constituency(constituency):
	for a in party_status.keys():
		if constituency in party_status[a]:
			return True

	return False

def convert_to_filename(country_names):
	filenames_final = []

	try:
		if search_constituency(country_names[0]):
			# LOK SABHA
			for constituency in country_names:
				filenames_final.append(convert_constituency(constituency))

			return filenames_final

	except:
		return filenames_final

	for country_name in country_names:
		if country_name in country_to_filename.keys():
			filenames_final.append(country_to_filename[country_name])
		else:
			filenames_final.append(country_name)

	return filenames_final

def get_tweets_list():
	tweets_file_path = os.path.join(current_data_dir, "tweets.txt")

	tweets_list = []
	with open(tweets_file_path, "r") as tweet_file:
		try:
			tweets_list = pickle.load(tweet_file)
		except EOFError:
			pass

	return tweets_list

def write_tweets_list(tweets_list):
	tweets_file_path = os.path.join(current_data_dir, "tweets.txt")

	with open(tweets_file_path, "w") as tweet_file:
		pickle.dump(tweets_list, tweet_file)

	return

def get_country_list():
	country_matrix_file_path = os.path.join(static_data_dir, country_matrix_filename)

	with open(country_matrix_file_path, 'r') as countries_file:
		countries_list = countries_file.readlines()
		for i in xrange(len(countries_list)):
			countries_list[i] = unicode(countries_list[i].strip(), 'utf-8')
	return countries_list

def get_gsl_list(filename):
	gsl_file_path = os.path.join(current_data_dir, filename)

	speakers_list = []
	with open(gsl_file_path, "r") as gsl_file:
		try:
			speakers_list = pickle.load(gsl_file)
		except EOFError:
			pass

	return speakers_list

def write_gsl_list(speakers_list, filename):
	gsl_file_path = os.path.join(current_data_dir, filename)

	with open(gsl_file_path, 'w') as speakers_file:
		pickle.dump(speakers_list, speakers_file)

def get_trending_topics():
	trending_file_path = os.path.join(current_data_dir, "trending.txt")

	trending = []

	with open(trending_file_path, 'r') as trending_file:
		try:
			trending = pickle.load(trending_file)
		except EOFError:
			pass

	return trending

def write_trending_topics(topics):
	trending_file_path = os.path.join(current_data_dir, "trending.txt")

	with open(trending_file_path, 'w') as trending_file:
		pickle.dump(topics, trending_file)

	return

def get_timer_status():
	timer_file_path = os.path.join(current_data_dir, "timer.txt")

	timer_status = None

	with open(timer_file_path, 'r') as timer_file:
		try:
			timer_status = pickle.load(timer_file)
		except EOFError:
			pass

	return timer_status

def write_timer_status(payload):
	timer_file_path = os.path.join(current_data_dir, "timer.txt")

	with open(timer_file_path, "w") as timer_file:
		pickle.dump(payload, timer_file)

	return
