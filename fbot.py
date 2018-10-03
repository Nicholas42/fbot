#!/usr/bin/env python

import requests # http requests
import websocket # websocket connections

# system libraries
import re # regex
import json # json

def on_message(ws, message):
	process_message(ws, message)

def on_close(ws):
	print('ws was closed')

def on_error(ws, error):
	print('ws error: ' + error)


def process_message(ws, message):
	print(message)
	messageDecoded = json.loads(message)
	chatPost = messageDecoded['message']
	# ~ position = messageDecoded['delay']
	# ~ print('position set to', position)
	print('received ', repr(chatPost))
	if re.match('!fbot', chatPost):
		send(ws)

def send(ws):
	message = {
		'channel' : 'fbot',
		'name' : 'fbot',
		'message' : 'heureka',
		# ~ 'delay' : position + 1,
		'publicid' : '1',
		'bottag' : 1
	}
	print('sending', message)
	ws.send(json.dumps(message))

def mainloop () :
	position = 0
	credentials = {
		'username' : '',
		'password' : '',
		'version' : '20171030131648'
	}
	authRequest = requests.post('https://chat.qed-verein.de/rubychat/account', data=credentials)

	ws = websocket.WebSocketApp('wss://chat.qed-verein.de/websocket?channel=fbot&position=-0&version=2',
			cookie = "userid=440; pwhash=" + authRequest.cookies['pwhash'],
			on_message = on_message,
			on_error = on_error,
			on_close = on_close,
			)
	ws.run_forever()


if __name__ == '__main__':
	try:
		mainloop()
	except KeyboardInterrupt:
		pass
