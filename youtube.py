#!/usr/bin/python
# -*- coding: utf8 -*-
################################
# Youtube Movie Grabber        #
# @since 2012.09.08            #
# @Author dsdgun@gmail.com     #
# @Homepage blog.dsdstudio.net #
################################

import re, sys, string, fileinput, urllib, urllib2, logging
from urlparse import parse_qs

class YoutubeURLOpener(urllib.FancyURLopener):
	version = 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'

''' 퀄리티 코드 dict + array 로 구성하였다 '''
''' TODO 아직 못구한 코드에 대한정보 수집 필요 '''
quality_dict = {
	5:{
		   'format':'_',
		   'quality':'240x400',
		   'dimension': '240x400',
		   'order':99
	   },
	13:{
		   'format':'3gp',
		   'quality':'Low Quality',
		   'dimension': '???',
		   'order':6
	   },
	17:{
		   'format':'3gp',
		   'quality':'Medium Quality',
		   'dimension':'144x176',
		   'order':4
	   },
	36:{
		   'format':'mp4',
		   'quality':'High Quality',
		   'order':2
	   },
	34:{
		   'format':'flv',
		   'quality':'320p',
		   'order':5
	   },
	35:{
		   'format':'flv',
		   'quality':'480p',
		   'order':4
	   },
	18:{
		   'format':'mp4',
		   'quality':'480p',
		   'order':3
	   },
	22:{
		   'format':'mp4',
		   'quality':'720p',
		   'order':1
	   },
	37:{
		   'format':'mp4',
		   'quality':'1080p',
		   'order':0
	   },
	45:{
		   'format':'webm',
		   'quality':'720p',
		   'order':7
	   },
	44:{
		   'format':'webm',
		   'quality':'520p',
		   'order':8
	   },
	43:{
		   'format':'webm',
		   'quality':'360x640',
		   'order':9
	   }
}


''' Argument checker ''' 
''' TODO Valid한 URL 인지 체크루틴 필요 ''' 
def argcheckandgeturl():
	if len(sys.argv) == 1:
		print "인자를 입력해주십셔 :: usage : youtube.py <watch_url>"
		exit (1)
	return sys.argv[1] + '&gl=US&hl=en&has_verified=1'

def geturlfd(requesturl):
	req = urllib2.Request(requesturl)
	try: 
		return urllib2.urlopen(req)
	except urllib2.URLError, e:
		print e.reason
		return ""

''' extract movie '''
def extract_movies(urlfd):
	movielist = []

	for line in urlfd:
		if line.strip() == "" or string.find(line, 'itag') == -1:
			continue
		m = re.findall('url_encoded_fmt_stream_map=(.[^&]*)', line)
		if len(m) > 0:
			fmt_url = urllib.unquote(m[0])
			urls = fmt_url.split(',')
			for url in urls:
				dict = parse_qs(url)
				if dict.has_key('itag'):
					quality = quality_dict[int(dict['itag'][0])]
					quality['src'] = urllib.unquote(dict['url'][0])
					quality['sig'] = dict['sig'][0]
					movielist.append(quality)
				else:
					continue
	print str(len(movielist)) + '가지 포맷의 동영상을 찾아냈습니다. ' 

	''' order(고화질순) 를 키로해서 정렬한다 ''' 
	movielist = sorted(movielist, key=lambda x: x['order'])
	for dict in movielist:
		print '\t' + dict['format'] + ' ' + dict['quality'] 
	return movielist

''' 파일 저장 매커니즘 정리 필요 '''
''' file 이름, 확장자, 저장위치 ''' 
def retrieve_moviefile(o, movie_id):
	filename = movie_id + '.' + o['format']
	print filename + ' downloading ... '

	req = urllib2.Request(o['src'] +"&signature=" + o['sig']);
	req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)');
	req.add_header('Referer','http://www.youtube.com/');
	req.add_header('Youtubedl-no-compression', 'True');
	try:
		wfile = urllib2.urlopen(req);
	except urllib2.URLError, e:
		print e
		print e.code
		exit (1)
	lfile = open(filename,'w');
	lfile.write(wfile.read());
	wfile.close()
	lfile.close()
	print 'finished ... '

def extract_movie_id(url):
	dict = parse_qs(url[url.find('?') +1:])
	if dict.has_key('v'):
		print 'movieid : ' + dict['v'][0]
		return dict['v'][0]
	print 'Movie id를 찾을수 없습니다.'
	exit(1)
	
	
''' Entry point ''' 
def main():
	urllib._urlopener = YoutubeURLOpener()
	url = argcheckandgeturl()
	movie_id = extract_movie_id(url)
	urlfd = geturlfd(url)
	
	movielist = extract_movies(urlfd)

	urlfd.close()
	if len(movielist) > 0:
		print '이중 가장 고화질의 파일을 다운로드합니다'
		retrieve_moviefile(movielist[0], movie_id)

if __name__ == '__main__':
	main()
