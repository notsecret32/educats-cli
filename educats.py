"""
Команда: install
Описание: Устанавливает зависимости из package.json
Параметры:
    1) -m, --modules MODULES_LIST Список модулей, которые надо установить (-m "admin subject test)

Команда: remove
Описание: Удаляет package-lock.json и node_modules
Параметры:
    1) -m, --modules MODULES_LIST Список модулей, которые надо очистить (-m "admin subject test)

Команда: build
Описание: Собирает модули нужной конфигурации
Параметры:
    1) -m, --modules MODULES_LIST Список модулей, которые надо очистить (-m "admin subject test)
    2) -c, --configuration [stage|production] DEFAULT=stage

Команда: reinstall
Описание: Объединение команды remove -> install
Параметры:
    1) -m, --modules MODULES_LIST Список модулей, которые надо очистить (-m "admin subject test)

Команда: rebuild
Описание: Собирает модули заданного типа. Объединение команды remove, install, build
Параметры:
    1) -m, --modules MODULES_LIST Список модулей, которые надо ребилдить (-m "admin subject test)
    2) -c, --configuration [stage|production] DEFAULT=stage
"""
import os
import sys
import toml
import click
import shutil
import subprocess

from tqdm import tqdm


try:
    with open('config.toml', 'r') as f:
        config = toml.load(f)
except FileNotFoundError:
    click.echo(click.style('Error: The pyproject.toml file could not be found', fg='red'))


# Constants
RELATIVE_MODULES_PATH = config['modules']['relative_modules_directory']
EXCLUDE_DIRECTORIES = config['modules']['exclude_directories']


def get_selected_modules(modules):
    modules_list = list(modules)
    result = [module for modules in modules_list for module in modules.split()]
    return result or []


def search_modules_path(modules=None, depth=1) -> dict:
    if modules is None:
        modules = []

    result = {}
    unique_modules = set(modules)

    for relative_module_directory in RELATIVE_MODULES_PATH:
        absolute_module_directory = os.path.realpath(relative_module_directory)

        for root, dirs, files in os.walk(absolute_module_directory, topdown=True):
            current_level = root[len(absolute_module_directory):].count(os.sep)
            current_work_directory = os.path.basename(os.path.normpath(root))

            if (
                (current_work_directory in unique_modules or not unique_modules)
                and current_work_directory not in EXCLUDE_DIRECTORIES
            ):
                result[current_work_directory] = root

            if current_level >= depth:
                dirs[:] = []

    return result


def install_modules(modules_path: dict):
    for module_name, module_path in modules_path.items():
        for _, _, files in os.walk(module_path):
            if 'package.json' in files:
                try:
                    click.echo(click.style(
                        f'{module_name}: The process of installing packages has started.',
                        fg='green'
                    ))

                    subprocess.check_call(
                        'npm install --force --silent',
                        shell=True,
                        cwd=module_path,
                    )

                    click.echo(click.style(
                        f'{module_name}: Packages have been installed successfully.',
                        fg='green'
                    ))
                except subprocess.CalledProcessError as ex:
                    click.echo(click.style(
                        f'{module_name}: {ex}',
                        fg='red'
                    ))
                    sys.exit(1)

            else:
                click.echo(click.style(f'No package.json file in {module_name} module.', fg='red'))
            break


def uninstall_modules(modules_path: dict):
    for module_name, module_path in modules_path.items():
        files_to_remove = []
        dirs_to_remove = []

        click.echo(click.style(
            f'{module_name}: The process of uninstalling packages has started.',
            fg='green'
        ))

        for root, dirs, files in os.walk(module_path, topdown=False):
            if 'package-lock.json' in files:
                files_to_remove.append(os.path.join(root, 'package-lock.json'))

            if 'node_modules' in dirs:
                dirs_to_remove.append(os.path.join(root, 'node_modules'))

        total_files = len(files_to_remove) + len(dirs_to_remove)

        if total_files > 0:
            with tqdm(total=total_files, desc=module_name, ncols=80) as progressbar:
                for file in files_to_remove:
                    os.remove(file)
                    progressbar.update(1)

                for dir in dirs_to_remove:
                    shutil.rmtree(dir)
                    progressbar.update(1)
        else:
            click.echo(click.style(
                f'Warning: Could not find package-lock.json or node_modules in the {module_name} module.',
                fg='yellow'
            ))
            break

        click.echo(click.style(
            f'{module_name}: Packages have been uninstalled successfully.',
            fg='green'
        ))


