from code_quality_tools import git, output
from code_quality_tools.hooks import HOOKS

MAX_MESSAGE_LEN = 70
ADJUST_FILL_CHAR = '.'


def run():
    exit_code = 0
    diff_files = git.diff_files()
    if not diff_files:
        output.writeln('No *.py files to commit')
        return exit_code

    for hook in HOOKS:
        output.write(hook.__name__.ljust(MAX_MESSAGE_LEN, ADJUST_FILL_CHAR))
        command_output, return_code = hook(diff_files)
        exit_code += return_code
        if return_code > 0:
            output.writeln('Failed', color=output.Colors.RED)
            output.writeln('hook_id: %s\n' % hook.__name__)
            output.writeln(command_output)
        else:
            output.writeln('Passed', color=output.Colors.GREEN)

    return exit_code


if __name__ == '__main__':
    exit(run())
