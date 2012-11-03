## Python Study  

Python 개인스터디용으로 한번 만들어봤습니다 :) 


## yt downloader 

코드구조나 개선사항이 있으면 issue에 올려주세요 

사용법 

	$> ./youtube.py <youtube_url>

Watch URL Example 

	http://www.youtube.com/watch?v=${video_id}
	http://www.youtube.com/watch?v=9bZkp7q19f0&feature=g-wl

video id명 + 확장자의 형태로 동영상파일이 실행한 경로에 저장됩니다.   

예) `Mbw_aa1.mp4`


## 쓸만한 코드패턴 

substring 

	str = 'xxx?aaa'
	str[str.find('?'):]

	>> aaa

str.lastindexof 

	str = 'a12.ddd.flac'
	str.rfind('.')

	>> 7

subprocess control



## Subprocess 호출 

