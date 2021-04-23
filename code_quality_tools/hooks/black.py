import subprocess

from code_quality_tools.cmd import run_cmd


def black_hook(files):
    *_, return_code = run_cmd(['black', '--check', *files], out=subprocess.DEVNULL)
    output = ''
    if return_code != 0:
        _, output, _ = run_cmd(['black', *files])
    return output, return_code
