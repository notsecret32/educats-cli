import click


@click.group()
def cli():
    pass


@click.command()
@click.option('--modules', default='*', help='Enumeration of modules to be installed')
@click.argument("modules_list")
def install(modules, modules_list):
    click.echo(f'command install with option {modules} and args {modules_list}')


cli.add_command(install)


if __name__ == "__main__":
    cli()
