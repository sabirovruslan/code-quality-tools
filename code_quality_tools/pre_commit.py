#!/usr/bin/env python

import subprocess


"""
Pre-commit hook template
"""


COMMAND = '#COMMAND#'


def main():
    return subprocess.call(COMMAND, shell=True)


if __name__ == '__main__':
    exit(main())
