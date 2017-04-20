import numpy as np
import csv
import re
import time
import urllib
import urllib2
import json

from datetime import datetime
from collections import defaultdict
from lxml import html, etree
from bs4 import BeautifulSoup

api_key = "AIzaSyCAtXeBCz4Ts1GMawSUN83sc8XFiLMOpzM"
short_url_regex = re.compile("https:\/\/en.wikipedia.org(\/wiki\/.*)")
date_regex = re.compile(".*\((.*)\)")
format_list_regex = re.compile("(\'(?:(?=(\\?))\2.)*?\')")
start_num = -1
links = [
		"https://en.wikipedia.org/wiki/List_of_Saturday_Night_Live_episodes_(seasons_1-15)",
		"https://en.wikipedia.org/wiki/List_of_Saturday_Night_Live_episodes_(seasons_16-30)",
		"https://en.wikipedia.org/wiki/List_of_Saturday_Night_Live_episodes"
	]

def scrape_wikipedia():
	with open("data/musical_guests2.csv", "wb") as music_f, open("data/hosts2.csv", "wb") as hosts_f:
		music_w = csv.writer(music_f)
		hosts_w = csv.writer(hosts_f)

		headers = ["season","epnumInSeason","epnum", "date","name","wikilink", "description", "types", "bday", "genres", "gender"]
		music_w.writerow(headers)
		hosts_w.writerow(headers)

		name_to_link = {}
		season_num = 1
		for link in links:
			response = urllib2.urlopen(urllib2.Request(link, headers={'User-Agent': 'Mozilla'})).read()
			page_soup = BeautifulSoup(response, 'lxml')
			season_tables = page_soup.findAll("table", {"class": "wikiepisodetable"})
			for table in season_tables:
				rows = table.findAll("tr", {"class": "vevent"})
				for row in rows:
					if row.find("th"):
						episode_num = int(row.find("th").getText())
						if episode_num > start_num:
							tds = row.findAll("td")
							num_in_season = int(tds[0].getText())
							hosts = filter(lambda x: "wiki/" in x["href"], tds[1].findAll("a"))
							musical_guests = filter(lambda x: "wiki/" in x["href"], tds[2].findAll("a"))
							date = ""
							if season_num == 36 or season_num == 37:
								raw_date = tds[3].getText().split(" ")
								if len(raw_date[1]) == 2:
									raw_date[1] = "0" + raw_date[1]
								date = datetime.strptime(" ".join(raw_date), "%B %d, %Y").strftime("%Y-%m-%d")
							else:
								date = date_regex.search(tds[3].getText().replace(u"\xa0", u" ")).group(1)

							for (group, writer, td) in [(hosts, hosts_w, tds[1]), (musical_guests, music_w, tds[2])]:
								if len(group) == 0:
									name = td.getText().encode('utf-8')
									if name in name_to_link:
										person_link = name_to_link[name]
										description, types = knowledge_graph_lookup(name, person_link, episode_num)
										bday, genres, gender = parse_person_page(person_link, types)

										writer.writerow([season_num, num_in_season, episode_num, date, name, person_link, description, ",".join(types), bday, ",".join(genres), gender])

									else:
										print episode_num, season_num
								else:
									for person in group:
										name = person.getText().encode('utf-8')
										person_link = person["href"]
										if name in name_to_link:
											if person_link != name_to_link[name]:
												redirected_url = urllib2.urlopen(urllib2.Request("http://www.wikipedia.com"+person_link, headers={'User-Agent': 'Mozilla'})).geturl()
												person_link = short_url_regex.search(redirected_url).group(1)

										name_to_link[name] = person_link
										description, types = knowledge_graph_lookup(name, person_link, episode_num)
										bday, genres, gender = parse_person_page(person_link, types)
										#print episode_num, name, gender
										writer.writerow([season_num, num_in_season, episode_num, date, name, person_link, description, ",".join(types), bday, ",".join(genres), gender])

				season_num += 1


def knowledge_graph_lookup(name, wiki_link, epnum):
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
		'query': name,
		'limit': 1,
		'indent': True,
		'key': api_key,
	}
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	element = response['itemListElement'][0]
	types = map(lambda x: x.encode('utf-8'), element['result']['@type'])
	description = ''
	if 'description' in element['result']:
		description = element['result']['description']
	link = element['result']['detailedDescription']['url']
	if link.split("/")[-1] != wiki_link.split("/")[-1]:
		print epnum, name, wiki_link, link
	return description, types

def parse_person_page(link, types):
	bday = ""
	genres = []
	gender = ""

	response = urllib2.urlopen(urllib2.Request("http://www.wikipedia.com"+link, headers={'User-Agent': 'Mozilla'})).read()
	page_soup = BeautifulSoup(response, 'lxml')

	table = page_soup.find("table", {"class": "infobox"})
	if table:
		rows = table.findAll("tr")
		for row in rows:
			header = row.find("th")
			if header and header.getText() == "Genres":
				genres = map(lambda x: x.getText().encode('utf-8'), filter(lambda x: "wiki/" in x["href"], row.find("td").findAll("a")))

	if page_soup.find("span", {"class": "bday"}):
		bday_span = page_soup.find("span", {"class": "bday"})
		if bday_span:
			bday = bday_span.getText()

	if "Person" in types:
		all_text = " ".join(map(lambda x: x.getText(), page_soup.findAll("p"))).lower()
		num_he = all_text.count(" he ")
		num_she = all_text.count(" she ")
		if num_he > num_she:
			gender = "Male"
		else:
			gender = "Female"

		# if np.absolute(num_he - num_she) < 10:
		# 	print "~~~~~~~~~~~~~~~Might want to check this one:::"

	return bday, genres, gender

if __name__ == "__main__":
	start_time = time.time()
	scrape_wikipedia()
	print("--- %s seconds ---" % (time.time() - start_time))
