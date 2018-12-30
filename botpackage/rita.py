import re
import hashlib
import random

import botpackage.helper.argparse as argparse # ~ import argparse
from botpackage.helper import helper, ud
from botpackage.helper.mystrip import stripFromBegin, _space_chars
import botpackage.helper.youtube as youtube
from varspace.settings import botMasters


_botname = 'Dr. Ritastein'
_bottrigger = 'rita'
_usageTemplate = 'usage: !' + _bottrigger + ' '
_help = _usageTemplate + '[decide|ping|sing|ud] [args]'
_help_ud = _usageTemplate + 'ud <expr>'
_slap_trigger = 'slap'
_featurerequest_trigger = 'featurerequest'


def processMessage(args, rawMessage, db_connection):
	if len(args) < 2:
		return None

	if args[0].lower() != '!' + _bottrigger.lower():
		return

	if args[1] == 'ping':
		return helper.botMessage('Hallu', _botname)

	elif args[1].lower() == 'ud':
		if len(args) <= 2:
			return helper.botMessage(_help_ud, _botname)
		term = stripFromBegin(rawMessage['message'], args[0:2])
		return helper.botMessage(ud.ud_parser(term), _botname)

	elif args[1].lower() == 'decide':
		if len(args) < 2:
			return
		antwort = '+' if ord(hashlib.sha1((rawMessage['message'].encode()+b'tpraR4gin8XHk_t3bGHZTJ206qc9vyV7LlUMTf655LNJDKGciVXKRLijqGkHgkpW <= Manfreds schlimmstes Geheimnis')).hexdigest()[0]) % 2 == 1 else '-'
		return helper.botMessage(antwort, _botname)

	elif args[1].lower() == 'sing':
		parser = argparse.ArgumentParser(prog='!rita sing')
		parser.add_argument('song', nargs='?')
		parser.add_argument('-l', '--learn', action='store_true', dest='learn')
		parser.add_argument('-r', '--remove', action='store_true', dest='remove')
		parser.add_argument('-h', '--help', action='store_true')
		parser.add_argument('-v', '--version', action='store_true') # needed
		try:
			parsedArgs = vars(parser.parse_known_args(args[2:])[0])
		except argparse.ArgumentError:
			return helper.botMessage(parser.print_usage(), _botname)

		if (( parsedArgs['learn'] or parsedArgs['remove'] ) and parsedArgs['song'] == None) or \
					parsedArgs['help']:
			return helper.botMessage(parser.format_usage().rstrip('\n'), _botname)
		elif parsedArgs['version']:
			return helper.botMessage('secret unlocked \o/ the first one calling w/ID gets some chocolate', _botmessage)

		if parsedArgs['learn']:
			return learntosing(parsedArgs['song'], db_connection)
		elif parsedArgs['remove']:
			if rawMessage['username'] in botMasters:
				return removeasong(parsedArgs['song'], db_connection)
			else:
				return helper.botMessage('ich habehabe einein Messer', _botname)

		return helper.botMessage(singasong(db_connection.cursor()), _botname)

	elif args[1].lower() in [_slap_trigger, _featurerequest_trigger]:
		if len(args) == 2:
			return helper.botMessage('was meinst du?', _botname)

		target = stripFromBegin(rawMessage['message'], args[0:2])
		if args[1] == _slap_trigger:
			return helper.botMessage('%s schlägt %s'%(_botname.replace('Dr. Ritastein', 'Rita'), target), _botname)
		elif args[1] == _featurerequest_trigger:
			return helper.botMessage('Ich will %s'%target, _botname)

	else:
		return helper.botMessage(_help, _botname)



def learntosing(link, db_connection):
		cursor = db_connection.cursor()
		# ~ if e['user_id'] in self.singbans:
			# ~ return helper.botMessage(message = "Ich hab Niveau!", _botname)
		link = link.replace('http://','https://').strip(_space_chars)
		if link.startswith('youtube') or link.startswith('youtu.be'):
			link = 'https://www.' + link
		elif link.startswith('www.'):
			link = 'https://'+s
		link = link.replace('youtube.de/','youtube.com/')
		link = link.replace('youtu.be/','youtube.com/watch?v=')
		link = link.replace('&feature=youtu.be', '')
		p=re.compile('^https:\/\/www.youtube.com\/watch\?v=[a-zA-Z0-9\-_]{,20}$')
		if not p.match(link):
			return helper.botMessage("Die url passt nicht ganz.", _botname)
		query = cursor.execute(
					"SELECT id FROM songs WHERE link = ?;", (link,)
				).fetchone()
		if query is not None:
			return helper.botMessage("Das kenn ich schon.", _botname)
		# ~ vid_id = link.partition("?v=")[2]
		# ~ vid_name = youtube.title(vid_id)
		# ~ if not vid_name:
			# ~ return helper.botMessage('Das Video gibts doch gar nicht..'%vid_name, _botname)
		# ~ print(vid_name)
		cursor.execute("INSERT INTO songs (link) VALUES (?);", (link,))
		db_connection.commit()
		return helper.botMessage('Ich kann jetzt was Neues singen: %s'%link, _botname)


def songCount(cursor):
	return cursor.execute(
				'SELECT COUNT(*) FROM songs;'
			).fetchone()[0]


def singasong(cursor):
	anzahl = songCount(cursor)
	if anzahl is 0:
		return 'ICH KANN NICHT SINGEN!'
	songids = [x[0] for x in cursor.execute('SELECT id FROM songs;').fetchall()]
	return cursor.execute(
				'SELECT link FROM songs WHERE id = ?',
				(random.choice(songids),)
			).fetchone()[0]


def removeasong(link, db_connection):
	cursor = db_connection.cursor()
	songid = cursor.execute(
				'SELECT id FROM songs WHERE link == ?;', (link,)
			).fetchone()
	if songid is None:
		return helper.botMessage('Ich kenne %s nicht.'%link, _botname)
	cursor.execute('DELETE FROM songs WHERE id == ?;', (songid[0],))
	db_connection.commit()
	return helper.botMessage('Ich kann jetzt %s nicht mehr singen.'%link, _botname)
