import os

BASE_DIR = os.path.abspath(os.environ.get("SOLAR_BASE_DIR", r"C:\Users\Jason\Documents\EECS6320-project\fairness_testing_code_generation\outputs\gemini_full_run\baseline\response"))

LOG_DIR = os.path.abspath(os.environ.get("SOLAR_LOG_DIR", r"C:\Users\Jason\Documents\EECS6320-project\fairness_testing_code_generation\outputs\gemini_full_run\baseline\test_result\log_files"))

REPORT_BASE_DIR = os.path.abspath(os.environ.get("SOLAR_REPORT_BASE_DIR", r"C:\Users\Jason\Documents\EECS6320-project\fairness_testing_code_generation\outputs\gemini_full_run\baseline\test_result\inconsistency_files"))
