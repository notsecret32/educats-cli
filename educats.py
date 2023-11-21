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
import toml
import click


with open('pyproject.toml', 'r') as f:
    config = toml.load(f)


# Constants
RELATIVE_MODULES_PATH = config['modules']['relative_modules_directory']


def get_selected_modules(modules):
    modules_list = list(modules)
    result = [module for modules in modules_list for module in modules.split()]
    return result or []


def search_modules_path(modules, depth=1) -> dict:
    result = {}
    unique_modules = set(modules)

    for relative_module_directory in RELATIVE_MODULES_PATH:
        absolute_module_directory = os.path.realpath(relative_module_directory)

        for root, dirs, files in os.walk(absolute_module_directory, topdown=True):
            current_level = root[len(absolute_module_directory):].count(os.sep)
            current_work_directory = os.path.basename(os.path.normpath(root))

            if (
                (current_work_directory in unique_modules or not unique_modules)
                and current_work_directory != 'node_modules'
            ):
                result[current_work_directory] = root

            if current_level >= depth:
                dirs[:] = []

    return result


@click.group()
def cli():
    pass


@click.command()
@click.option('-m', '--modules', multiple=True, help='List of modules to install')
def install(modules):
    modules = get_selected_modules(modules)
    modules_path = search_modules_path(modules)
    for key, value in modules_path.items():
        click.echo("{0}: {1}".format(key, value))


@click.command()
@click.option('-m', '--modules', multiple=True, help='List of modules to remove')
def remove(modules):
    click.echo(modules)


@click.command()
@click.option('-m', '--modules', multiple=True, help='List of modules to build')
@click.option('-c', '--configuration', type=click.Choice(['stage', 'production']), help='Specifies which build configuration to use')
def build(modules, configuration):
    click.echo(modules)
    click.echo(configuration)


@click.command()
def reinstall():
    pass


@click.command()
def rebuild():
    pass


cli.add_command(install)
cli.add_command(remove)
cli.add_command(build)
cli.add_command(reinstall)
cli.add_command(rebuild)


if __name__ == '__main__':
    cli()
