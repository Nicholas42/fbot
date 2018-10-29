#!/usr/bin/env python

import requests # http requests
import websocket # websocket connections
import sqlite3
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
db_connection = sqlite3.connect('varspace/fbotdb.sqlite')

def on_message(ws, message):
	messageDecoded = json.loads(message)
	chatPost = messageDecoded['message']
	messageDecoded['name'] = messageDecoded['name'].strip(' \n\t\u200b')
	if messageDecoded['bottag'] in ['1', 1]:
		return
	args = split_with_quotation_marks(chatPost)
	print('received', repr(messageDecoded['message']))
	for bot in botpackage.__all__:
		answer = bot.processMessage(args, messageDecoded, db_connection)
		if answer is not None:
			print('sending', repr(answer['message']))
			send(ws, answer['name'], answer['message'], messageDecoded['id']+1)


def send(ws, name, chatPost, position=0):
	message = {
		# ~ 'channel' : args['channel'],
		'name' : name,
		'message' : chatPost,
		'delay' : position,
		'publicid' : '1',
		'bottag' : 1
	}
	with sending_lock:
		ws.send(json.dumps(message))
		time.sleep(_time_between_botposts)


def getCookies():
	return requests.post('https://chat.qed-verein.de/rubychat/account', data=credentials)

def create_ws(args):
	authRequest = getCookies()

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

def split_with_quotation_marks(s):
	retval = ['']
	quote_mode = None
	_quotation_chars = ['\'', '"']
	_space_chars = [' ', '\t', '\n']
	for c in s:
		if quote_mode is None:
			if c in _quotation_chars:
				quote_mode = c
				retval.append('')
			elif c in _space_chars:
				retval.append('')
				pass
			else:
				retval[len(retval)-1] += c
		else:
			if c == quote_mode:
				quote_mode = None
			else:
				retval[len(retval)-1] += c
	return [x for x in retval if x != '']


def mainloop(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--interactive', action='store_true')
	parser.add_argument('--channel', default='fbot')
	args = vars(parser.parse_args())

	if args['interactive'] == True:
		print('fbot interactive mode. your wish?')
		eiDii = 0
		while True:
			eiDii += 1
			try:
				inp = input('> ')
			except EOFError:
				exit(0)
			except:
				raise
			inpSplit = split_with_quotation_marks(inp)
			for bot in botpackage.__all__:
				x = bot.processMessage(inpSplit[1:], {'name': ''.join(inpSplit[:1]), 'message': ' '.join([x + ' ' for x in inpSplit[1:]]), 'id' : eiDii}, db_connection)
				if x is not None:
					print(x)
			print()
	while True:
		create_ws(args).run_forever()
		time.sleep(1)

if __name__ == '__main__':
	sending_lock = threading.Lock()

	try:
		mainloop(args)
	except KeyboardInterrupt:
		pass
