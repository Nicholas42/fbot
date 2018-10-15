#!/usr/bin/env python

import requests # http requests
import websocket # websocket connections

# system libraries
# ~ import re # regex
import json # json

from settings import credentials
import botpackage

channel = ''
def on_message(ws, message):
	process_message(ws, message)

def on_close(ws):
	print('ws closed')

def on_error(ws, error):
	print('ws error: ' + error)


def process_message(ws, message):
	messageDecoded = json.loads(message)
	chatPost = messageDecoded['message']
	if messageDecoded['bottag'] in ['1', 1]:
		return
	args = [x.strip(' \t\n') for x in chatPost.split(' ')]
	print('processing', args)
	for bot in botpackage.__all__:
		answer = bot.processMessage(args)
		if answer is not None:
			send(ws, answer['name'], answer['message'], messageDecoded['id'])

def send(ws, name, chatPost, position):
	message = {
		'channel' : 'fbot',
		'name' : name,
		'message' : chatPost,
		'delay' : position + 1,
		'publicid' : '1',
		'bottag' : 1
	}
	ws.send(json.dumps(message))


def create_ws():
	authRequest = requests.post('https://chat.qed-verein.de/rubychat/account', data=credentials)

	ws = websocket.WebSocketApp('wss://chat.qed-verein.de/websocket?channel=' + channel + '&position=-0&version=2',
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
		# ~ print(botpackage.nickname.processMessage(['!nickname', 'franz'], 'Franz'))
		# ~ exit(0)
		while True:
			inp = input('')
			for x in botpackage.__all__:
				print(x.processMessage(inp.split(' ')[1:], inp.split(' ')[0]))
			print()
		# ~ mainloop()
	except KeyboardInterrupt:
		pass
	except Exception:
		raise
