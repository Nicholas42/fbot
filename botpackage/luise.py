_botname = 'Lusie'
_help = 'usage: !' + _botname + ' [ping|ud expr]'

from botpackage.helper import helper, ud

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
	else:
		return helper.botMessage(_help, _botname)
