from src.helper_features.logging import LoggingFunctions
from src.data_handlers import Globals

class TestLoggingFunctions:

    def test_determine_log_file_name(self):
        log = LoggingFunctions()

        Globals.ANALYSIS_TYPE = "full"
        log_file_name = log.determine_log_file_name()
        assert log_file_name == 'stock_api_log_main_run.log'
        Globals.ANALYSIS_TYPE = "earnings_calendar"
        assert log.determine_log_file_name() == 'stock_api_log_earnings_calendar_run.log'
        Globals.ANALYSIS_TYPE = "cli"
        assert log.determine_log_file_name() == 'cli_stock_api_log.log'