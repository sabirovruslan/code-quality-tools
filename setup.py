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
    python_requires=">=3.7",
    package_data={
        'code_quality_tools': ['configs/*.toml', 'configs/.flake8', 'configs/.isort.cfg'],
    },
    install_requires=[
        'aspy.refactor_imports==0.5.3',
        'black==18.9b0',
        'click>=6.7',
        'flake8-bandit==2.0.0',
        'flake8-bugbear==18.8.0',
        'flake8-comprehensions==1.4.1',
        'flake8-mutable==1.2.0',
        'isort==4.3.4',
        'radon==2.4.0',
    ],
    entry_points={
        "console_scripts": [
            "code-quality=code_quality_tools.cli:cli",
        ]
    },
)
