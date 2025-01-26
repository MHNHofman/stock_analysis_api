from src.helper_features.common_calculations import get_analysis_type, get_day_difference
from src.data_handlers import Globals

class TestCommonCalculations:

    def test_get_day_difference(self):

        day_diff = get_day_difference('2023-06-30')
        # from day of this test was written we are 512 days ahead
        assert day_diff > 511

    def test_get_analysis_type(self):

        Globals.STOCK_LIST = []
        full_analysis_type = get_analysis_type(predefined_symbols=None)
        predefined_symbols = ['AAPL', 'GOOGL']
        earnings_analysis_type = get_analysis_type(predefined_symbols=predefined_symbols)
        Globals.STOCK_LIST = predefined_symbols
        cli_analysis_type = get_analysis_type(predefined_symbols=None)
        assert full_analysis_type == 'full'
        assert earnings_analysis_type == 'earnings_calendar'
        assert cli_analysis_type == 'cli'
