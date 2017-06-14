import configparser

from motey.utils.path_helper import absolute_file_path

config = configparser.ConfigParser()
config.read(absolute_file_path('motey/configuration/config.ini'))
