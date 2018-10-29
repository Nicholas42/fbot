import sqlite3

from botpackage.helper import helper
_botname = 'Luise'
_help = '#name nick [-s|-a <int>|-r <int>]'

def processMessage(args, rawMessage, db_connection):
	if len(args) < 2:
		return

	if '' in args[:2]:
		return

	if args[0][0] not in ['#']:
		return


	parsedArgs = {'punktName' : args[0], 'username' : args[1], 'toAdd' : 1}
	try:
		if len(args) >= 3:
			if args[2] == '-s':
				parsedArgs['toAdd'] = 0
			elif args[2] == '-a':
				if len(args) >= 4:
					parsedArgs['toAdd'] = int(args[3])
			elif args[2] == '-r':
				if len(args) == 3:
					parsedArgs['toAdd'] = -1
				else:
					parsedArgs['toAdd'] = int(args[3])
			else:
				return helper.botMessage(_help, _botname)
	except ValueError:
		return


	cursor = db_connection.cursor()

	if args[1] == 'self':
		username = rawMessage['name']
	else:
		username = args[1]
	userid = helper.useridFromUsername(cursor, username)

	if userid is None:
		return helper.botMessage('Ich kenne ' + username + ' nicht.', _botname)

	username = helper.usernameFromUserid(cursor, userid)

	punktname = args[0]
	punktid = punktidFromPunktName(cursor, punktname)

	anzahl = anzahlFromPunktidAndUserid(cursor, punktid, userid)

	if parsedArgs['toAdd'] == 0:
		return helper.botMessage(username + ' hat ' + str(anzahl)  + ' ' + punktname[1:] + '.', _botname)
	else:
		if punktid is None:
			cursor.execute(
						'INSERT INTO freiepunkteliste (name) VALUES (?);',
						(punktname,)
					)
			punktid = cursor.execute(
						'SELECT id FROM freiepunkteliste WHERE name == ?;',
						(punktname,)
					).fetchone()[0]
		if anzahl is None:
			anzahl = parsedArgs['toAdd']
			cursor.execute(
							'INSERT INTO freiepunkte '
							'(userid, freiepunkteid, anzahl) '
							'VALUES (?, ?, ?) '
							';', (userid, punktid, anzahl)
						)
		else:
			anzahl += parsedArgs['toAdd']
			cursor.execute(
						'UPDATE freiepunkte '
						'SET anzahl = ? '
						'WHERE freiepunkteid = ? '
						'AND userid = ? '
						';', (anzahl, punktid, userid)
					)
		db_connection.commit()
		return helper.botMessage(username + ' hat jetzt ' + str(anzahl)  + ' ' + punktname[1:] + '.', _botname)
	return


def punktidFromPunktName(cursor, punktName):
	query = cursor.execute(
				'SELECT id FROM freiepunkteliste WHERE name = ?;',
				(punktName.lower(),)
			).fetchone()
	return None if query is None else query[0]


def anzahlFromPunktidAndUserid(cursor, punktid, userid):
	if punktid is None:
		return 0
	query = cursor.execute(
				'SELECT anzahl '
				'FROM freiepunkte '
				'WHERE freiepunkteid = ? '
				'AND userid == ? '
				';', (punktid, userid,)
			).fetchone()

	return None if query is None else query[0]
