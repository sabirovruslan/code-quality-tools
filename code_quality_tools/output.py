import sys


class Colors:
    RED = '\033[101m'
    GREEN = '\033[102m'
    RESET = '\033[0m'


def write(message, color=None):
    if color is not None:
        message = color + message + Colors.RESET
    sys.stdout.write(message)
    sys.stdout.flush()


def writeln(message, color=None):
    write(message, color)
    write('\n')
