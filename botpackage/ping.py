import sqlite3

def processMessage(args, rawMessage):
	db_connection = sqlite3.connect('fbotdb.sqlite')
	cursor = db_connection.cursor()

	message = None

	recipientNicks = [rawMessage['name']]
	for nick in cursor.execute(
				'SELECT nickname '
				'FROM nicknames '
				'WHERE userid = ('
					'SELECT userid '
					'FROM nicknames '
					'WHERE lower(nickname) == ? '
					'ORDER BY deletable DESC'
				');', (rawMessage['name'].lower(),)
		):
		if nick[0] not in recipientNicks:
			recipientNicks.append(nick[0])

	for nick in recipientNicks:
		cursor = db_connection.cursor()
		for pong in \
					cursor.execute(
						'SELECT sender, message '
						'FROM pings '
						'WHERE lower(recipient) == ? '
						';', (nick.lower(), )
		):
			if message is None:
				message = name + ', dir wollte jemand etwas sagen:'
			message += '\n' + pong[0] + ' sagte: ' + pong[1]
			cursor.execute(
						'DELETE '
						'FROM pings '
						'WHERE lower(recipient) = ?'
						';', (nick.lower(), ))
			db_connection.commit()

	if len(args) > 1 and args[0] == '!ping':
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
		return {'name' : 'pingbot', 'message' : message}
