import configparser
import pytest


@pytest.fixture(scope='session')

def db_config():
    #read the config file
    configs = configparser.ConfigParser()
    configs.read('config.ini')
    config = configs['DATABASE']
    host=config['host']
    user=config['username']
    password= config['password']
    database=config['db_name']

    return {
        'host':host,
        'database': database,
        'username': user,
        'password': password
    }
