import os
import shutil

import click

from code_quality_tools import pre_commit, runner

AVAILABLE_ENVIRONMENTS = ["docker", "pipenv", "host", "custom"]

check_command = "code-quality run"

ENVIRONMENT_COMMANDS = {
    "docker": "docker run -v=$(pwd):/src -i #DOCKER_IMAGE# bash -c \"%s\"; exit $?;" % check_command,
    "pipenv": "pipenv run %s" % check_command,
    "host": check_command,
}

GIT_FOLDER = './.git/hooks'
PRE_COMMIT_HOOK_PATH = os.path.join(GIT_FOLDER, 'pre-commit')
PRE_COMMIT_TEMPLATE_PATH = pre_commit.__file__


@click.group()
def cli():
    pass


def input_env():
    while True:
        env = input("You should specify env:\n - %s\n" % "\n - ".join(AVAILABLE_ENVIRONMENTS))
        if env in AVAILABLE_ENVIRONMENTS:
            return env


def input_cmd():
    while True:
        cmd = input("You should specify cmd(e.g \"%s\"):\n" % check_command)
        if cmd:
            return cmd


def input_image():
    while True:
        image = input("You should specify image(run docker images to see images):\n")
        if image:
            return image


@cli.command()
@click.option('--env', type=click.Choice(AVAILABLE_ENVIRONMENTS), help='Execute command environment')
@click.option('--cmd', type=str, help='Custom hook command')
@click.option('--image', type=str, help='Image used by docker env')
def install(env, cmd, image):
    if not os.path.exists(GIT_FOLDER):
        return click.echo("Git folder doesn't exists: %s" % GIT_FOLDER)
    if not env:
        env = input_env()
    if env == "custom" and cmd is None:
        cmd = input_cmd()
    if env == 'docker' and image is None:
        image = input_image()

    with open(PRE_COMMIT_TEMPLATE_PATH) as source, open(PRE_COMMIT_HOOK_PATH, 'w+') as dest:
        content = source.read()
        content = content.replace('#COMMAND#', ENVIRONMENT_COMMANDS.get(env, cmd))
        if env == 'docker':
            content = content.replace('#DOCKER_IMAGE#', image)
        dest.write(content)

    os.chmod(PRE_COMMIT_HOOK_PATH, 0o777)

    click.echo('pre-commit hook installed: %s' % PRE_COMMIT_HOOK_PATH)


@cli.command()
def uninstall():
    if not os.path.exists(GIT_FOLDER):
        return click.echo("Git folder doesn't exists: %s" % GIT_FOLDER)
    try:
        os.remove(PRE_COMMIT_HOOK_PATH)
    except FileNotFoundError:
        return click.echo("pre-commit hook not installed")
    return click.echo("pre-commit hook successfully uninstalled")


@cli.command()
def init_configs():
    config_dir = os.path.join(os.path.dirname(PRE_COMMIT_TEMPLATE_PATH), 'configs')
    files = os.listdir(config_dir)
    for file in files:
        shutil.copyfile(os.path.join(config_dir, file), file)


@cli.command()
def run():
    exit(runner.run())


if __name__ == '__main__':
    cli()
