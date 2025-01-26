import pytest
from src.earnings_calendar import EarningsCalendar
from src.helper_features.api_features import SyncAPIFunctions



class TestEarningsCalendar(SyncAPIFunctions):

    @pytest.mark.asyncio
    async def test_get_stock_name(self) -> None:
        """
        Function to test whether stock can be found
        :return: None
        """
        stock_list = ['MSFT', 'AAPL', 'BLABLA']
        expected_names = [['MSFT', 'Microsoft Corporation'], ['AAPL', 'Apple Inc.'], ['BLABLA', 'name not found']]

        earnings_calendar = EarningsCalendar()
        await earnings_calendar.get_stock_name(stock_symbol_list=stock_list)

        assert earnings_calendar.symbols == expected_names


    @pytest.mark.asyncio
    async def test_get_earnings_surprise(self) -> None:
        """
        Function to test whether stock can be found
        :return: None
        """

        earnings_calendar = EarningsCalendar()
        await earnings_calendar.async_get_earnings_surprises(share='MSFT')
        assert earnings_calendar.shares_with_earnings_surprises == ['MSFT']


    @pytest.mark.asyncio
    async def test_calculate_earnings_surprise(self) -> None:
        """
        Function to test whether stock can be found
        :return: None
        """
        positive_earnings_result = {'estimatedEarning': 1, 'actualEarningResult': 2}
        negative_earnings_result = {'estimatedEarning': 2, 'actualEarningResult': 1}
        earnings_calendar = EarningsCalendar()
        positive_earnings_calculation = await earnings_calendar.calculate_earnings_surprise(earnings_result=positive_earnings_result)
        negative_earnings_calculation = await earnings_calendar.calculate_earnings_surprise(earnings_result=negative_earnings_result)

        assert positive_earnings_calculation == True
        assert negative_earnings_calculation == False



    @pytest.mark.asyncio
    async def test_earnings_analysis(self) -> None:
        """
        Function to test whether stock can be found
        :return: None
        """
        earnings_calendar = EarningsCalendar()
#         write mock test for this function


# def test_earnings_calendar():
#     """
#     Function to test the earnings calendar
#     :return: None
#     """
#     earnings = EarningsCalendar()
#     stock_symbols = earnings.get_earnings_calendar()
#     assert type(stock_symbols) == list



# def test_earnings_surprises():
#     """
#     Function to test the earnings calendar
#     :return: None
#     """
#     earnings = EarningsCalendar()
#     stock_symbols = earnings.get_earnings_calendar()
#     earning_surprises = earnings.get_earnings_surprises(shares=stock_symbols)
#     assert type(stock_symbols) == list



# class TestMainRun:
#
#
#     def test_main_stock_analysis_run(self) -> None:
#         """
#         Function to test the main run method
#         :return: None
#         """
#         Globals.STOCK_LIST = ["BIDU", "XPEV", "ALIT", "AMAT", "ACHR","ATRA"]
#         run_stock_api(predefined_symbols=None)
#         assert 1==1