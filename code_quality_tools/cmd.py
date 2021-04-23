import subprocess


def parse_output(output):
    if output is None:
        return ''
    return output.decode('utf-8')


def run_cmd(cmd, out=subprocess.PIPE):
    """
    :param cmd: Shell command to execute, e.g. ['ls', '-la']
    :param out: Where send output
    :return: tuple(stdout_output, stderr_output, exit_code)
    """
    process = subprocess.Popen(cmd, stdout=out, stderr=out)
    stdout, stderr = process.communicate()
    return parse_output(stdout), parse_output(stderr), process.returncode
