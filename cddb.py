#!/usr/bin/python
# cddb.py - maintain a flat-file database, allowing users to query, delete an entry, create an entry.
#Author - Kaveri Krishnaraj

import collections
import sys
import re
import os
#import argparse
from optparse import OptionParser


class CD() :


	def _init_(self) :
		self.album = ""
		self.date = ""
		self.songs = list()

	def setAlbum(self, album) :
		self.album = album
	
	def getAlbum(self) :
		return self.album

	def setdate(self, date) :
		self.date = date
	
	def getdate(self) :
		return self.date
	
	def setSong(self, song) :
			self.songs.append(song)

	def getSong(self) :
		return self.songs
	
db = {}

def listAlbum(option, opt_str, value, parser) :

	
	file = os.getenv("CDDB")
	f = open(file, 'r')
	artist = " "
	artistPattern = re.compile('^[a-zA-Z]') 
	datePattern = re.compile('^[0-9]') 
	songPattern = re.compile('^-') 
	cd = CD()
	for line in f :
		if line == "\n" and artist != " " :
				db[artist] = [cd]
		 		cd = CD()
		 		artist = " "
		elif artistPattern.match(line) :
			artist = line.strip('\n')
		elif datePattern.match(line) :
			line = line.split()
			cd.setdate(line.pop(0))
			str = " "
			cd.setAlbum(str.join(line))
			
		elif songPattern.match(line) :
			song = line.strip('-\n')
			
			cd.setSong(song)
		
	if artist != " ":
				db[artist] = [cd]
	
	artistList()	

def artistList() :

	count = 1
	for key in sorted(db.keys()) :
		print count, key
		count = count + 1
	reply_artist = raw_input("Choose an artist by entering the number or quit by entering a q")
	if reply_artist != 'q' :
		albumList(reply_artist)
		
def albumList(reply_artist) :

	reply_artist = int(reply_artist) - 1
	alist =  sorted(db.keys())
	count = 1
	cd = CD()
	album = db[alist[reply_artist]]

	for cd in album :
		print count, cd.getdate(), " ", cd.getAlbum()
		count = count + 1
	reply_album = raw_input("Choose an album by entering the number or enter a to return to artist")
	
	if reply_album != 'a' :
		reply_album = int(reply_album) - 1
		count1 = 1
		x = album[reply_album]
		for song in x.getSong() :
			print count1 , song
			count1 = count1 + 1
					
	else :
		artistList()
		

def main( args ) :
	
	parser = OptionParser()
	parser.add_option("-l", "--list" , action="callback", callback=listAlbum, help="List Albums. Must be given alone")

	if len( args ) < 2 :
		parser.print_help()
		sys.exit()	

	(options, args) = parser.parse_args()


if __name__ == "__main__":
		sys.exit(main( sys.argv ))
	
