import argparse


class ArgumentError(Exception):
    def __init__(self, prog, msg):
        self.prog = prog
        self.msg = msg

    def __str__(self):
        return self.msg


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True):
        super().__init__(prog=prog,
                    usage=usage,
                    description=description,
                    epilog=epilog,
                    parents=parents,
                    formatter_class=formatter_class,
                    prefix_chars=prefix_chars,
                    fromfile_prefix_chars=fromfile_prefix_chars,
                    argument_default=argument_default,
                    conflict_handler=conflict_handler,
                    add_help=False,
                    allow_abbrev=allow_abbrev)
    def exit(self, status=0, message=None):
        raise ArgumentError(self.prog, msg)
    def error(self, msg):
        raise ArgumentError(self.prog, msg)

    def _print_message(self, message, file=None):
        pass
