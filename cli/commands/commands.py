import click

from cli.modules.modules_list import ModulesList
from cli.utils import (
    run_npm,
    warning,
)


def create_module_list(selected_modules_list,
                       exclude_modules: list):
    if isinstance(selected_modules_list, tuple):
        return ModulesList(
            parameter=selected_modules_list,
            exclude_modules=exclude_modules
        )
    else:
        return selected_modules_list


def install_modules(selected_modules_list,
                    exclude_modules,
                    is_silent_mode: bool):
    modules_list = create_module_list(selected_modules_list, exclude_modules)

    # Код пока не выводит модули, которых были переданы, но их не существует.
    # Чтобы это исправить, необходимо на этапе создания модулей, разделять те, которые есть и тех, которых нет

    if not modules_list.is_empty():
        for module in modules_list:
            if module.has('package.json'):
                run_npm(f"npm install --force {'--silent' if is_silent_mode else ''}", module.absolute_path)
            else:
                warning(f'Warning: package.json not found in {module.name.upper()} module.')
    else:
        warning(f'Warning: no modules to install.')


def uninstall_modules(selected_modules_list: tuple,
                      exclude_modules,
                      delete_package_lock_file: bool):
    modules_list = create_module_list(selected_modules_list, exclude_modules)

    if not modules_list.is_empty():
        for module in modules_list:
            module.delete_files('package-lock.json', delete_package_lock_file)
            module.delete_files('node_modules', True)
    else:
        warning('Warning: no modules to uninstall.')


def reinstall_modules(selected_modules_list: tuple,
                      exclude_modules: list,
                      is_silent_mode: bool,
                      delete_package_lock_file: bool):
    modules_list = create_module_list(selected_modules_list, exclude_modules)
    uninstall_modules(modules_list, exclude_modules, delete_package_lock_file)
    install_modules(modules_list, exclude_modules, is_silent_mode)


def build_modules(selected_modules_list: tuple,
                  exclude_modules,
                  configuration: str):
    modules_list = ModulesList(
        parameter=selected_modules_list,
        exclude_modules=exclude_modules
    )

    if not modules_list.is_empty():
        for module in modules_list:
            if module.has('package.json'):
                run_npm(f'npm build -- --configuration={configuration}')
            else:
                warning(f'Warning: package.json not found in {module.name.upper()} module.')
    else:
        warning('Warning: no modules to build')


def rebuild_modules(selected_modules_list: tuple,
                    exclude_modules: list,
                    is_silent_mode: bool,
                    delete_package_lock_file: bool,
                    configuration: str):
    modules_list = create_module_list(selected_modules_list, exclude_modules)
    reinstall_modules(selected_modules_list=modules_list, is_silent_mode=is_silent_mode, delete_package_lock_file=delete_package_lock_file)
    build_modules(selected_modules_list=modules_list, configuration=configuration)


def show_all_modules(global_modules_list):
    for module in global_modules_list:
        click.echo(f'{module.name}: {module.absolute_path}')
