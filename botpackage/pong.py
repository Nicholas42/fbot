def processMessage(args):
	if len(args) < 2:
		return None

	if args[0] == '!fbot' \
			and args[1] == 'ping':
		return {'name' : 'fbot', 'message' : 'pong'}
