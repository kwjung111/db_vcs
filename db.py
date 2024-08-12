import mysql.connector
from config import Config
from mysql.connector import Error
from logger import logger

class Database:
    def __init__(self,conf : Config ):
        self.__conf=conf.get_database()
    
    def connect(self,database,sys):
        try:
            connection = mysql.connector.connect(
                host=database['host']
                ,port=database['port']
                ,user=database['user']
                ,password=database['password'])
            
            logger.debug(f"{sys} : connected")      
        except Error as e:
            logger.error(f"Error: {e}")
    
        return connection

    def connect_all(self):
        conf=self.__conf
        connections = {}
        for key, value in conf.items():
            connections[key] = self.connect(value,key)
        return connections

    def read(self, connection , sql):
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)
        record = cursor.fetchall()
        return record
    