from cli import *


global_modules_list = ModulesList(
    ModulesListActions.CREATE_LIST_FROM_MODULES,
    selected_modules=('admin server',)
)

print(global_modules_list)
