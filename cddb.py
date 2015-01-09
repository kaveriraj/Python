#!/usr/bin/python
# cddb.py - maintain a flat-file database, allowing users to query, delete an entry, create an entry.
# author: Stephen W. Slaughter
# 3/22/13

import sys
import os
import re
from optparse import OptionParser
import collections

class Album :  #data structure for Album info storage

  
	def _init_(self) :
 		self.releaseDate = ""
		self.name = ""
		self.tracks = []
	
	def getReleaseDate(self) :
		return self.releaseDate

	def getName(self) :
		return self.name
	
	def getTracks(self) :
		return self.tracks
   
	def setReleaseDate(self, releaseDate) :
		self.releaseDate = releaseDate
	
	def setName(self, name) :
		self.name = name
	
	def setTrack(self, track) :
		try:
			self.tracks.append(track)
		except AttributeError :
			self.tracks = [track]

db = {}  #the DB dictionary

def readDB() :  # read the DB info from file into the dictionary
	
	global db
	file = os.getenv("CDDB")
	f = open(file, 'r')
	x = Album()
	artist = ""
	artistPat = re.compile('^[a-zA-Z]') #artist name pattern
	releaseDatePat = re.compile('^[0-9]') #release date pattern
	trackPat = re.compile('^-') #track pattern
	match = False
	for line in f :
		if line == "\n" and artist != "" : #in case of blank lines and full variables, store info in dictionary
			if db.has_key(artist) :
				for album in db[artist] :
					if album.getName() == x.getName() and album.getReleaseDate() == x.getReleaseDate():
						match = True
					if match == False :
						db[artist].append(x)
			else :
				db[artist] = [x]
			x = Album()
			artist = ""
		elif artistPat.match(line) :
			artist = line.strip('\n')
		elif releaseDatePat.match(line) :
			line = line.split()
			x.setReleaseDate(line.pop(0))
			x.setName(' '.join(line))
		elif trackPat.match(line) :
			track = line.strip('-\n')
			x.setTrack(track)
	
	if artist != "" : #in case of remaining object, store in dictionary
		try: 
			db[artist].append(x)
		except KeyError:
			db[artist] = [x]

def listAlbum(option, opt_str, value, parser) : 
	readDB()
	artistMenu()

def artistMenu() :
	global db
	c = 1
	for key in sorted(db.keys(), key=str.lower) :
		print "(", c, ") ", key
		c+=1
	answer = raw_input("Enter the number of the artist or 'q' to quit:  ")
	if answer == 'q':
		sys.exit()
	else:
		answer = int(answer) - 1
		artist_list = sorted(db.keys(), key=str.lower)
		albumMenu(artist_list, answer)

def albumMenu(artist_list, answer) :
	global db
	c = 1
	answer = int(answer)
	for album in db[artist_list[answer]] :
		print "(", c, ") ", album.getReleaseDate(), " ", album.getName()
		c+=1		
	answer2 = raw_input("Enter the number of the album or 'a' to return to the artist menu:  ")
	if answer2 == 'a' :
		artistMenu()
	else:
		answer2 = int(answer2) - 1
		album_list = db[artist_list[answer]]
		songMenu(artist_list, answer, album_list, answer2)

def songMenu(artist_list, answer, album_list, answer2) :
	global db
	album = album_list[answer2]
	c = 1
	for track in album.getTracks() :
		print "(", c, ") ", track
		c+=1
	answer3 = raw_input("Enter 'a' to return to the albumMenu:  ")
	if answer3 == 'a' :
		albumMenu(artist_list, answer) 
			      
def deleteAlbum(option, opt_str, value, parser) : #due date: Saturday March 20
	readDB()
	deleteArtistMenu()

def deleteArtistMenu() :
	global db
	c = 1
	if db.keys() == [] :
		print ("The Database is empty. Now updating DB and quitting....")
		updateDB()
		sys.exit()
	for key in sorted(db.keys(), key=str.lower) :
		print "(", c, ") ", key
		c+=1
	answer = raw_input("Enter the number of the artist or 'q' to quit:  ")
	if answer == 'q':
		updateDB()
		sys.exit()
	else:
		answer = int(answer) - 1
		artist_list = sorted(db.keys(), key=str.lower)
		deleteAlbumMenu(artist_list, answer)

def deleteAlbumMenu(artist_list, answer) :
	global db
	c = 1
	answer = int(answer)

	for album in db[artist_list[answer]] :
		print "(", c, ") ", album.getReleaseDate(), " ", album.getName()
		c+=1
	answer2 = raw_input("Enter the number of the album to delete or 'a' to return to the artist menu:  ")
	if answer2 == 'a' :
		deleteArtistMenu()
	else:
		answer2 = int(answer2) - 1
		album_list = db[artist_list[answer]]
		del db[artist_list[answer]][answer2]
		if db[artist_list[answer]] == [] :
			del db[artist_list[answer]]
			answer3 = raw_input("Enter 'a' to return to the artist menu or 'q' to quit")
			if answer3 == 'a' :
				deleteArtistMenu()
			else :
				updateDB()
				sys.exit()
		else :
			answer4 = raw_input("Enter 'a' to return to the album menu or 'q' to quit")
	if answer4 == 'a' :
		deleteAlbumMenu(artist_list, answer)
	else :
		updateDB()
		sys.exit() 
      
def addAlbum(option, opt_str, value, parser) : 
	global db
	more = 'a'
   
	readDB()

	while more == 'a' :
		tracks = []
		x = Album()
		match = False
		artist = raw_input("\nEnter the artist name:  ")
		album_name = raw_input("\nEnter the album name:  ")
		releaseDate = raw_input("\nEnter the release date:  ")
		end = 'a'
		while (end == 'a') :
			tracks.append(raw_input("Enter track title:  "))
			end = raw_input("Enter 'a' to add another track or 'q' to quit:  ")
			if end == 'q' : 
				x.setReleaseDate(releaseDate)
				x.setName(album_name)
				for track in tracks :
					x.setTrack(track)
				if db.has_key(artist) :
					for album in db[artist] :
						if album.getName() == x.getName() and album.getReleaseDate() == x.getReleaseDate():
							match = True
							print "\nERROR: THIS ALBUM ALREADY EXISTS IN THE DB!"
					if match == False :	
						db[artist].append(x)
				else :
					db[artist] = [x]
		more = raw_input("\nEnter 'a' to add another album or 'q' to quit:  ")
		if more == 'q' :
			updateDB()
			return	
		updateDB()

def updateDB() : #update the database file with the dictionary (db) in memory
	global db
	f = open('tempfile', 'w')
	artists = db.keys()

	for artist in artists :
		for album in db[artist] :
			f.write(artist + '\n')
			value = album.getReleaseDate() + " " + album.getName() + '\n'
			value = str(value)
			f.write(value)
			tracks = album.getTracks()
			for track in tracks :
				f.write('-'+ track + '\n')
			f.write('\n')
	f.close()
	os.system("mv tempfile $CDDB")
			
def main( args ) :
	
	parser = OptionParser() 	#command-line options parser
	parser.add_option("-l", "--list" , action="callback", callback=listAlbum, help="List Albums. Must be given alone")
	parser.add_option("-d", "--delete", action="callback", callback=deleteAlbum, help="Delete Album(s). Must be given alone")
	parser.add_option("-a", "--add", action="callback", callback=addAlbum, help="Add Album(s). Must be given alone")

	if len( args ) < 2 : #in case of zero options
		parser.print_help()
		sys.exit()
	
	(options, args) = parser.parse_args() #parse the command-line args and delegate control


if __name__ == '__main__' :
		sys.exit( main( sys.argv ))
