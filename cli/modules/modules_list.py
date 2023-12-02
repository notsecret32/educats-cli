import os.path

from cli.modules.module import Module


class ModulesList:
    _modules_list = []
    _relative_path_to_modules = []

    def __init__(self, parameter=None, **kwargs):
        if parameter is None:
            self._modules_list = []
        elif isinstance(parameter, list):
            self._modules_list = [Module(rp) for rp in parameter]
        elif isinstance(parameter, tuple):
            if parameter:
                exclude_modules = kwargs.get('exclude_modules')
                converted_modules_names = parameter[0].split()
                self._modules_list = [Module(relative_path) for relative_path in ModulesList._relative_path_to_modules
                                      if os.path.basename(os.path.normpath(relative_path)) in converted_modules_names
                                      and os.path.basename(os.path.normpath(relative_path)) not in exclude_modules]
        else:
            raise AttributeError(f'Error: impossible combination of parameters.')

    def __str__(self):
        return f'Modules List: {self._modules_list}'

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self._modules_list):
            module = self._modules_list[self.index]
            self.index += 1
            return module
        else:
            raise StopIteration

    def __getitem__(self, index) -> Module:
        return self._modules_list[index]

    def compare(self, selected_modules_list):
        matching_modules = []
        non_matching_modules = []
        for module in self._modules_list:
            if any(module.name == selected_module.name for selected_module in
                   selected_modules_list._modules_list):
                matching_modules.append(module)
            else:
                non_matching_modules.append(module)
        return matching_modules, non_matching_modules

    def is_empty(self):
        return True if not self._modules_list else False

    @staticmethod
    def set_global_path_to_modules(relative_path_to_modules: str):
        ModulesList._relative_path_to_modules = relative_path_to_modules
