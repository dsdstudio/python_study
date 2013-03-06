#!/usr/bin/python
# -*- coding: utf8 -*-

import os,sys,time
from datetime import date

def __log(s):
	print s

def main():
	if len(sys.argv) != 3:
		__log("usage : ./classfi.py <source_dir> <target_dir>")
		exit (1)
	sourcedir = sys.argv[1]
	targetdir = sys.argv[2]

	if not os.path.exists(targetdir):
		__log("target directory does not exist ! ["+targetdir+"]")
		exit(1)

	for r,d,f in os.walk(sourcedir):
		for files in f:
			fileAbsolutePath = os.path.join(r,files);
			filestat = os.stat(fileAbsolutePath)
			modifytime = date.fromtimestamp(filestat.st_mtime)
			if not os.path.exists(os.path.join(targetdir, modifytime.isoformat())):
				os.makedirs(os.path.join(targetdir, modifytime.isoformat()))
			os.rename(fileAbsolutePath,os.path.join(os.path.join(targetdir,modifytime.isoformat()),files))

if __name__ == "__main__":
	main()
