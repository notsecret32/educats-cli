import os
import shutil

from cli.utils import (
    success,
    warning
)


class Module:
    def __init__(self, relative_path):
        self.relative_path = relative_path
        self.absolute_path = os.path.realpath(relative_path)
        self.name = os.path.basename(os.path.normpath(self.absolute_path))

    def delete(self, file_or_folder_name: str):
        path = os.path.join(self.absolute_path, file_or_folder_name)

        if os.path.exists(path):
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return not os.path.exists(path)
        else:
            return False

    def delete_files(self, file_name, should_delete):
        if self.has(file_name) and should_delete:
            if self.delete(file_name):
                success(f'{self.name}: {file_name} file successfully removed.')
            else:
                warning(f'{self.name}: failed to remove {file_name} file.')
        else:
            warning(f'Warning: {file_name} file not found in {self.name.upper()} module.')

    def has(self, folder_or_file: str):
        return os.path.exists(os.path.join(self.absolute_path, folder_or_file))

    def __str__(self):
        return f'Module({self.name}, {self.absolute_path})'