def build_modules(modules_path: dict, configuration):
    for module_name, module_path in modules_path.items():
        for _, _, files in os.walk(module_path):
            if 'package.json' in files:
                try:
                    click.echo(click.style(
                        f'{module_name}: The process of building module has started.',
                        fg='green'
                    ))

                    subprocess.check_call(f'npm run build -- --configuration={configuration}', shell=True, cwd=module_path)

                    click.echo(click.style(
                        f'{module_name}: The package was successfully built.',
                        fg='green'
                    ))
                except subprocess.CalledProcessError as ex:
                    click.echo(click.style(
                        f'{module_name}: {ex}',
                        fg='red'
                    ))
                    sys.exit(1)
            else:
                click.echo(click.style(f'No package.json file in {module_name} module.', fg='red'))

            break


class OrderCommands(click.Group):
    def list_commands(self, ctx: click.Context):
        return list(self.commands)


@click.group()
def cli():
    pass


@cli.command(
    help='Installs the project packages specified in package.json file.'
)
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be installed."
)
def install(modules):
    modules = get_selected_modules(modules)
    modules_path = search_modules_path(modules)
    install_modules(modules_path)


@cli.command(
    help='Deletes the project packages specified in package.json file.'
)
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help="Specifies the name of the modules to be deleted."
)
def uninstall(modules):
    modules = get_selected_modules(modules)
    modules_path = search_modules_path(modules)
    uninstall_modules(modules_path)


@cli.command(
    help='Removes packages from the module and then installs them.'
)
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help='Specifies the name of modules to be reinstalled.'
)
def reinstall(modules):
    modules_list = get_selected_modules(modules)
    modules_path = search_modules_path(modules_list)
    uninstall_modules(modules_path)
    install_modules(modules_path)


@cli.command(
    help='Starts the module build.'
)
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help='Specifies the name of modules to be build.'
)
@click.option(
    '-c',
    '--configuration',
    type=click.Choice(['stage', 'production']),
    default='stage',
    help='Specifies which build configuration to use. [DEFAULT=stage]'
)
def build(modules, configuration):
    modules_list = get_selected_modules(modules)
    modules_path = search_modules_path(modules_list)
    build_modules(modules_path, configuration)


@cli.command(
    help='First reinstall packages, and then builds them.'
)
@click.option(
    '-m',
    '--modules',
    multiple=True,
    help='Specifies the name of modules to be rebuild.'
)
@click.option(
    '-c',
    '--configuration',
    type=click.Choice(['stage', 'production']),
    default='stage',
    help='Specifies which build configuration to use. [DEFAULT=stage]'
)
def rebuild(modules, configuration):
    modules_list = get_selected_modules(modules)
    modules_path = search_modules_path(modules_list)
    uninstall_modules(modules_path)
    install_modules(modules_path)
    build_modules(modules_path, configuration)


@cli.command(
    name='list',
    help='Displays a list of found modules.'
)
def list_modules():
    modules_path = search_modules_path()

    if not modules_path:
        click.echo(click.style(
            ''.join((
                "Warning: The list of available modules is empty.",
                "\nChange the search folders in the pyproject.toml file."
            )),
            fg='yellow')
        )

    for key, value in modules_path.items():
        click.echo("{0}: {1}".format(key, value))


cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(reinstall)
cli.add_command(build)
cli.add_command(rebuild)
cli.add_command(list_modules)


if __name__ == '__main__':
    cli()
