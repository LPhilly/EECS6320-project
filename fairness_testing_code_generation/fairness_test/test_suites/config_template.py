import os

# Base directory where test cases are stored
BASE_DIR = os.path.abspath(os.environ.get("SOLAR_BASE_DIR", "##PATH##TO##RESPONSE##"))

# Base directory for log files
LOG_DIR = os.path.abspath(os.environ.get("SOLAR_LOG_DIR", "##PATH##TO##LOG##FILES##"))

# Base directory for report files
REPORT_BASE_DIR = os.path.abspath(os.environ.get("SOLAR_REPORT_BASE_DIR", "##PATH##TO##INCONSISTENCY##FILES##"))
