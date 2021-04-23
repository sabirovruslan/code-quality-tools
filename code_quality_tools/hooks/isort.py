from code_quality_tools.cmd import run_cmd


def isort_hook(files):
    *_, return_code = run_cmd(['isort', '-c', *files])
    output = ''
    if return_code != 0:
        output, *_ = run_cmd(['isort', *files])
    return output, return_code
