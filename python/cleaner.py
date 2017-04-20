import csv
from datetime import datetime
from collections import defaultdict

d = {"season":0,"epnumInSeason":1,"epnum":2,"date":3,"name":4,"wikilink":5,"description":6,"types":7,"bday":8,"genres":9,"gender":10,"category":11}

host_categories = {'':'', 'Television host':'TV', 'Radio host':'Radio', 'Baseball player':'Sports', 'Film actress':'Actor', 
'Football running back':'Sports','Writer':'TV','Politician':'Politics', 'Rock band':'Music', 'Actor':'Actor', 'Swimmer':'Sports',
'Baseball Manager':'Sports', 'Activist':'Politics','Chief Executive of Forbes':'Business','Former White House Press Secretary':'Politics',
'Former Mayor of New York City':'Politics', 'Television presenter':'TV', 'Football coach':'Sports', 'Race car driver':'Sports',
'Television producer':'TV', 'Hip-hop artist':'Music', 'Mixed martial artist':'Sports', 'Television actress':'TV',
'Former United States Representative':'Politics', 'Musician':'Music','Director':'Film', 'Civil rights activist':'Politics',
'Singer-songwriter':'Music', 'Former Vice President of the United States':'Politics', 'Character actor':'Actor', 'Television personality':'TV',
'Figure skater':'Sports', 'Football quarterback':'Sports', 'Newscaster':'TV', 'Publisher':'Business', 'Singer':'Music', 'Film director':'Film',
'Former american football player':'Sports', 'Professional wrestler':'Sports', 'Businesswoman':'Business', 'Rapper':'Music', 'Professional boxer':'Sports',
'United States Senator':'Politics', 'Tennis player':'Sports', 'Television actor':'Actor','Basketball player':'Sports', 'Businessman':'Business', 
'Model':'Model', 'Stand-up comedian':'Comedy', 'Record producer':'Music', 'Social activist':'Politics', 'Television writer':'TV', 
'Professional road racing cyclist':'Sports', 'Executive':'Business', 'Media proprietor':'Business', 'Actress':'Actor', 'Football player':'Sports',
'Film actor':'Film', 'Comedian':'Comedy', '45th U.S. President':'Politics','Comedy group':'Comedy', 'Comic':'Comedy',
'Fashion Designer':'Business', 'Martial artist':'Sports', 'Ice hockey player':'Sports', 'Journalist':'Journalism'}

