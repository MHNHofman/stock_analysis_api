#pylint disable=f-string-without-interpolation, too-few-public-methods
"""Module to determine a logfile and write log messages to it"""
import logging
from src.data_handlers import Globals
logger = logging.getLogger(__name__)


class LoggingFunctions:
    """Create logfile and write log messages to it"""

    @classmethod
    def determine_log_file_name(cls) -> str:
        """Function to determine the log file name based on the analysis type"""
        file_name: str
        if Globals.ANALYSIS_TYPE == "full":
            file_name = f"stock_api_log_main_run.log"
        elif Globals.ANALYSIS_TYPE == "earnings_calendar":
            file_name = f"stock_api_log_earnings_calendar_run.log"
        else:
            file_name = f"cli_stock_api_log.log"
        return file_name
