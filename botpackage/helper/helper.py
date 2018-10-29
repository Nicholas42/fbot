def botMessage(message, name='fbot'):
	return {'name' : name, 'message' : message}


def useridFromUsername(cursor, username):
	query = cursor.execute(
				'SELECT userid '
				'FROM nicknames '
				'WHERE lower(nickname) == ? '
				';', (username.lower(),)
			).fetchone()
	return None if query is None else query[0]


def usernameFromUserid(cursor, userid):
	query = cursor.execute(
				'SELECT nickname '
				'FROM nicknames '
				'WHERE userid == ? '
				'AND deletable == 1'
				';', (userid, )).fetchone()
	return query[0]
