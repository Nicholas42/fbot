import sqlite3

from botpackage.helper import helper

_help = 'usage: !nickname <nickname> [[-a|-r] <nickname>]'
_botname = 'nicknamebot'


def processMessage(args, rawMessage):
	if len(args) == 0:
		return
	if args[0] not in ['!nickname', '!nicknames']:
		return

	if len(args) < 2:
		return helper.botMessage(_help, _botname)

	db_connection = sqlite3.connect('fbotdb.sqlite')
	cursor = db_connection.cursor()

	if args[1].lower() == 'self':
		args[1] = rawMessage['name']

	useridQuery = cursor.execute(
				'SELECT userid '
				'FROM nicknames '
				'WHERE lower(nickname) == ? '
			';', (args[1].lower(), )).fetchone()
	if useridQuery is None:
		return helper.botMessage('Ich kenne ' + args[1] + ' nicht.', _botname)

	userid = useridQuery[0]

	username = cursor.execute(
				'SELECT nickname '
				'FROM nicknames '
				'WHERE userid == ? '
				'AND deletable == 1'
				';', (userid, )).fetchone()[0]

	# print nicknames
	if len(args) == 2:
		message = ''
		nicknames = []
		for nickname in cursor.execute(
					'SELECT nickname '
					'FROM nicknames '
					'WHERE userid == ? '
					'AND deletable == 0'
					';', (userid, )
				):
			nicknames.append(nickname[0])

		if len(nicknames) < 1:
			return

		message = username + ' hat die Nicknames:\n'
		for nickname in nicknames:
			message += nickname + '\n'

	# add, remove nicknames
	elif len(args) == 4:
		if args[2] == '-a': # add nickname
			cursor = db_connection.cursor() ## todo braucht man das wirklich
			toAddCheck = cursor.execute(
						'SELECT userid '
						'FROM nicknames '
						'WHERE lower(nickname) == ?'
						';', (args[3].lower(), )).fetchone()
			if toAddCheck is not None:
				message = 'Der nickname ' + args[3] + ' existiert schon.'
			else:
				cursor = db_connection.cursor()
				cursor.execute('INSERT INTO nicknames (nickname, userid) VALUES (?, ?);', (args[3], userid))
				db_connection.commit()
				message = username + ' hat nun den Nickname ' + args[3] + '.'
		elif args[2] == '-r': # remove nickname
			toRemoveCheck = cursor.execute(
						'SELECT userid '
						'FROM nicknames '
						'WHERE lower(nickname) == ?'
						';', (args[3].lower(), )).fetchone()
			if toRemoveCheck is None:
				message = 'Ich kenne ' + args[3] + ' nicht.'
			else:
				cursor = db_connection.cursor()
				cursor.execute(
						'DELETE FROM nicknames '
						'WHERE nickname == ?'
						';', (args[3], ))
				db_connection.commit()
				message = username + ' hat jetzt den nicknamen ' + args[3] + ' nicht mehr.'
		else:
			message = _help
	else:
		message = _help

	db_connection.close()
	return helper.botMessage(message, _botname)
