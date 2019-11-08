#!/usr/bin/env python3

# This script will take a Discogs release identifier and gather track data from Discogs to 
# generate a Label track text file for Audacity. Post recording of vinyl record, one can
# import the label track text file to get the tracks labeled and the markers close to where
# they should be.

# Written by Karl Abbott <karl1@99b.org>
# Licensed under the GPL version 3.

import sys,subprocess,json,urllib.parse,datetime

discogs_token="<YOUR ACCESS TOKEN>"

def xml_scrub(textin):
	newtext=""
	for line in textin.split("\n"):
		start=line.find('<')
		end=line.find('>')
		if start>-1 and end>-1:
			url=line[start+1:end]
			line=line.replace('<'+url+'>','['+url+']('+url+')')
		line=line.replace('<','&lt;')
		line=line.replace('>','&gt;')
		line=line.replace('&','&amp;')
		newtext=newtext+line
	return newtext



music_id=sys.argv[1:][0]
release_id=urllib.parse.quote(music_id,safe='')

# grab the id and then query the release....
myrelease=subprocess.getoutput('curl -s "https://api.discogs.com/releases/'+str(release_id)+'" -H "Authorization: Discogs token='+discogs_token+'"')
myrelease_json=json.loads(myrelease)
x=0
for genre in myrelease_json["genres"]:
	if x==0:
		my_genre=genre
	x=x+1
x=0
for artist in myrelease_json["artists"]:
	if x==0:
		artist_name=artist["name"]
	x=x+1


print("Writing out "+str(music_id)+"-tags.xml for importing into metadata.")
tags_out=open(music_id+"-tags.xml","w")
tags_out.write("<tags>\n")
tags_out.write('\t<tag name="GENRE" value="'+xml_scrub(my_genre)+'"/>\n')
tags_out.write('\t<tag name="YEAR" value="'+xml_scrub(myrelease_json["released"])+'"/>\n')
tags_out.write('\t<tag name="ARTIST" value="'+xml_scrub(artist_name)+'"/>\n')
tags_out.write('\t<tag name="ALBUM" value="'+xml_scrub(myrelease_json["title"])+'"/>\n')
tags_out.write("</tags>\n")
tags_out.close()

# Parse the track list.
tracklist=myrelease_json['tracklist']
track_counter=datetime.timedelta(hours=0,minutes=0,seconds=0)
# These two lines format the counter the way that audacity needs it
# May need to not do time but do everything as a datetime...
track_counter_float=float(track_counter.total_seconds())
tcstring=str(f'{track_counter_float:.6f}')

print("Writing out "+str(music_id)+".txt for importing as a label track.")
lf=open(str(music_id)+".txt","w")

# Let's generate the label file now..
for track in tracklist:
	lf.write(tcstring+"\t"+tcstring+"\t"+track["title"]+"\n")
	duration=datetime.datetime.strptime(track["duration"],"%M:%S").time()
	track_counter_increment=datetime.timedelta(hours=duration.hour,minutes=duration.minute,seconds=duration.second)
	track_counter=track_counter+track_counter_increment
	track_counter_float=float(track_counter.total_seconds())
	tcstring=str(f'{track_counter_float:.6f}')

lf.close()
