import os
import click
import subprocess


def convert_tuple_to_list(modules_list: tuple):
    return [module for modules in list(modules_list) for module in modules.split()]


def combine_exclude_modules(default_exclude_modules: list, selected_exclude_modules: tuple):
    converted_exclude_modules = convert_tuple_to_list(selected_exclude_modules)
    return list(set(default_exclude_modules + converted_exclude_modules))


def run_npm(cmd: str, path: str = None):
    try:
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=path)
        return result
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"Error: An unexpected error has occurred.", fg='red'))
        error_lines = e.stderr.decode("utf-8").splitlines()
        for line in error_lines:
            click.echo(click.style(line, fg='red'))


def success(message: str):
    click.echo(click.style(message, fg='green'))


def warning(message: str):
    click.echo(click.style(message, fg='yellow'))


def error(message: str):
    click.echo(click.style(message, fg='red'))