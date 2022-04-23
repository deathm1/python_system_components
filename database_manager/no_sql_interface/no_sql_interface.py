# class imports 
from console_manager.console_manager import console_manager

# module imports
import configparser
from pymongo import MongoClient
import pymongo
import logging

class no_sql_interface():

    my_console_manager = None

    @classmethod
    def __init__(self) -> None:
        """Constructor
        """
        self.my_console_manager = console_manager()
    

    @classmethod
    def get_database(self, config):
        """This fucntion is responsible for initiating connection with mongo db database.

        Args:
            config (configparser): This is config parser object

        Returns:
            pymongo: pymongo object
        """
        try:
            CONNECTION_STRING = config.get("DATABASE_CONFIGURATION","CONNECTION_STRING")
            NO_SQL_DATABASE = config.get("DATABASE_CONFIGURATION","NO_SQL_DATABASE")
            NO_SQL_DATABASE_COLLECTION = config.get("DATABASE_CONFIGURATION","NO_SQL_DATABASE_COLLECTION")
            client = MongoClient(CONNECTION_STRING)
            database = client[NO_SQL_DATABASE]
            my_collection = database[NO_SQL_DATABASE_COLLECTION]
            return (True, my_collection)
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[no_sql_interface][get_database] Something went wrong while initiating connection with database. Error : {str(e)}",
                logging.ERROR
            )
            return (False, e)
