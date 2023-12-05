import pprint
import requests
import re
import json
import subprocess
import os
      #https://api.bilibili.com/pgc/player/web/v2/playurl?support_multi_audio=true&avid=209275263&cid=18461714&qn=80&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&ep_id=108772&session=4197b3405796e9eb8f75abc1c800cac4&drm_tech_type=2
url = 'https://api.bilibili.com/pgc/player/web/v2/playurl?support_multi_audio=true&avid=11158411&cid=18461723&qn=80&fnver=0&fnval=4048&fourk=1&gaia_source=&from_client=BROWSER&ep_id=108766&session=470f673cc499f829159c9ee270107d74&drm_tech_type=2'
headers = {
    'cookie':'LIVE_BUVID=AUTO4716404297276975; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; buvid_fp_plain=undefined; buvid4=5A8A40C9-473F-D41C-1582-561111B563E459166-022013119-s1Fxj9YrQ%2FP3tunafhkeuQ%3D%3D; DedeUserID=327583066; DedeUserID__ckMd5=c5728077e592dd61; rpdid=|(umYuY~~kYl0J\'uYYm||J|Jk; buvid3=EF298286-1052-9B4B-6ACE-E37BC1F88DBE03734infoc; b_nut=1672128603; _uuid=1B98988D-749D-F537-1E2F-AA10101E9C5101604148infoc; b_ut=5; header_theme_version=CLOSE; nostalgia_conf=-1; CURRENT_PID=e7f66140-d13c-11ed-95e9-8d2bcc9c0511; FEED_LIVE_VERSION=V8; enable_web_push=ENABLE; iflogin_when_web_push=1; home_feed_column=5; fingerprint=06570a17f133e7acbc474f7e5f525e1d; CURRENT_QUALITY=80; browser_resolution=1612-846; buvid_fp=06570a17f133e7acbc474f7e5f525e1d; CURRENT_FNVAL=4048; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDE4NzA1NDQsImlhdCI6MTcwMTYxMTI4NCwicGx0IjotMX0.lMVjWbb_ynI_P1eVumwqR2l9gaZdwYOnF0hFxwTldDE; bili_ticket_expires=1701870484; b_lsid=F5C29D4A_18C39BAFBEC; bp_video_offset_327583066=871614409582051349; SESSDATA=fed409e4%2C1717331106%2Caff5b%2Ac2CjDMVoIkWjyxsfMfDghHMrpoxCicVeEKQwX132qD2v0cTw_cKXzV-x3z_4XCkF8fAIoSVmpVN25MWXZYYlZ0elZLTExiMl93S0U5UWtLWWE5T3hSV3d1VVREYTBHbHozSU9xR0t1OXFCX0x1SmV1N1F0d2Z6Z3hQRUFMMk0taEtNTnJYSTdHdWJnIIEC; bili_jct=d1a7c5390a5654ac8928c3748ce841db; sid=80w8j7ac; PVID=2',
    'referer':'https://www.bilibili.com/',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }
response = requests.get(url=url,headers=headers)
json_name = json.loads(requests.get(url='https://api.bilibili.com/pgc/review/user?media_id=6260&ts=1701779563902',headers=headers).text)
json_title = json_name['result']['media']['title'].replace(' ','')
title = re.sub(r'[\/:*?"><|]','',json_title)
json_data = json.loads(response.text)
audio_url = json_data['result']['video_info']['dash']['audio'][0]['baseUrl']
video_url = json_data['result']['video_info']['dash']['video'][0]['baseUrl']
#pprint.pprint(json_data)
audio_content = requests.get(url=audio_url,headers=headers).content
video_content = requests.get(url=video_url,headers=headers).content
with open('F:\\python-crawler\\download\\' + title + '.mp3',mode='wb') as audio:
    audio.write(audio_content)
with open('F:\\python-crawler\\download\\' + title + '.mp4',mode='wb') as video:
    video.write(video_content)
 

cmd = f'F:\\ffmpeg-6.1-essentials_build\\bin\\ffmpeg -i F:\\python-crawler\\download\\{title}.mp4 -i F:\\python-crawler\\download\\{title}.mp3 -c:v copy -c:a aac -strict experimental F:\\python-crawler\\download\\{title}output.mp4'
subprocess.run(cmd,shell=True)