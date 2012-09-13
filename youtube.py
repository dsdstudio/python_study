#!/usr/bin/python
# -*- coding: utf8 -*-
################################
# Youtube Data Grabber         #
# @since 2012.09.08            #
# @Author dsdgun@gmail.com     #
# @Homepage blog.dsdstudio.net #
################################

import fileinput
import re
import sys
import string
import urllib
import urllib2

class YoutubeURLOpener(urllib.FancyURLopener):
	version = 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'

urllib._urlopener = YoutubeURLOpener()

if len(sys.argv) == 1:
	print "인자를 입력해주십셔 : youtube.py <watch_url>"
	exit (1)
target_url = sys.argv[1]
print target_url

req = urllib2.Request(target_url)
try: 
	urllinebyline = urllib2.urlopen(req)
except URLError, e:
	print e.reason
	exit(1)


# 퀄리티 코드 dict + array 로 구성하였다 
# TODO 아직 못구한 코드에 대한정보 수집 필요 
quality_dict = {
	13:['3gp','Low Quality'],
	17:['3gp','Medium Quality'],
	36:['3gp','High Quality'],
	34:['flv','320p'],
	35:['flv','480p'],
	18:['mp4','480p'],
	22:['mp4','720p'],
	37:['mp4','1080p']
}


for line in urllinebyline:
	if  line.strip() == "" or string.find(line,'itag') == -1:
		continue
	m = re.findall('stream_map=(.[^&]*)', line)

	if len(m) > 0:
		fmt_url = urllib.unquote(m[0])
		''' 직접입력일때만 이 로직이 필요하다 urlopen으로 데이터를 가져오면 한번 escaping이 일어나서 특수 unicode 문자열은 따로 처리해주지않아도 된다. '''
		''' m = re.findall('^(.*?)\\\\u0026',fmt_url); '''
		urls = fmt_url.split(',')
		for url in urls:
			realurl_tup = re.findall('url=(.*?)&.*?itag=([0-9]+)', url);
			if len(realurl_tup) > 0:
				try:
					print quality_dict[int(realurl_tup[0][1])]
					print urllib.unquote(realurl_tup[0][0])
				except:
					print '찾을수 없는 타입입니다' + realurl_tup[0][1]

		''' 파일 저장 매커니즘 정리 필요 '''
		'''
		if len(urls) > 0:
			realurl_tup = re.findall('url=(.*?)&.*?itag=([0-9]+)', urls[1]);
			if len(realurl_tup) > 0:
				wfile = urllib.urlopen(urllib.unquote(realurl_tup[0][0]));
				lfile = open('t.mp4','w');
				lfile.write(wfile.read());
				wfile.close()
				lfile.close()
		'''
exit(0)

