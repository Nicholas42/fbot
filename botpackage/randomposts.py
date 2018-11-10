import random

from botpackage.helper import helper

_randompost_propability = 500
_names = {
	'manf':['Hack the planet!','Paladschinken'],
	'kathie':['Ich bin nicht putzig.','Kathie'],
	'luise':['Lalalalalalalalalalala','Luise'],
	'nicholas':['Knuddeln ist Sport.','Nicholas']
}


def processMessage(args, rawMessage, db_connection):
	if random.randrange(_randompost_propability) == 0:
		msg_obj = _names[random.choice(list(_names))]
		return helper.botMessage(msg_obj[0], msg_obj[1])
	return
