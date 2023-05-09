
import sqlalchemy import create_engine

from utils.utilsfile import ConfigsParser as parser

class Db():
    def __init__(self):
        self.db_configs = parser.parse_configs('DATABASE')
        self.username = self.db_configs['username']
        self.password = self.db_configs['password']
        self.host = self.db_configs['host']
        self.database = self.db_configs['db_name']
        self.db_engine = self.get_engine()


    def get_engine(self):
        try:
            engine =create_engine("mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8&binary_prefix=true".format(
                username =self.username,
                password = self.password,
                host =self.host,
                database = self.database,
            ))  

            return engine
        
        except Exception as e:
            print ("Error creating db connection: ", e)
        
        
        
            