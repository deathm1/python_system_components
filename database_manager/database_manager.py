# class imports
from database_manager.sql_interface.sql_interface import sql_interface
from database_manager.no_sql_interface.no_sql_interface import no_sql_interface
from console_manager.console_manager import console_manager
# module imports
import pyodbc
import configparser
import logging

class database_manager:
    """[database_manager] class helps in establishing connection with any database.
    Make sure to have a config.ini file in the root directory to pass database specific arguments.
    """
    my_console_manager = None
    my_was_connection_established = None 
    my_connection_object_or_error = None

    @classmethod
    def __init__(self):
        """Constructor
        """
        config = configparser.ConfigParser()
        config.read("./config.ini")
        self.my_console_manager = console_manager()
        if(config.get("DATABASE_CONFIGURATION", "DB_TYPE")=="SQL"):
            was_connection_established, connection_object_or_error = self.create_connection_with_sql_database(config)
            self.my_connection_object_or_error = connection_object_or_error
            self.my_was_connection_established = was_connection_established
            if(was_connection_established):
                pass
            else:
                self.my_console_manager.make_console_log(
                f"[database_manager][__init__] Something went wrong establishing connection with SQL database. ERROR : {str(connection_object_or_error)}",
                logging.ERROR
            )
        elif(config.get("DATABASE_CONFIGURATION", "DB_TYPE")=="NOSQL"):
            was_connection_established, connection_object_or_error = self.create_connection_with_no_sql_database(config)
            self.my_connection_object_or_error = connection_object_or_error
            self.my_was_connection_established = was_connection_established
            if(was_connection_established):
                pass
            else:
                self.my_console_manager.make_console_log(
                f"[database_manager][__init__] Something went wrong establishing connection with NOSQL database. ERROR : {str(connection_object_or_error)}",
                logging.ERROR
                )
    @classmethod
    def get_database_controller(self):
        """This function returns my_was_connection_established, my_connection_object_or_error

        Returns:
            bool, pyodbc object: my_was_connection_established, my_connection_object_or_error
        """
        return (self.my_was_connection_established, self.my_connection_object_or_error)
    @classmethod
    def create_connection_with_sql_database(self, config):
        """This function is responsible for initializing connection to SQL database.

        Args:
            config (configparser): configparser object
        """
        if(config.get("DATABASE_CONFIGURATION", "AUTHENTICATION")=="OS"):
            try:
                DRIVER = config.get("DATABASE_CONFIGURATION", "DRIVER")
                SERVER = config.get("DATABASE_CONFIGURATION", "SERVER")
                DATABASE = config.get("DATABASE_CONFIGURATION", "DATABASE")
                TRUSTED_CONNECTION = config.get("DATABASE_CONFIGURATION", "DATABASE")
                connection_string = 'DRIVER='+DRIVER+';' + 'SERVER='+SERVER+';' + 'DATABASE='+DATABASE+';' + 'Trusted_Connection='+TRUSTED_CONNECTION+';'
                connection = pyodbc.connect(connection_string, echo = True)
                my_sql = sql_interface(connection)
                return (True, my_sql)
            except Exception as e:
                return (False, e)

        elif(config.get("DATABASE_CONFIGURATION", "AUTHENTICATION")=="CREDENTIALS"):
            try:
                DRIVER = config.get("DATABASE_CONFIGURATION", "DRIVER")
                SERVER = config.get("DATABASE_CONFIGURATION", "SERVER")
                DATABASE = config.get("DATABASE_CONFIGURATION", "DATABASE")
                UID = config.get("DATABASE_CONFIGURATION", "UID")
                PWD = config.get("DATABASE_CONFIGURATION", "PWD")
                connection_string = 'DRIVER='+DRIVER+';' + 'SERVER='+SERVER+';' + 'DATABASE='+DATABASE+';' + 'UID='+UID+';' + 'PWD='+PWD+';'
                connection = pyodbc.connect(connection_string, echo = True)
                my_sql = sql_interface(connection)
                return (True, my_sql)
            except Exception as e:
                return (False, e)
    @classmethod
    def create_connection_with_no_sql_database(self, config):
        """This function is reposnible for connecting ot NO SQL database.

        Args:
            config (configparser): This is configparser object.

        Returns:
            was_connection_established, connection_object_or_error: was_connection_established, connection_object_or_error
        """
        try:
            my_no_sql_object = no_sql_interface()
            was_connection_established, connection_object_or_error = my_no_sql_object.get_database(config)
            return (was_connection_established, connection_object_or_error)
        except Exception as e:
            return (False, e)
    @classmethod
    def __del__(self):
        """Destructor
        """
        pass
        #self.my_console_manager.make_console_log(f"[database_manager][__del__] Database manager has been destroyed.", logging.INFO)