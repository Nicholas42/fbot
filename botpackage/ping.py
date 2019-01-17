import sqlite3
import parsedatetime, datetime

from botpackage.helper import helper
from botpackage.helper.mystrip import _space_chars, stripFromBegin, norm
from botpackage.helper.split import split_with_quotation_marks

import varspace.settings as settings

_botname = 'Navi'
_posts_since_ping = 25

def processMessage(args, rawMessage, db_connection):
	cursor = db_connection.cursor()

	message = None

	if rawMessage['username'] != None:
		recipientNicks = [rawMessage['username'].lower()]
	else:
		recipientNicks = [norm(rawMessage['name'])]
	for nick in cursor.execute(
				'SELECT lower(nickname) '
				'FROM nicknames '
				'WHERE userid = ('
					'SELECT userid '
					'FROM nicknames '
					'WHERE lower(nickname) == ? '
					'ORDER BY deletable DESC'
				');', (recipientNicks[0],)
		):
		if nick[0].lower() not in recipientNicks:
			recipientNicks.append(nick[0].lower())


	pingProperties = dict(print=True, delete=True)
	for nick in recipientNicks:
		cursor = db_connection.cursor()
		pongs = cursor.execute(
				'SELECT sender, message, messageid, id '
				'FROM pings '
				'WHERE lower(recipient) == ? '
				';', (nick.lower(), )
				).fetchall()
		for pong in pongs:
			if pong[2] + _posts_since_ping > rawMessage['id']:
				pingProperties['print'] = False
			# ~ pongSplit = split_with_quotation_marks(pong[1])
			# ~ if len(pongSplit) >= 3 \
					# ~ and pongSplit[0].startswith('-') \
					# ~ and pongSplit[0][1:] == 'pong':
				# ~ pongTime = datetime.datetime(*parsedatetime.Calendar().parse(pongSplit[1])[0][:6])
				# ~ if datetime.datetime.now() < pongTime:
					# ~ pingProperties['print'] = False
				# ~ else:
					# ~ pingProperties['delete'] = False

			if pingProperties['print'] == True:
				if message == None:
					message = rawMessage['name'].strip(_space_chars) + ', dir wollte jemand etwas sagen:'
				message += '\n' + pong[0] + ' sagte: ' + pong[1]
			else:
				pingProperties['ping'] = True
			if pingProperties['delete']:
				cursor.execute(
							'DELETE '
							'FROM pings '
							'WHERE id == ? '
							';', (pong[3],))
		db_connection.commit()

	if len(args) >= 2 and args[0] == '!ping' and ''.join(args[2:]).strip(_space_chars) != '':
		cursor = db_connection.cursor()
		pingCount = cursor.execute(
					'SELECT count(*) '
					'FROM pings '
					'WHERE recipient == ? '
					'AND sender == ? '
					';', (args[1], rawMessage['name'].strip(_space_chars))
		).fetchone()
		if pingCount[0] == 0 or not settings.overwrite_pings:
			cursor.execute(
						'INSERT OR REPLACE '
						'INTO pings '
						'(recipient, message, sender, messageid) '
						'VALUES (?, ?, ?, ?)'
						';', (
							args[1],
							stripFromBegin(rawMessage['message'], args[0:2]),
							rawMessage['name'].strip(_space_chars),
							rawMessage['id'],
						)
				)
		else:
			cursor.execute(
						'UPDATE pings '
						'SET message = ?, messageid = ? '
						'WHERE recipient = ? '
						'AND sender = ?'
						';', (
							stripFromBegin(rawMessage['message'], args[0:2]),
							rawMessage['id'],
							args[1],
							rawMessage['name'].strip(_space_chars),
						)
				)
		db_connection.commit()

	if message is not None:
		return helper.botMessage(message, _botname)
