import hashlib
from botpackage.helper import helper, ud

_botname = 'Lusie'
_help = 'usage: !' + _botname + ' [ping|ud expr]'


def processMessage(args, rawMessage, db_connection):
	if len(args) < 2:
		return None

	if args[0].lower() != '!' + _botname.lower():
		return

	if args[1] == 'ping':
		return helper.botMessage('pong', _botname)
	elif args[1].lower() == 'ud':
		return
		if len(args) < 2:
			return
		return helper.botMessage(ud.ud_parser(args[2]), _botname)
	elif args[1].lower() == 'decide':
		if len(args) < 2:
			return
		antwort = '+' if ord(hashlib.sha1((rawMessage['message'].encode()+b'tpraR4gin8XHk_t3bGHZTJ206qc9vyV7LlUMTf655LNJDKGciVXKRLijqGkHgkpW <= Manfreds schlimmstes Geheimnis')).hexdigest()[0]) % 2 == 1 else '-'
		# ~ print(rawMessage['message'])
		return helper.botMessage(antwort, _botname)
		return
	elif args[1].lower() == 'sing':
		return helper.botMessage('lalalala', _botname)
	else:
		return helper.botMessage(_help, _botname)
