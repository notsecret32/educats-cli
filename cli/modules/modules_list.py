from enum import Enum

from module import Module


class ModulesListActions(Enum):
    CREATE_LIST_FROM_PATH = 1
    CREATE_LIST_FROM_MODULES = 2


class ModulesList:
    def __init__(self, action: ModulesListActions, **kwargs):
        # Если создаем объект из относительного пути
        if action == ModulesListActions.CREATE_LIST_FROM_PATH:
            # Проверяем наличие аттрибута relative_path_to_modules
            if hasattr(kwargs, 'relative_path_to_modules'):
                # Получаем относительные пути
                relative_path_to_modules = kwargs.get('relative_path_to_modules')

                # Создаем список модулей
                self.modules_list = self._create_modules_from_path(relative_path_to_modules)
            else:
                # Если аттрибут не найден, вызываем исключение
                raise AttributeError(f'Error: relative_path_to_modules attribute not found.')

        # Если создаем объект на основе введенных модулей
        if action == ModulesListActions.CREATE_LIST_FROM_MODULES:
            # Проверяем наличие аттрибута selected_modules
            if hasattr(kwargs, 'selected_modules'):
                # Получаем список модулей
                selected_modules: tuple = kwargs.get('selected_modules')

                # Делаем из него список
                self.modules_list = self._create_modules_from_selected(selected_modules)
            else:
                # Если аттрибут не найден, вызываем исключение
                raise AttributeError(f'Error: relative_path_to_modules attribute not found.')

    # Делаем класс итерируемым
    def __iter__(self):
        for module in self.modules_list:
            yield module

    # Сравниваем два списка модулей и возвращаем кортеж из совпадающих и несовпадающих модулей
    def compare(self, compare_modules_list):
        if not isinstance(compare_modules_list, ModulesList):
            raise ValueError(f'Error: compare_modules_list is not an instance of ModulesList')

        matched_modules_list = list(set(self.modules_list) & set(compare_modules_list))
        mismatched_modules_list = list(set(self.modules_list) - set(compare_modules_list))

        return matched_modules_list, mismatched_modules_list

    # Создаем список модулей на основе относительного пути
    @staticmethod
    def _create_modules_from_path(relative_path_to_modules):
        modules_list = []

        for relative_module_path in relative_path_to_modules:
            modules_list.append(Module(relative_module_path))

        return modules_list

    # Создаем список на основе переданного картежа
    @staticmethod
    def _create_modules_from_selected(selected_modules):
        modules_list = list(selected_modules)
        result = [module for modules in modules_list for module in modules.split()]
        return result or []
