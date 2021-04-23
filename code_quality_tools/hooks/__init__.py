from code_quality_tools.hooks.black import black_hook
from code_quality_tools.hooks.flake8 import flake8_hook
from code_quality_tools.hooks.isort import isort_hook
from code_quality_tools.hooks.seed_isort import seed_isort_hook


HOOKS = [
    seed_isort_hook,
    isort_hook,
    black_hook,
    flake8_hook
]
