import sqlite3

_help = '!nickname <nickname> [[-a|-r] <nickname>]'

def processMessage(args):
	message = _help
	if len(args) >= 2:
		if args[0] not in ['!nickname', '!nicknames']:
			return

		db_connection = sqlite3.connect('fbotdb.sqlite')
		cursor = db_connection.cursor()

		userid = cursor.execute(
					'SELECT userid '
					'FROM nicknames '
					'WHERE lower(nickname) == ? '
				';', (args[1].lower(), )).fetchone()

	# print nicknames
	if len(args) == 2:
		if userid == None:
			message = 'Ich kenne ' + args[1] + ' nicht.'
		else:
			userid = userid[0]

			nicknames = []
			username = cursor.execute(
						'SELECT nickname '
						'FROM nicknames '
						'WHERE userid == ? '
						'AND deletable == 1'
					';', (userid, )).fetchone()[0]

			for nickname in cursor.execute(
						'SELECT nickname '
						'FROM nicknames '
						'WHERE userid == ?'
						'AND deletable == 0'
						';', (userid, )
					):
				nicknames.append(nickname[0])

			if len(nicknames) > 1:
				message = username + ' hat die Nicknames:\n'
				for nickname in nicknames:
					message += nickname + '\n'
	# add, remove nicknames
	elif len(args) == 4:
		if args[2] == '-a': # add nickname
			if userid is None: # nickname existiert noch nicht
				message = 'Ich kenne ' + args[1] + ' nicht.'
			else:
				cursor = db_connection.cursor() ## todo braucht man das wirklich
				toAddCheck = cursor.execute(
							'SELECT userid '
							'FROM nicknames '
							'WHERE nickname == ?'
							';', (args[3].lower(), )).fetchone()
				if toAddCheck is not None:
					message = 'Der nickname ' + args[3] + ' existiert schon.'
				else:
					cursor = db_connection.cursor()
					cursor.execute('INSERT INTO nicknames (nickname, userid) VALUES (?, 440);', args[3])
					db_connection.commit()
					message = args[1] + ' hat nun den Nickname ' + args[3] + '.'
		elif args[2] == '-r': # remove nickname
			message = _help

	else:
		db_connection.close()
		message = _help
		return

	db_connection.close()
	return {'name' : 'nicknamebot', 'message' : message}
