import configparser


print("should only be executed once")
config = configparser.ConfigParser()
config.read('config.ini')