music_genre_counts = {'folk rock': 71, '': 5, 'indian classical': 1, 'spoken word': 1, 'jazz fusion': 11, 'ragga': 1, 'dance': 35, 'uk funky': 1, 
'minneapolis sound': 1, 'punk blues': 2, 'jam band': 8, 'soul jazz': 2, 'power pop': 20, 'g-funk': 3, 'surf rock': 5, 'dance-pop': 35, 'heavy metal': 11, 
'alternative': 3, 'cabaret': 2, 'experimental rock': 7, 'great american songbook': 1, 'alternative rock': 156, 'indie folk': 6, 'jazz poetry': 1, 
'vaudevillian': 4, 'experimental pop': 2, 'post-punk': 19, 'easy listening': 3, 'stoner rock': 1, 'jam': 5, 'ska': 8, 'reggae rock': 2, 'heartland rock': 22, 
'country pop': 8, 'indie electronic': 1, 'smooth soul': 3, 'dancehall': 4, 'boogie woogie': 1, 'west coast hip hop': 2, 'ringbang': 1, 'jazz pop': 2, 
'psychedelic pop': 2, 'piano rock': 14, 'hipster hop': 1, "children's music": 1, 'jazz': 73, 'crunk&b': 1, 'nu-funk': 1, 'quiet storm': 5, 'art pop': 26, 
'fusion': 1, 'avant-garde': 6, 'proto-punk': 3, 'tech house': 1, 'improvisational multi-genre': 2, 'funk rock': 22, 'world': 20, 'jazz rock': 4, 
'musical comedy': 1, 'urban pop': 2, 'country rock': 30, 'calypso': 1, 'electro': 1, 'mbube': 1, 'neo-folk': 2, 'post-grunge': 23, 'free jazz': 3, 
'jangle pop': 20, 'jazz blues': 3, 'latin pop': 8, 'disco': 14, 'electric blues': 4, 'art punk': 4, 'thrash metal': 1, 'psychedelic rock': 11, 'hip hop': 117,
'rock': 204, 'popular': 1, 'acoustic': 5, 'gospel': 33, 'nu-disco': 2, 'emo': 5, 'progressive metal': 1, 'east coast hip hop': 1, 'folktronica': 3,  
'post-punk revival': 12, 'classical': 15, 'glam rock': 18, 'pop rap': 2, 'electronica': 18, 'alternative country': 7, 'traditional pop': 5, 'new wave': 70, 
'a cappella': 3, 'cowpunk': 2, 'doo-wop': 1, 'blues': 64, 'dub': 1, 'progressive rock': 8, 'afro pop': 1, 'folk': 62, 'choir': 1, 'chicano rock': 2,
'alternative pop': 3, 'celtic folk': 1, 'indie rock': 47, 'proto-rap': 1, 'country blues': 4, 'grime': 1, 'film score': 2, 'hi-nrg': 1, 'observational comedy': 1,
'r&b': 175, 'outlaw country': 6, 'instrumental rock': 2, 'folk blues': 1, 'deep house': 1, 'folk punk': 1, 'improvisational comedy': 1, 'house': 5, 'celtic punk': 1, 
'ska punk': 5, 'cajun': 1, 'latin': 14, 'christian': 2, 'free funk': 1, 'pop punk': 18, 'gangsta rap': 5, 'minimalism': 1, 'ragtime': 5, 'jazz-funk': 6, 
'hip hop soul': 3, 'indie pop': 32, 'dance-punk': 5, 'anti-folk': 8, 'chamber pop': 7, 'contemporary christian': 2, 'new orleans r&b': 1, 'worldbeat': 6, 
'glam pop': 1, 'uk garage': 1, 'indietronica': 5, 'reggae fusion': 3, 'country': 68, 'indie\xc2\xa0rock': 1, 'southern hip hop': 4, 'rock and roll': 27, 
'hardcore punk': 4, 'garage rock revival': 4, 'swing': 3, 'neofolk': 1, 'folk pop': 3, 'synth-pop': 4, 'experimental': 13, 'avant-pop': 3, 'noise pop': 1, 
'alternative dance': 4, 'industrial': 1, 'trip hop': 7, 'rockabilly': 4, 'americana': 30, 'smooth jazz': 3, 'garage punk': 3, 'pop': 252, 'rocksteady': 2, 
'boogie rock': 2, 'europop': 1, 'ska-core': 1, 'avant-garde jazz': 2, '2 tone': 2, 'hard rock': 74, 'electronic': 12, 'swamp rock': 1, 'rap metal': 4, 
'latin rock': 3, 'funk metal': 9, 'jazz rap': 3, 'adult contemporary': 11, 'pop rock': 98, 'outsider': 1, 'dixieland': 1, 'future garage': 1, 'downtempo': 2, 
'nu metal': 9, 'rapcore': 3, 'psychedelic soul': 4, 'celtic fusion': 1, 'baroque pop': 14, 'nu-metal': 1, 'isicathamiya': 1, 'roots rock': 23, 'psychedelic': 1, 
'blues-rock': 1, 'country rap': 1, 'progressive pop': 2, 'tex-mex': 3, 'techno': 2, 'skate punk': 3, 'urban': 1, 'jam rock': 6, 'grunge': 21, 'dance-rock': 10, 
'freestyle': 1, 'orchestral': 1, 'pop-rap': 1, 'alternative hip hop': 19, 'vocal jazz': 2, 'honky tonk': 2, 'space music': 1, 'jazz-rock': 1, 'soft rock': 45, 
'electroclash': 1, 'folk-pop': 1, 'world music': 3, 'industrial rock': 2, 'indie hip hop': 1, '2-step garage': 1, 'funk': 41, 'pop country': 1, 'post-britpop': 6,
'acid jazz': 3, 'pub rock': 3, 'neo-psychedelia': 10, 'space rock': 2, 'acoustic hip hop': 1, 'christian metal': 1, 'acoustic rock': 4, 'soul': 113, 'vocal': 2, 
'texas blues': 2, 'brill building': 1, 'progressive bluegrass': 1, 'neo soul': 26, 'sophisti-pop': 3, 'disco-rock': 1, 'arena rock': 4, 'irish folk': 1, 'edm': 4, 
'opera': 1, 'lo-fi': 1, 'bluegrass': 12, 'chicano rap': 1, 'hardcore hip hop': 4, 'jump blues': 1, 'emo pop': 1, 'traditional irish': 1, 'ambient': 2, 'film scores': 1, 
'psychedelic funk': 2, 'philadelphia soul': 1, 'glam metal': 11, 'britpop': 1, 'zulu': 1, 'blues rock': 64, 'southern rock': 17, 'acid rock': 1, 'rap rock': 10, 
'dream pop': 7, 'afro-pop': 1, 'synthpop': 21, 'lounge': 1, 'art rock': 38, 'free improvisation': 1, 'teen pop': 2, 'alternative r&b': 5, 'comedy': 1, 
'rhythm and blues': 15, 'bebop': 1, 'reggae': 26, 'punk rock': 30, 'third wave ska': 1, 'electronic dance music': 1, 'garage rock': 9, 'maskanda': 1, 'trap': 2, 
'celtic rock': 4, 'wagnerian rock': 2, 'noise rock': 1, 'electropop': 14, 'post-hardcore': 2, 'post-bop': 2, 'comedy rock': 3, 'salsa': 1, 'psychedelia': 1, 
'avant-funk': 2, 'native american': 1, 'jazz-fusion': 1, 'southern soul': 1, 'celtic': 3, 'latin hip hop': 1, 'rock en espa\xc3\xb1ol': 3, 'alternative metal': 16, 
'college rock': 7, 'new jack swing': 7, 'catalan rumba': 1, 'chicago blues': 1, 'hip house': 1, 'blue-eyed soul': 32, 'gothic rock': 3, 'contemporary classical': 1, 
'big band': 8, 'mbaqanga': 2, 'zydeco': 2, 'show tunes': 2, 'electronic rock': 6, 'chamber rock': 1, 'parody': 1}

