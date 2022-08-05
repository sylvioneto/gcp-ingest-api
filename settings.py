# demo/settings.py
import os
import logging


# Get env vars and log error if not found
def read_env_var(var_name):
    var_value = os.environ.get(var_name)
    if not var_value:
        logging.error("Missing env var {}={}".format(var_name, var_value))
    return var_value


PROJECT_ID = read_env_var("PROJECT_ID")
TOPIC_ID = read_env_var("TOPIC_ID")
SOURCE_SYSTEM = read_env_var("SOURCE_SYSTEM")
