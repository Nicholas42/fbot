import sqlite3

from botpackage.helper import helper

_botname = 'pingbot'
_posts_since_ping = 2

def processMessage(args, rawMessage, db_connection):
	cursor = db_connection.cursor()

	message = None

	recipientNicks = [rawMessage['name'].lower()]
	for nick in cursor.execute(
				'SELECT lower(nickname) '
				'FROM nicknames '
				'WHERE userid = ('
					'SELECT userid '
					'FROM nicknames '
					'WHERE lower(nickname) == ? '
					'ORDER BY deletable DESC'
				');', (rawMessage['name'].lower(),)
		):
		if nick[0].lower() not in recipientNicks:
			recipientNicks.append(nick[0].lower())


	notThisPing = False
	for nick in recipientNicks:
		cursor = db_connection.cursor()
		for pong in \
					cursor.execute(
						'SELECT sender, message, messageid '
						'FROM pings '
						'WHERE lower(recipient) == ? '
						';', (nick.lower(), )
				):
			if pong[2] + _posts_since_ping - 1 >= rawMessage['id']:
				notThisPing = True
			if notThisPing == False:
				if message is None:
					message = rawMessage['name'] + ', dir wollte jemand etwas sagen:'
				message += '\n' + pong[0] + ' sagte: ' + pong[1]
			else:
				notThisPing = False
		cursor.execute(
					'DELETE '
					'FROM pings '
					'WHERE LOWER(recipient) == ? '
					';', (nick,))
		# ~ db_connection.commit()

	if len(args) > 1 and args[0] == '!ping' and ''.join(args[2:]).strip(' \t\n') != '':
		cursor = db_connection.cursor()
		pingCount = cursor.execute(
					'SELECT count(*) '
					'FROM pings '
					'WHERE recipient == ?'
					';', (args[1], )
		).fetchone()
		if pingCount[0] is 0:
			cursor.execute(
						'INSERT OR REPLACE '
						'INTO pings '
						'(recipient, message, sender, messageid) '
						'VALUES (?, ?, ?, ?)'
						';', (
							args[1],
							''.join(x + ' ' for x in args[2:]).strip(),
							rawMessage['name'],
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
							''.join(x + ' ' for x in args[2:]).strip(),
							rawMessage['id'],
							args[1],
							rawMessage['name'],
						)
				)
		db_connection.commit()

	if message is not None:
		return helper.botMessage(message, _botname)
