from enum import Enum

from cli.modules.module import Module


class ModulesListActions(Enum):
    CREATE_LIST_FROM_PATH = 1
    CREATE_LIST_FROM_MODULES = 2


class ModulesList:
    def __init__(self, action: ModulesListActions, **kwargs):
        # Если создаем объект из относительного пути
        if action == ModulesListActions.CREATE_LIST_FROM_PATH:
            # Проверяем наличие аттрибута relative_path_to_modules и его тип (список)
            if 'relative_path_to_modules' in kwargs and isinstance(kwargs.get('relative_path_to_modules'), list):
                # Получаем относительные пути
                relative_path_to_modules = kwargs.get('relative_path_to_modules')

                # Создаем список модулей
                self.modules_list = self._create_modules_from_path(relative_path_to_modules)
            else:
                # Если аттрибут не найден, вызываем исключение
                raise AttributeError(f'Error: relative_path_to_modules attribute not found.')

        # Если создаем объект на основе введенных модулей
        if action == ModulesListActions.CREATE_LIST_FROM_MODULES:
            # Проверяем наличие аттрибута selected_modules и его тип (кортеж)
            if 'selected_modules' in kwargs:
                if isinstance(kwargs.get('selected_modules'), tuple):
                    # Получаем список модулей в виде кортежа
                    selected_modules: tuple = kwargs.get('selected_modules')

                    # Делаем из него массив объектов Module
                    self.modules_list = self._create_modules_from_tuple(selected_modules)
                elif isinstance(kwargs.get('selected_modules'), list):
                    # Получаем список модулей в виде списка
                    selected_modules: list = kwargs.get('selected_modules')

                    # Делаем из него массив объектов Module
                    self.modules_list = self._create_modules_from_list(selected_modules)
                else:
                    raise AttributeError(
                        f"""Error: the type of selected_modules passed is a {type(kwargs.get('selected_modules'))}, 
                        and a list or tuple was expected."""
                    )
            else:
                # Если аттрибут не найден, вызываем исключение
                raise AttributeError(f'Error: relative_path_to_modules attribute not found.')

    # Делаем класс итерируемым
    def __iter__(self):
        for module in self.modules_list:
            yield module

    def __str__(self):
        return f'ModulesList({self.modules_list})'

    # Сравниваем два списка модулей и возвращаем кортеж из совпадающих и несовпадающих модулей
    def compare(self, compare_modules_list):
        if not isinstance(compare_modules_list, ModulesList):
            raise ValueError(f'Error: compare_modules_list is not an instance of ModulesList')

        matched = [module for module in self.modules_list if module in compare_modules_list.modules_list]
        mismatched = [module for module in compare_modules_list.modules_list if module not in self.modules_list]

        return (ModulesList(ModulesListActions.CREATE_LIST_FROM_MODULES, selected_modules=matched),
                ModulesList(ModulesListActions.CREATE_LIST_FROM_MODULES, selected_modules=mismatched))

    # Создаем список модулей на основе относительного пути
    @staticmethod
    def _create_modules_from_path(relative_path_to_modules: str):
        modules_list = []

        for relative_module_path in relative_path_to_modules:
            modules_list.append(Module(relative_module_path))

        return modules_list

    # Создаем список на основе переданного картежа
    @staticmethod
    def _create_modules_from_tuple(selected_modules: tuple):
        if not isinstance(selected_modules, ModulesList):
            raise ValueError(f'Error: selected_modules is not an instance of ModulesList')

        selected_modules_list = list(selected_modules)
        result = [module for modules in selected_modules_list for module in modules.split()]
        return result or []
