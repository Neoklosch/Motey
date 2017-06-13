import os
import sys


def absolute_file_path(file_name):
    root_folder_path = os.path.dirname(sys.modules['__main__'].__file__)
    return os.path.abspath(os.path.join(root_folder_path, file_name))
