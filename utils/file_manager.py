import os
import re
import shutil

EXTENSION = '.png'
PATTERN = '\d+-\d+'


class FileManager:
    def __init__(self, destination_folder):
        self.destination_folder = destination_folder

    def move_files(self):
        files = self.get_files()
        for file_path in files:
            self.move_file(file_path)

    def get_files(self):
        downloads_folder = os.path.expanduser("~/Downloads")
        files = []
        for filename in os.listdir(downloads_folder):
            if filename.endswith(EXTENSION) and re.search(PATTERN, filename):
                file_path = os.path.join(downloads_folder, filename)
                files.append(file_path)
        return files

    def move_file(self, file_path):
        if not os.path.exists(self.destination_folder):
            os.makedirs(self.destination_folder)
        shutil.move(file_path, self.destination_folder)

    def rename_file(self, file_name, new_name):
        new_file_path = os.path.join(self.destination_folder, new_name)
        old_file_path = os.path.join(self.destination_folder, file_name)
        os.rename(old_file_path, new_file_path)
