from code_quality_tools.cmd import run_cmd


def flake8_hook(files):
    output, _, return_code = run_cmd(['flake8', *files])
    return output, return_code
