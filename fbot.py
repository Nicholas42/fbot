#!/usr/bin/env python

import requests # http requests
import websocket # websocket connections

# system libraries
# ~ import re # regex
import json # json

from settings import credentials
import botpackage

def on_message(ws, message):
	process_message(ws, message)

def on_close(ws):
	print('ws closed')

def on_error(ws, error):
	print('ws error: ' + error)


def process_message(ws, message):
	messageDecoded = json.loads(message)
	chatPost = messageDecoded['message']
	position = messageDecoded['id']
	print('parsing', repr(chatPost))
	args = [x.strip(' \t\n') for x in chatPost.split(' ')]
	for x in botpackage.__all__:
		answer = x.processMessage(args)
		if answer is not None:
			send(ws, answer['name'], answer['message'], position)

def send(ws, name, chatPost, position):
	message = {
		'channel' : 'fbot',
		'name' : name,
		'message' : chatPost,
		'delay' : position + 1,
		'publicid' : '1',
		'bottag' : '1'
	}
	ws.send(json.dumps(message))


def create_ws():
	authRequest = requests.post('https://chat.qed-verein.de/rubychat/account', data=credentials)

	ws = websocket.WebSocketApp('wss://chat.qed-verein.de/websocket?channel=fbot&position=-0&version=2',
			cookie = "userid=440; pwhash=" + authRequest.cookies['pwhash'],
			on_message = on_message,
			on_error = on_error,
			on_close = on_close,
			)
	return ws

def mainloop():
	ws = create_ws()
	ws.run_forever()


if __name__ == '__main__':
	try:
		mainloop()
	except KeyboardInterrupt:
		pass
	except Exception as e:
		print(e)
