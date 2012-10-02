#!/usr/bin/python
# -*- coding: utf8 -*-
################################
# Youtube Movie Grabber        #
# @since 2012.09.08            #
# @Author dsdgun@gmail.com     #
# @Homepage blog.dsdstudio.net #
################################

import re, sys, string, fileinput, urllib, urllib2, logging

class YoutubeURLOpener(urllib.FancyURLopener):
	version = 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'

''' 퀄리티 코드 dict + array 로 구성하였다 '''
''' TODO 아직 못구한 코드에 대한정보 수집 필요 '''
quality_dict = {
	13:{
		   'format':'3gp',
		   'quality':'Low Quality',
		   'order':6
	   },
	17:{
		   'format':'3gp',
		   'quality':'Medium Quality',
		   'order':4
	   },
	36:{
		   'format':'3gp',
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
	   }
}


''' Argument checker ''' 
''' TODO Valid한 URL 인지 체크루틴 필요 ''' 
def argcheckandgeturl():
	if len(sys.argv) == 1:
		print "인자를 입력해주십셔 :: usage : youtube.py <watch_url>"
		exit (1)
	return sys.argv[1]

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
		m = re.findall('stream_map=(.[^&]*)', line)
		if len(m) > 0:
			fmt_url = urllib.unquote(m[0])
			''' 직접입력일때만 이 로직이 필요하다 
				urlopen으로 데이터를 가져오면 한번 escaping이 일어나서 
				특수 unicode 문자열은 따로 처리해주지않아도 된다. '''
			''' m = re.findall('^(.*?)\\\\u0026',fmt_url); '''
			urls = fmt_url.split(',')
			for url in urls:
				''' realurl_tup = re.findall('url=(.*?)&.*?itag=([0-9]+)', url); '''
				realurl_tup = re.findall('itag=([0-9]+)&url=(.*?)&.*?', url);
				if len(realurl_tup) > 0:
					try:
						movie_url = urllib.unquote(realurl_tup[0][1])
						quality = quality_dict[int(realurl_tup[0][0])]
						quality['src'] = movie_url
						movielist.append(quality)
					except:
						print '찾을수 없는 타입입니다' + realurl_tup[0][0]
	print str(len(movielist)) + '가지 포맷의 동영상을 찾아냈습니다. ' 

	''' order(고화질순) 를 키로해서 정렬한다 ''' 
	movielist = sorted(movielist, key=lambda x: x['order'])
	for dict in movielist:
		print '\t' + dict['format'] + ' ' + dict['quality'] 
	return movielist

''' 파일 저장 매커니즘 정리 필요 '''
''' file 이름, 확장자, 저장위치 ''' 
def retrieve_moviefile(o):
	filename = 't.' + o['format']
	print filename + ' ' + o['src'] + ' downloading ... '
	req = urllib2.Request(o['src']);
	req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)');
	wfile = urllib2.urlopen(req);
	lfile = open(filename,'w');
	lfile.write(wfile.read());
	wfile.close()
	lfile.close()
	print 'finished ... '

''' Entry point ''' 
def main():
	urllib._urlopener = YoutubeURLOpener()
	url = argcheckandgeturl()
	urlfd = geturlfd(url)
	movielist = extract_movies(urlfd)
	urlfd.close()
	if len(movielist) > 0:
		print '이중 가장 고화질의 파일을 다운로드합니다'
		retrieve_moviefile(movielist[0])

if __name__ == '__main__':
	main()
