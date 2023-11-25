import os


class Module:
    def __init__(self, relative_path):
        self.relative_path = relative_path
        self.absolute_path = self.get_absolute_path()
        self.name = self.get_work_directory()

    def __str__(self):
        return f'Module({self.name}, {self.absolute_path})'

    def get_absolute_path(self):
        return os.path.realpath(self.relative_path)

    def get_work_directory(self):
        return os.path.basename(os.path.normpath(self.absolute_path))

    def remove_file(self, file_name: str):
        absolute_path_to_file = os.path.join(self.absolute_path, file_name)
        if os.path.exists(absolute_path_to_file):
            os.remove(absolute_path_to_file)
        else:
            raise FileNotFoundError(f'Warning: file {file_name} not found in {absolute_path_to_file} directory.')

    def remove_files(self, file_names: list):
        for file in file_names:
            self.remove_file(file)

    def remove_folder(self, folder_name):
        absolute_path_to_folder = os.path.join(self.absolute_path, folder_name)
        if os.path.isdir(absolute_path_to_folder):
            os.rmdir(absolute_path_to_folder)
        else:
            raise FileNotFoundError(f'Warning: {folder_name} folder not found in {absolute_path_to_folder} directory.')

    def remove_folders(self, folder_names: list):
        for folder in folder_names:
            self.remove_folder(folder)
