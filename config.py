import configparser

config = configparser.ConfigParser()
config.read('config.ini')

BROWSER = config['default']['browser']
