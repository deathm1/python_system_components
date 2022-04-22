# class imports
from console_manager.console_manager import console_manager

#module imports
import logging

class sql_interface():
    """This is operation interface class of SQL

    Returns:
        list: Returns the list of tupples fetched from the database. 
    """
    my_sql_connection = None
    my_console_manager = None

    @classmethod
    def __init__(self, sql_connection_object) -> None:
        """This function is responsible for assigning [my_sql_connection] and initializing [console_manager]

        Args:
            sql_connection_object (pyodbc object): SQL connection object returned by pyodbc if everything was right.
        """
        self.my_sql_connection = sql_connection_object
        self.my_console_manager = console_manager()

    @classmethod
    def read_stored_procedure(self, stored_procedure_name : str, is_parameter : bool, is_without_parameter_name : bool, parameter_name : str, parameter : str) -> list:
        """This function is responsible for executing read stored procedures in SQL database.

        Args:
            stored_procedure_name (str): Name of the Stored Procedure.
            is_parameter (bool): Does the stored procedure have parameters.
            parameter_name (str): Name of the parameter variable.
            parameter (str): The parameter itself.

        Returns:
            list: Returns the list of tupples fetched from the database.
        """
        try:
            if(is_parameter):
                sql_command = "{" + f"CALL {stored_procedure_name}(@{parameter_name}=?)" + "}"
                return list(self.my_sql_connection.cursor().execute(sql_command, parameter).fetchall())
            elif(is_without_parameter_name):
                my_sql_command = f"CALL {stored_procedure_name}('{parameter}')"
                print(my_sql_command)
                self.my_sql_connection.cursor().execute(my_sql_command).fetchall()
            else:
                sql_command = "{" + f"call {stored_procedure_name}()" + "}"
                return list(self.my_sql_connection.cursor().execute(sql_command).fetchall())
            self.my_sql_connection.commit()
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[database_manager][sql][read_stored_procedure] Something went wrong while executing read stored procedure. ERROR : {str(e)}",
                logging.ERROR
            )
            return []
            
    @classmethod
    def write_stored_procedure(self, stored_procedure_name : str, is_parameter : bool, is_without_parameter_name : bool, parameter_name : str, parameter : str):
        """This function is responsible for executing write stored procedures in SQL database.

        Args:
            stored_procedure_name (str): Name of the Stored Procedure.
            is_parameter (bool): Does the stored procedure have parameters.
            parameter_name (str): Name of the parameter variable.
            parameter (str): The parameter itself.
        """
        try:
            if(is_parameter):
                sql_command = "{" + f"CALL {stored_procedure_name}(@{parameter_name}=?)" + "}"
                self.my_sql_connection.cursor().execute(sql_command, parameter)
            elif(is_without_parameter_name):
                my_sql_command = "{" +  f"CALL {stored_procedure_name}('{parameter}')" + "}"
                self.my_sql_connection.cursor().execute(my_sql_command)
            else:
                sql_command = "{" + f"call {stored_procedure_name}()" + "}"
                self.my_sql_connection.cursor().execute(sql_command)
            self.my_sql_connection.commit()
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[database_manager][sql][write_stored_procedure] Something went wrong while executing write stored procedure. ERROR : {str(e)}",
                logging.ERROR
            )

    @classmethod
    def simple_query_executor(self, SQL_query):
        """This function takes in a simple SQL query and executes it.

        Args:
            SQL_query (str): SQL query string

        Returns:
            list: list of tuples
        """
        try:
            return self.my_sql_connection.cursor().execute(SQL_query).fetchall()
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[database_manager][sql][simple_query_executor] Something went wrong while executing SQL Query. ERROR : {str(e)}",
                logging.ERROR
            )

    @classmethod
    def close_sql_connection(self):
        """This function is reponsible for closing sql connection.
        """
        try:
            self.my_sql_connection.commit()
            self.my_sql_connection.close()
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[database_manager][sql][close_sql_connection] Something went wrong while closing SQL connection. ERROR : {str(e)}",
                logging.ERROR
            )
    
    @classmethod
    def __del__(self):
        """Destructor responsible for commiting in SQL database.
        """
        try:
            self.my_sql_connection.commit()
        except Exception as e:
            self.my_console_manager.make_console_log(
                f"[database_manager][sql][__del__] Something went wrong while commiting in SQL. ERROR : {str(e)}",
                logging.ERROR
            )