import ast
import io
import os
import os.path
import re

from aspy.refactor_imports.classify import ImportType
from aspy.refactor_imports.classify import classify_import

SUPPORTED_CONF_FILES = ['.isort.cfg', 'pyproject.toml']
THIRD_PARTY_RE = re.compile(r'^known_third_party(\s*)=(\s*?)[^\s]*$', re.M)
KNOWN_OTHER_RE = re.compile(
    r'^known_((?!third_party)\w+)\s*=\s*([^\s]*)$', re.M,
)


class Visitor(ast.NodeVisitor):
    def __init__(self, appdirs=('.',)):
        self.appdirs = appdirs
        self.third_party = set()

    def _maybe_append_name(self, name):
        name, _, _ = name.partition('.')
        imp_type = classify_import(name, self.appdirs)
        if imp_type == ImportType.THIRD_PARTY:
            self.third_party.add(name)

    def visit_Import(self, node):
        if node.col_offset == 0:
            for name in node.names:
                self._maybe_append_name(name.name)

    def visit_ImportFrom(self, node):
        if node.col_offset == 0:
            if not node.level:
                self._maybe_append_name(node.module)


def third_party_imports(filenames, appdirs=('.',)):
    visitor = Visitor(appdirs)
    for filename in filenames:
        with open(filename, 'rb') as f:
            visitor.visit(ast.parse(f.read(), filename=filename))
    return visitor.third_party


def get_all_files(directory, ext='.py'):
    result = []
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith(ext):
                result.append(os.path.join(path, name))
    return result


def seed_isort_hook(*args, **kwargs):
    """
    Found third party packages and populates "known_third_party" in .isort.cfg
    :return:
    """
    app_dir = '.'
    filenames = get_all_files(app_dir)
    third_party = third_party_imports(filenames, [app_dir])
    for filename in SUPPORTED_CONF_FILES:
        filename = os.path.join(app_dir, filename)
        if not os.path.exists(filename):
            continue

        with io.open(filename, encoding='UTF-8') as f:
            contents = f.read()

        for match in KNOWN_OTHER_RE.finditer(contents):
            third_party -= set(match.group(2).split(','))

        if THIRD_PARTY_RE.search(contents):
            third_party = ','.join(sorted(third_party))
            if filename.endswith('.toml'):
                third_party = '"%s"' % third_party
            replacement = r'known_third_party\1=\2{}'.format(third_party)
            new_contents = THIRD_PARTY_RE.sub(replacement, contents)
            if new_contents == contents:
                return third_party + '\n', 0
            else:
                with io.open(filename, 'w', encoding='UTF-8') as f:
                    f.write(new_contents)
                return third_party + '\n', 0

    return "Cannot perform operation", 1
