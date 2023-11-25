from cli.modules.modules_list import ModulesList


global_modules_list: ModulesList


def initialize_global_modules(modules_list: ModulesList):
    global global_modules_list
    global_modules_list = modules_list
