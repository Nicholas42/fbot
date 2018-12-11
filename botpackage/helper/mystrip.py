_space_chars = ' \t\n\u200b'

def stripFromBegin(s : str, a : list):
	if len(a) == 0:
		return s
	return stripFromBegin(
			s[s.find(a[0]) + len(a[0]):], a[1:]). \
			lstrip(_space_chars)


def norm(name):
    return name.lower().strip(_space_chars)
