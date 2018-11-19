import botpackage.helper.calc as calc
import botpackage.helper.timeout as timeout
from botpackage.helper import helper
from botpackage.helper.mystrip import stripFromBegin, _space_chars

_botname = '۞'
_bottrigger = 'calc'
_help = '%s <mathematischer Ausdruck>'%_bottrigger

def processMessage(args, rawMessage, db_connection):
	return
    if len(args) < 1 or args[0].lower() != "!" + _bottrigger:
        return

    expr = stripFromBegin(rawMessage["message"], ["!" + _bottrigger]).strip(''.join(_space_chars))

    ret = timeout.timed_run(calc.evaluate, [expr])

    if isinstance(ret, Exception):
        return helper.botMessage("Ein Fehler trat auf: %s"%ret, _botname)
    elif ret is None:
        return helper.botMessage("Die Evaluierung dauerte zu lange.", _botname)
    else:
        return helper.botMessage("%s"%ret, _botname)
