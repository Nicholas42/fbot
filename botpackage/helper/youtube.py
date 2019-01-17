import requests
import json

import varspace.settings as settings

_yt_api_url = 'https://www.googleapis.com/youtube/v3/videos?'

def title(vid_id : str):
	try:
		r = requests.get(_yt_api_url + 'key=%s&id=%s&part=%s'%(settings.google_api_key, vid_id, 'snippet'))
		items = json.loads(r.text)['items']
		if items == []:
			return dict(status=1, error='Das Video gibts doch gar nicht.')
		vid_title = items[0]['snippet']['localized']['title']
		return dict(status=0, title=vid_title)
	except requests.exceptions.ConnectionError as e:
		return dict(status=1, error='sry*50 ich kann youtube nicht erreichen.')
	except Exception as e: #socket.gaierror as e:
		return dict(status=1, error='NO')
