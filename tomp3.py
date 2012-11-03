#!/usr/bin/python
# -*- coding: utf8 -*-
################################
# Any file to Mp3 Converter    #
# @since 2012.11.03            #
# @Author dsdgun@gmail.com     #
# @Homepage blog.dsdstudio.net #
################################

import os,sys,subprocess


def isExistExtension(extarr, filename):
	try:
		idx = extarr.index(filename[filename.rfind('.'):])
		return idx != -1
	except ValueError, e:
		return False

def execute(directory, src): 
	destfile = src[0:src.rfind('.')] + '.mp3'
	destpath = os.path.join(directory, destfile)
	srcfile = os.path.join(directory, src)

	if os.path.exists(destpath): 
		print 'exist mp3 file founded [%s]' % destfile
		os.remove(destpath)
	process = subprocess.Popen([
			'ffmpeg', 
			'-i', srcfile,
			'-f', 'mp3',
			'-ab', '320k',
			'-ac', '2',
			'-ar', '44100',
			destpath
			], stdout=open(os.devnull, 'wb'))
	process.wait()


def main():
	if len(sys.argv) != 2:
		print "usage : ./tomp3.py <directory_path>"
		exit (1)
	filepath = sys.argv[1]
	fileextarr = ['.flac','.ape','.cue','.ogg']
		
	for r,d,f in os.walk(filepath):
		for files in f:
			if isExistExtension(fileextarr, files):
				execute(r, files)
				print os.path.join(r,files)

if __name__ == '__main__':
	main()
