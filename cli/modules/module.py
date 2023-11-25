import os

from cli import EducatsCLI
print(EducatsCLI.get_relative_path_to_global_modules())


class Module:
    def __init__(self, relative_path_to_module: str, **kwargs):
        pass
