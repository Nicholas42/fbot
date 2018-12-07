import argparse


class ArgumentError(Exception):
    def __init__(self, prog, msg):
        self.prog = prog
        self.msg = msg

    def __str__(self):
        return self.msg

class ArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        raise ArgumentError(self.prog, msg)
    def exit(self, status=0, message=None):
        raise ArgumentError(self.prog, message)

    def format_help(self):
        pass
