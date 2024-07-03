import os
import sys
import logging

# Define the logging format string with placeholders for timestamp, log level, module name, and message
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Directory where log files will be stored
log_dir = "logs"

# Full path to the log file
log_filepath = os.path.join(log_dir, "running_logs.log")

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format=logging_str,  # Set the logging format
    handlers=[
        # Write log messages to the specified file
        logging.FileHandler(log_filepath),
        # Also output log messages to the console (stdout)
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a logger object with the name "ClassifierLogger"
logger = logging.getLogger("ClassifierLogger")
