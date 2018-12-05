import argparse


class ArgumentError(Exception):
    def __init__(self, prog, msg):
        self.prog = prog
        self.msg = msg

    def __str__(self):
        return self.msg

# ~ class _HelpAction(argparse._HelpAction):
    # ~ def __call__(self, parser, namespace, values, option_string=None):
        # ~ pass

class ArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        raise ArgumentError(self.prog, msg)
    def print_help(self, file=None):
        pass