#with open('data/hosts2.csv', 'rb') as r, open('data/hosts3.csv', 'wb') as w:
with open('data/musical_guests2.csv', 'rb') as r, open('data/musical_guests3.csv', 'wb') as w:
	reader = csv.reader(r)
	writer = csv.writer(w)
	headers = next(reader)
	writer.writerow(headers + ["category"])
	genre_counter = defaultdict(int)
	for line in reader:
		types = line[7].split(",")
		types.remove("Thing")
		bday = line[d["bday"]]
		if bday != "":
			try:
				datetime.strptime(line[d["bday"]], "%Y-%m-%d")
			except Exception as e:
				bday = ""

		biggest_genre = ""
		genre_count = 0
		for genre in line[d["genres"]].lower().split(','):
			if genre_count < music_genre_counts[genre] and genre not in ["pop", "alternative rock","rock"]:
				biggest_genre = genre
				genre_count = music_genre_counts[genre]

		if biggest_genre == "":
			print line
		genre_counter[biggest_genre] += 1

		writer.writerow([line[0], line[1], line[2], line[3], line[4], line[5],line[6], ",".join(types), bday, line[9].lower(), line[10], biggest_genre])

	for genre, count in sorted(genre_counter.items(), key=lambda x: x[1]):
		print genre, count


