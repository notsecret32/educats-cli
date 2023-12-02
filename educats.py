import sys

import click
import toml


from cli.utils import combine_exclude_modules
from cli.modules.modules_list import ModulesList
from cli.commands import (
    install_modules,
    uninstall_modules,
    reinstall_modules,
    build_modules,
    rebuild_modules,
    show_all_modules
)


# Открываем файл с настройками
try:
    with open('config.toml', 'r') as f:
        config = toml.load(f)
except FileNotFoundError:
    click.echo(click.style(f'Error: config.toml file not found.', fg='red'))
    sys.exit(1)


# Константы из конфигурационного файла
RELATIVE_MODULES_PATH_LIST = config['modules']['relative_modules_path_list']
EXCLUDE_MODULES_FROM_INSTALL = config['modules']['exclude_modules_for_install']
EXCLUDE_MODULES_FROM_UNINSTALL = config['modules']['exclude_modules_for_uninstall']
EXCLUDE_MODULES_FROM_REINSTALL = config['modules']['exclude_modules_for_reinstall']
EXCLUDE_MODULES_FROM_BUILD = config['modules']['exclude_modules_for_build']
EXCLUDE_MODULES_FROM_REBUILD = config['modules']['exclude_modules_for_rebuild']


# Глобальный список модулей
ModulesList.set_global_path_to_modules(RELATIVE_MODULES_PATH_LIST)
global_modules_list = ModulesList(parameter=RELATIVE_MODULES_PATH_LIST)


# Определение команд и их настройка
class CommandOrder(click.Group):
    def __init__(self, *args, **kwargs):
        self.list_commands = None
        self.priorities = {}
        super(CommandOrder, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(CommandOrder, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(CommandOrder, self).list_commands(ctx)
        return (c[1] for c in sorted(
            (self.priorities.get(command, 1), command)
            for command in commands))

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        priority = kwargs.pop('priority', 1)
        priorities = self.priorities

        def decorator(f):
            cmd = super(CommandOrder, self).command(*args, **kwargs)(f)
            priorities[cmd.name] = priority
            return cmd

        return decorator


@click.group(cls=CommandOrder)
def cli():
    pass


@cli.command(priority=1,
             help='Installs the libraries specified in the package.a json file.')
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be installed."
)
@click.option(
    '-e',
    '--exclude',
    multiple=True,
    help="Specifies the names of modules to be excluded."
)
@click.option(
    '-s',
    '--silent',
    is_flag=True,
    help="Specifies whether to output npm logs to the console or not."
)
def install(modules, exclude, silent=False):
    install_modules(
        modules,
        combine_exclude_modules(
            EXCLUDE_MODULES_FROM_INSTALL,
            exclude
        ),
        silent
    )


@cli.command(priority=2,
             help='Deletes the folder node_modules and package-lock.json file (optional).')
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be uninstalled."
)
@click.option(
    '-e',
    '--exclude',
    multiple=True,
    help="Specifies the names of modules to be excluded."
)
@click.option(
    '-p',
    '--package-lock',
    is_flag=True,
    help="Indicates whether to delete the package-lock.json file or not."
)
def uninstall(modules, exclude, package_lock):
    uninstall_modules(
        modules,
        combine_exclude_modules(
            EXCLUDE_MODULES_FROM_UNINSTALL,
            exclude
        ),
        package_lock,
    )


@cli.command(priority=3,
             help='Reinstalls the modules specified in the package.json file.')
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be reinstalled."
)
@click.option(
    '-e',
    '--exclude',
    multiple=True,
    help="Specifies the names of modules to be excluded."
)
@click.option(
    '-s',
    '--silent',
    is_flag=True,
    help="Specifies whether to output npm logs to the console or not."
)
@click.option(
    '-p',
    '--package-lock',
    is_flag=True,
    help="Indicates whether to delete the package-lock.json file or not."
)
def reinstall(selected_modules, exclude_modules, silent, delete_package_lock_file):
    reinstall_modules(
        selected_modules,
        combine_exclude_modules(
            EXCLUDE_MODULES_FROM_REINSTALL,
            exclude_modules
        ),
        silent,
        delete_package_lock_file
    )


@cli.command(priority=4,
             help='Builds modules with the specified configuration.')
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be build."
)
@click.option(
    '-e',
    '--exclude',
    multiple=True,
    help="Specifies the names of modules to be excluded."
)
@click.option(
    '-c',
    '--configuration',
    type=click.Choice(['stage', 'production']),
    default='stage',
    help='Specifies which build configuration to use. [DEFAULT=stage]'
)
def build(selected_modules, exclude_modules, configuration):
    build_modules(
        selected_modules,
        combine_exclude_modules(
            EXCLUDE_MODULES_FROM_BUILD,
            exclude_modules
        ),
        configuration
    )


@cli.command(priority=5,
             help='Rebuilds modules with the specified configuration.')
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be rebuild."
)
@click.option(
    '-e',
    '--exclude',
    multiple=True,
    help="Specifies the names of modules to be excluded."
)
@click.option(
    '-s',
    '--silent',
    is_flag=True,
    help="Specifies whether to output npm logs to the console or not."
)
@click.option(
    '-p',
    '--package-lock',
    is_flag=True,
    help="Indicates whether to delete the package-lock.json file or not."
)
@click.option(
    '-c',
    '--configuration',
    type=click.Choice(['stage', 'production']),
    default='stage',
    help='Specifies which build configuration to use. [DEFAULT=stage]'
)
def rebuild(selected_modules, exclude_modules, silent, delete_package_lock_file, configuration):
    rebuild_modules(
        selected_modules,
        combine_exclude_modules(
            EXCLUDE_MODULES_FROM_REBUILD,
            exclude_modules
        ),
        silent,
        delete_package_lock_file,
        configuration
    )


@cli.command(name='list',
             priority=6,
             help='Displays a list of found modules.')
def list_modules():
    show_all_modules(global_modules_list)


cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(reinstall)
cli.add_command(build)
cli.add_command(rebuild)
cli.add_command(list_modules)


if __name__ == "__main__":
    cli()
