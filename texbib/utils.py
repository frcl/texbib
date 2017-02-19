import sys


def runtime_action(msg, action='tell'):
    print('texbib:', msg)
    if action == 'fail':
        sys.exit(1)


class CmdTracker(dict):

    def register(self, cmd_func):
        self[cmd_func.__name__] = cmd_func
        return cmd_func
