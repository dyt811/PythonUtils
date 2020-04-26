# This is a stand alone, useful logging utility:
# Inspired by earlier work with DICOMTransit

# Inspect is used to get module name effectively.
import logging

# Required for timing
from datetime import datetime

# Required for path generation
from pathlib import Path

import os

# The logger object which will be imported by other modules which will use this to log out.
logger = logging.getLogger("UniversalLogger")

# Ensure file out folder exist:
path_logs = Path(__file__).parent / "logs"

if not path_logs.exists():
	os.makedirs(path_logs)


# Log all debug events
logger.setLevel(logging.DEBUG)
handler_std_out = logging.StreamHandler()
handler_file_out = logging.FileHandler(
	path_logs / (datetime.now().isoformat().replace(":", "") + ".log")
)

formatter = logging.Formatter(
	"[%(asctime)s]\t\t\t\t[%(levelname)s]\t\t\t\t[%(filename)s,%(module)s,%(funcName)s():\t\t\t\tLine %(lineno)i]:\t\t\t\t%(message)s"
)

# Add the formatter to the handler
handler_std_out.setFormatter(formatter)
handler_file_out.setFormatter(formatter)

# Add the hanlder to the right logger object
logger.addHandler(handler_file_out)
logger.addHandler(handler_std_out)






