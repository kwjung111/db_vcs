import yaml
import sys
from enum import Enum
from logger import logger

class Config:
    DEFAULT_CONFIG_PATH='config.yaml'
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        with open(config_path,'r') as file:
            config = yaml.safe_load(file)
            
        self.__database = config.get('database',{})
        self.__repository= config.get('repository',{})
        self.__logging = config.get('logging',{})
        self.__interval_days = config.get('interval_days',{})
        if config.get('mode',{}) == 'ENTIRE':
            self.__mode = Mode.ENTIRE
        elif config.get('mode',{}) == 'WHEN_ALTERED':
            self.__mode = Mode.WHEN_ALTERED
            if not self.__interval_days:
                self.__interval_days = 1
        else:
            logger.Error(f"Config Error : check Required field 'mode' in your config.yaml file")
            sys.exit(1)
        
    def get_database(self):
        return self.__database
    
    def get_repository(self):
        return self.__repository
    
    def get_logging(self):
        return self.__logging 
    
    def get_mode(self):
        return self.__mode
    
    def get_interval_days(self):
        return self.__interval_days
    
class Mode(Enum):
    ENTIRE=1
    WHEN_ALTERED=2
    