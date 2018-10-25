#!/usr/bin/env python

import requests # http requests
import websocket # websocket connections

# system libraries
import json # json
import argparse

import threading # lock
import time # sleep()

from varspace.settings import *
import botpackage

def on_close(ws):
	print('ws closed')

def on_error(ws, error):
	print('ws error: ' + error)

args = None

def on_message(ws, message):
	messageDecoded = json.loads(message)
	chatPost = messageDecoded['message']
	if messageDecoded['bottag'] in ['1', 1]:
		return
	args = [x.strip(' \t\n') for x in chatPost.split(' ')]
	print('received', repr(messageDecoded['message']))
	for bot in botpackage.__all__:
		answer = bot.processMessage(args, messageDecoded)
		if answer is not None:
			print('sending', repr(answer['message']))
			send(ws, answer['name'], answer['message'], messageDecoded['id']+1)

def send(ws, name, chatPost, position=0):
	message = {
		'channel' : 'fbot',
		'name' : name,
		'message' : chatPost,
		'delay' : position,
		'publicid' : '1',
		'bottag' : 1
	}
	with sending_lock:
		ws.send(json.dumps(message))
		time.sleep(_time_between_botposts)


def create_ws(args):
	authRequest = requests.post('https://chat.qed-verein.de/rubychat/account', data=credentials)

	ws = websocket.WebSocketApp('wss://chat.qed-verein.de/websocket?channel=' + args['channel'] + '&position=-0&version=2',
			cookie = format_cookies({
						'userid' : authRequest.cookies['userid'],
						'pwhash' : authRequest.cookies['pwhash'],
					}),
			on_message = on_message,
			on_error = on_error,
			on_close = on_close,
			)
	return ws

def format_cookies(obj):
	retval = ''
	for key in obj:
		retval += key + '=' + obj[key] + ';'
	return retval

def mainloop(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--interactive', action='store_true')
	parser.add_argument('--channel', default='fbot')
	args = vars(parser.parse_args())

	if args['interactive'] == True:
		eiDii = 0
		while True:
			eiDii += 1
			try:
				inp = input('')
			except EOFError:
				exit(0)
			except:
				raise
			inpSplit = inp.split(' ')
			for bot in botpackage.__all__:
				x = bot.processMessage(inp.split(' ')[1:], {'name': inp.split(' ')[0], 'message': ''.join(inp.split(' ')[1:]), 'id' : eiDii})
				if x is not None:
					print(x)
			print()
	create_ws(args).run_forever()

if __name__ == '__main__':
	sending_lock = threading.Lock()

	try:
		mainloop(args)
	except KeyboardInterrupt:
		pass
	except Exception:
		raise
