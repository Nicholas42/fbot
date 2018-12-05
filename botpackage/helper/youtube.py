import requests
import json

from varspace.settings import google_api_key

_yt_api_url = 'https://www.googleapis.com/youtube/v3/videos?'

def title(vid_id : str):
	try:
		r = requests.get(_yt_api_url + 'key=%s&id=%s&part=%s'%(google_api_key, vid_id, 'snippet'))
	except requests.exception.ConnectionError as e:
		print(type(e))
	# ~ items = json.loads(r.text)['items']
	if items == []:
		return
	vid_title = items[0]['snippet']['localized']['title']
	return vid_title
