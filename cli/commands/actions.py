import click

from cli.modules import global_modules_list
from cli.modules.modules_list import ModulesList, ModulesListActions


def install_modules(modules_list: tuple):
    selected_modules = ModulesList(
        action=ModulesListActions.CREATE_LIST_FROM_MODULES,
        selected_modules=modules_list
    )

    matched_modules, mismatched_modules = global_modules_list.compare(selected_modules)

    for mismatched_module in mismatched_modules:
        click.echo(click.style(f'Warning: {mismatched_module.name} not found.', fg='yellow'))

