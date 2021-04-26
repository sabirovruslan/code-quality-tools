import io
import re

from setuptools import setup, find_packages

project_name = 'code_quality_tools'

with io.open('code_quality_tools/__init__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='code_quality_tools',
    version=version,
    packages=find_packages(exclude=['tests']),
    python_requires=">=3.9",
    package_data={
        'code_quality_tools': ['configs/*.toml', 'configs/.flake8', 'configs/.isort.cfg'],
    },
    install_requires=[
        'aspy.refactor_imports',
        'black',
        'click',
        'flake8-bandit',
        'flake8-bugbear',
        'flake8-comprehensions',
        'flake8-mutable',
        'isort',
        'radon',
    ],
    entry_points={
        "console_scripts": [
            "code-quality=code_quality_tools.cli:cli",
        ]
    },
)
