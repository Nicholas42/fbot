_botname = 'lusie'
_help = 'usage: !' + _botname + ' ping'

from botpackage.helper import helper

def processMessage(args, name):
	if len(args) < 2:
		return None

	if args[0].lower() != '!' + _botname:
		return

	if args[1] == 'ping':
		message = 'pong'
	else:
		message = _help

	return helper.botMessage(message, _botname)
