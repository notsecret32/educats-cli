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
import click


@click.group()
def cli():
    pass


@click.command()
@click.option('-m', '--modules', multiple=True, help='List of modules to install')
def install(modules):
    pass


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
