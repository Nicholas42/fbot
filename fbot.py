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
from botpackage.helper.mystrip import mystrip, mylstrip, _space_chars

def on_close(ws):
	print('ws closed')

def on_error(ws, error):
	print('ws error: ' + error)

args = None
db_connection = sqlite3.connect('varspace/fbotdb.sqlite')

def on_message(ws, message):
	messageDecoded = json.loads(message)
	chatPost = messageDecoded['message']
	messageDecoded['name'] = mystrip(messageDecoded['name'])
	if int(messageDecoded['bottag']) != 0:
		return
	args = split_with_quotation_marks(chatPost)
	print('received', repr(messageDecoded['message']))
	for bot in botpackage.__all__:
		answer = bot.processMessage(args, messageDecoded, db_connection)
		if answer is not None:
			print('sending', repr(answer['message']))
			send(ws, answer['name'], answer['message'], messageDecoded['id']+1)


def send(ws, name, chatPost, position=0):
	message = dict(
		# ~ 'channel' : args['channel'],
		name = name,
		message = chatPost,
		delay = position,
		publicid = '1',
		bottag = 1
	)
	with sending_lock:
		ws.send(json.dumps(message))
		time.sleep(_time_between_botposts)


def getCookies():
	while True:
		try:
			req = requests.post('https://chat.qed-verein.de/rubychat/account', data=credentials)
		except ConnectionResetError as e:
			print('Error while downloading cookies:', e)
		else:
			return req.cookies
		time.sleep(1)

def create_ws(cookies, args):
	try:
		cookies['userid']
		cookies['pwhash']
	except AttributeError:
		print('cookies not right')
		return

	ws = websocket.WebSocketApp('wss://chat.qed-verein.de/websocket?channel=' + args['channel'] + '&position=-0&version=2',
			cookie = format_cookies(dict(
						userid = cookies['userid'],
						pwhash = cookies['pwhash'],
					)),
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
	for i in range(len(s)):
		if quote_mode is None:
			if s[i] in _quotation_chars and i > 0 and s[i-1] in _space_chars:
				quote_mode = s[i]
				retval.append('')
			elif s[i] in _space_chars:
				retval.append('')
				pass
			else:
				retval[len(retval)-1] += s[i]
		else:
			if s[i] == quote_mode:
				quote_mode = None
			else:
				retval[len(retval)-1] += s[i]
	return [x for x in retval if x != '']


def mainloop(args):
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--interactive', action='store_true')
	parser.add_argument('--channel', default='fbot')
	parser.add_argument('--mainchannel-on-my-own-risk', action='store_true')
	parsedArgs = vars(parser.parse_args())

	if parsedArgs['interactive'] == True:
		print('fbot interactive mode. first word will be used as nick')
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
			message = {
				'name': ''.join(inpSplit[:1]),
				'message': mystrip(inp[inp.find(inpSplit[0])+len(inpSplit[0])+1:]),
				'id' : eiDii
			}
			for bot in botpackage.__all__:
				x = bot.processMessage(inpSplit[1:], message, db_connection)
				if x is not None:
					print(x)
			print()

	if parsedArgs['mainchannel_on_my_own_risk'] == True:
		parsedArgs['channel'] = ''
	cookies = getCookies()
	while True:
		print('creating new websocket')
		ws = create_ws(cookies, parsedArgs)
		if ws:
			ws.run_forever()
		time.sleep(1)

if __name__ == '__main__':
	sending_lock = threading.Lock()

	try:
		mainloop(args)
	except KeyboardInterrupt:
		pass
