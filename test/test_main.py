from stock_main_run import run_stock_api
from src.data_handlers import Globals


class TestMainRun:


    def test_main_stock_analysis_run(self) -> None:
        """
        Function to test the main run method
        :return: None
        """

        Globals.STOCK_LIST = ["MSFT", "AAPL"]
        run_stock_api(predefined_symbols=None)
        assert 1==1
