if __name__ == "__main__":
    import sys
    import toml
    import click

    from cli.commands.commands import cli
    from cli.modules import initialize_global_modules
    from cli.modules.modules_list import ModulesList, ModulesListActions

    try:
        with open('config.toml', 'r') as f:
            config = toml.load(f)
    except FileNotFoundError:
        click.echo(click.style(f'Error: config.toml not found.', fg='red'))
        sys.exit(1)

    relative_path_to_modules = config['modules']['relative_modules_path_list']
    initialize_global_modules(ModulesList(
        ModulesListActions.CREATE_LIST_FROM_PATH,
        relative_path_to_modules=relative_path_to_modules
    ))

    cli()
