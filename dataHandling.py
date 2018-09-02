import os
import pickle

country_matrix_filename = "countries_unhrc_2018_workshop.txt"
country_to_filename = {"Democratic Republic of Congo":"Democratic-Republic-of-the-Congo",
					   "Dominican Republic":"Dominican-Republic",
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
					   }

party_status = {"Aam_Aadmi_Party":["Patiala (Punjab)"],
				"All_India_Trinamool_Congress":["Jadavpur (West Bengal)", "Balurghat (West Bengal)"],
				"AIUDF":["Barpeta (Assam)", "Karimganj (SC)(Assam)"],
				"Apna_Dal":["Mirzapur (Uttar Pradesh)"],
				"Bharatiya_Janata_Party":["Ahmedabad East (Gujarat)", "Arunachal West (Arunachal Pradesh)","Bangalore Central (Karnataka)","Beed (Maharashtra)","Chandigarh (Chandigarh)","Dibrugarh (Assam)","Gandhinagar (Gujarat)","Gauhati (Assam)","Hardwar (Uttarakhand)","Indore (Madhya Pradesh)","Jaipur (Rajasthan)","Jamnagar (Gujarat)","Jorhat (Assam)","Mathura (Uttar Pradesh)","New Delhi (NCT of Delhi)","Patna Sahib (Bihar)","Shimoga (Karnataka)","Tezpur (Assam)","Vadodara (Gujarat)","Vidisha (Madhya Pradesh)"],
				"Biju_Janata_Dal":["Balasore","Puri (Odisha)"],
				"Indian_National_Congress":["Alappuzha (Kerala)","Amritsar (Punjab)","Arunachal East (Arunachal Pradesh)","Gulbarga (Karnataka)","Guna (Madhya Pradesh)","Inner Manipur (Manipur)","Jangipur (West Bengal)","Kishanganj (Bihar)","Rohtak (Haryana)","Silchar (Assam)","Thiruvananthapuram (Kerala)"],
				"RSP":["Kollam (Kerala)"]
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
