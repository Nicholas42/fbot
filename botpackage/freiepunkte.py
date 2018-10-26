import sqlite3
from enum import Enum

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

	cursor = db_connection.cursor()

	useridQuery = cursor.execute(
			'SELECT userid '
			'FROM nicknames '
			'WHERE lower(nickname) == ? '
		';', (args[1].lower(), )).fetchone()
	if useridQuery is None:
		return helper.botMessage('Ich kenne ' + args[1] + ' nicht.', _botname)

	userid = useridQuery[0]

	modifyMode = False
	if len(args) == 2:
		modifyMode = True
	else:
		if args[2] in ['-a', '-r']:
			modifyMode = True

	username = cursor.execute(
				'SELECT nickname '
				'FROM nicknames '
				'WHERE userid == ? '
				'AND deletable == 1'
				';', (userid, )).fetchone()[0]

	punktName = args[0]

	freiepunktidAnfrage = cursor.execute(
				'SELECT id FROM freiepunkteliste WHERE name = ?;',
				(args[0],)
			).fetchone()
	if freiepunktidAnfrage is None:
		punkteWert = 0
		if modifyMode:
			cursor.execute(
					'INSERT INTO freiepunkteliste (name) VALUES (?);',
					(punktName,)
				)
			freiepunktidAnfrage = cursor.execute(
					'SELECT id FROM freiepunkteliste WHERE name = ?;',
					(args[0],)
				).fetchone()
			punktId = freiepunktidAnfrage[0]
	else:
		punktId = freiepunktidAnfrage[0]

	punkteWertQuery = cursor.execute(
				'SELECT anzahl '
				'FROM freiepunkte '
				'WHERE userid == ? '
				'AND freiepunkteid = ? '
				';', (userid, punktId,)
			).fetchone()

	if punkteWertQuery is None:
		punkteWert = 0
	else:
		punkteWert = punkteWertQuery[0]


	if len(args) == 2:
		if punkteWert is 0:
			cursor.execute(
						'INSERT INTO freiepunkte '
						'(userid, freiepunkteid, anzahl) '
						'VALUES (?, ?, 0) '
						';', (userid, punktId,)
					)
		cursor.execute(
					'UPDATE freiepunkte '
					'SET anzahl = ? '
					'WHERE userid = ? '
					'AND freiepunkteid = ? '
					';', (punkteWert + 1, userid, punktId)
				)
		print('updating for user', userid, 'with value', punkteWert+1)
		db_connection.commit()
		message = username + ' hat jetzt ' + str(punkteWert + 1)  + ' ' + punktName[1:] + '.'
	else:
		if args[2] in ['-s']:
			message = username + ' hat ' + str(punkteWert)  + ' ' + punktName[1:] + '.'
		elif len(args) < 4:
			message = _help
		else:
			if args[2] == '-a':
				message = 'adding not implemented'
			elif args[2] == '-r':
				message = 'removing not implemented'
			else:
				message = _help

	return helper.botMessage(message, _botname)
