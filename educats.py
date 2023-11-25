import click

from cli.commands import (
    install_modules,
    uninstall_modules,
    reinstall_modules,
    build_modules,
    rebuild_modules
)


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


@cli.command(priority=1)
def install(selected_modules):
    install_modules(selected_modules)


@cli.command(priority=2)
def uninstall(selected_modules, delete_package_lock_file):
    uninstall_modules(selected_modules, delete_package_lock_file)


@cli.command(priority=3)
def reinstall(selected_modules, delete_package_lock_file):
    reinstall_modules(selected_modules, delete_package_lock_file)


@cli.command(priority=4)
def build(selected_modules, configuration):
    build_modules(selected_modules, configuration)


@cli.command(priority=5)
def rebuild(selected_modules, delete_package_lock_file, configuration):
    rebuild_modules(selected_modules, delete_package_lock_file, configuration)


@cli.command(name='list', priority=6)
def list_modules():
    pass


cli.add_command(install)
cli.add_command(uninstall)
cli.add_command(reinstall)
cli.add_command(build)
cli.add_command(rebuild)
cli.add_command(list_modules)


if __name__ == "__main__":
    cli()
