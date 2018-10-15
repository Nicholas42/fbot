_botname = 'Luise'
_help = 'usage: !' + _botname + ' ping'


def processMessage(args, name):
	if len(args) < 2:
		return None

	if args[0] != '!' + _botname:
		return

	if args[1] == 'ping':
		message = 'pong'
	else:
		message = _help

	return {'name' : 'fbot', 'message' : message}
