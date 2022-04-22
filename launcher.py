# from database_manager.database_manager import database_manager

# import json


# my_database_manager = database_manager()




# was_connection_established, connection_object_or_error = my_database_manager.get_sql_controller()



# my_dict = {
#     "logMessage":"some log message", 
#     "logComponent":"INFO", 
#     "addedBy":"linux"
# }

# connection_object_or_error.write_stored_procedure("insert_log", False, True, "", json.dumps(my_dict))

import traceback

from logging_interface.logging_interface import logging_interface
import logging
i = 1

while i<=10000:
    my_log_obj = logging_interface(f"Simple Log{str(i)}", logging.INFO, None, None)
    i = i + 1