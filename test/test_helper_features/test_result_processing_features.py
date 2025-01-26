import fmpsdk
import pytest
import unittest
from unittest.mock import patch

from src.helper_features.result_processing_features import ResultsProcessing, InsiderTrading
from src.helper_features.api_features import AsyncAPIFunctions
from src.random_scripts import process_data

class TestResultsProcessing:

    @pytest.mark.asyncio
    async def test_add_key(self) -> None:
        """
        Function to test absolute path
        :return: None
        """
        new_key = ["symbol", "name"]
        new_value = ["AAPL", "Apple Inc."]
        existing_list = [{'date': '2023-06-30', 'reportedCurrency': 'USD'}, {'date': '2023-06-30', 'reportedCurrency': 'USD'}]
        added_keys = await ResultsProcessing.add_key(new_key=new_key, new_value= new_value, input_list=existing_list)
        assert len(added_keys) == 2
        assert added_keys[0]['symbol'] == 'AAPL'
        assert added_keys[0]['name'] == 'Apple Inc.'
        assert added_keys[1]['symbol'] == 'AAPL'
        assert added_keys[1]['name'] == 'Apple Inc.'

    @pytest.mark.asyncio
    @patch('src.data_handlers.DataProcessingFunctions.write_to_dataframe')
    async def test_handle_process_responses(self, mock_write_to_dataframe) -> None:
        df_names = ['stock_price', 'stock_metrics']
        responses = [[{'10Y': 896.1265, '1D': -2.0137, '1M': 4.36391, '1Y': 23.73093, 'symbol': 'AAPL'}], False]
        symbol = 'AAPL'
        name = 'Apple Inc.'
        # Set up the mock to return a known value
        number_of_requests = await ResultsProcessing.handle_process_responses(responses=responses, dataframe_names=df_names, symbol=symbol, name=name)
        assert number_of_requests == 2
        # Ensure the mock was called only once, as the second response is False
        mock_write_to_dataframe.assert_called_once()


class TestInsiderTrading:

    @pytest.mark.asyncio
    async def test_get_insider_trading(self) -> None:
        """
        Function to test absolute path
        :return: None
        """
        symbol = 'LULU'
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        limit = 10
        insider_trading = InsiderTrading(symbol=symbol, api_key=api_key)
        results = await insider_trading.get_insider_trading(limit=limit)
        income = fmpsdk.cash_flow_statement_growth(symbol=symbol, apikey=api_key)
        print(income)
        growth = fmpsdk.financial_growth( symbol=symbol, apikey=api_key)

        # growth[0]['epsgrowth']
        # growth[0]['freeCashFlowGrowth']


        print('ok')
        # assert insider_trading == 10


class TestResultsMock(unittest.TestCase):

    @patch('src.random_scripts.fetch_data')
    def test_process_data(self, mock_fetch_data):
        # Set up the mock to return a known value
        mock_fetch_data.return_value = {"key": "mock_value"}

        # Call the function under test
        result = process_data()

        # Verify the result
        self.assertEqual(result, {"processed_key": "MOCK_VALUE"})

        # Ensure the mock was called as expected
        mock_fetch_data.assert_called_once()
