import os
from datetime import datetime

# Find location of script and run all commands from there
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(BASE_DIR)

# Determine root of pipeline directory
pipeline_directory = os.getenv("PIPELINE_DIRECTORY")

# Check to see if active hours are set and fail if outside active hours.
active_hours = os.getenv("APPLICATION_ACTIVEHOURS")

if active_hours is not None:
    active_hours = [ int(hour) for hour in active_hours.split(' ') ]
    if int(datetime.strftime(datetime.now(), '%H')) not in active_hours:
        raise RuntimeError("WARNING:"+str(datetime.now())+
                           ":pipeline:Task: Check Active Hours Restriction, \
                            OUTSIDE APPLICATION_ACTIVEHOURS")
