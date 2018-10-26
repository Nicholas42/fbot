_botname = 'Lusie'
_help = 'usage: !' + _botname + ' ping'

from botpackage.helper import helper, ud

def processMessage(args, rawMessage, db_connection):
	if len(args) < 2:
		return None

	if args[0].lower() != '!' + _botname.lower():
		return

	if args[1] == 'ping':
		message = 'pong'
	elif args[1].lower() == 'ud':
		if len(args) < 2:
			return helper.botMessage(_help_ud, _botname)
		return helper.botMessage(ud.ud_parser(args[2]), _botname)
	else:
		message = _help

	return helper.botMessage(message, _botname)
