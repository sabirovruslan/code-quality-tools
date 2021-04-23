from code_quality_tools.cmd import run_cmd


def diff_files():
    return set(diff_cached() + diff_no_cached())


def diff_cached():
    cmd_params = ['git', 'diff', '--cached', '--name-only', '--diff-filter', 'ACM']
    output, *_ = run_cmd(cmd_params)
    return parse_py_files(output)


def diff_no_cached():
    cmd_params = ['git', 'diff', '--name-only', '--diff-filter', 'ACM']
    output, *_ = run_cmd(cmd_params)
    return parse_py_files(output)


def parse_py_files(output):
    print(output)
    return list(filter(lambda x: x.endswith('.py'), output.split('\n')))
