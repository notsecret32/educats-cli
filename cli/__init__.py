import toml


class EducatsCLI:
    """
    Класс, который связывает CLI с модулями, предоставляя удобный интерфейс для работы с командами и модулями.
    """
    _relative_path_to_global_modules = []

    @classmethod
    def initialize(cls, config: str):
        try:
            with open(config, 'r') as f:
                config = toml.load(f)
                cls._relative_path_to_global_modules = config['modules']['relative_modules_path_list']
        except FileNotFoundError:
            raise FileNotFoundError(f'Error: {config} not found.')

    @classmethod
    def get_relative_path_to_global_modules(cls):
        return cls._relative_path_to_global_modules
