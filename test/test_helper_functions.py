# import unittest
# from unittest.mock import AsyncMock
# import asyncio
# import fmpsdk
# import warnings
# import openpyxl
# import pytest
# import unittest
# import pandas as pd
# from unittest.mock import Mock, patch
# from pathlib import Path
# from src.helper_features.api_features import AsyncAPIFunctions
# from src.helper_features.excel_features import ExcelOperations
# from src.helper_features.result_processing_features import ResultsProcessing
# from src.data_handlers import (
#     TradesOverview,
#     DataFrameFunctions,
#     Globals,
#     make_request,
#     do_session_get,
#     GenericFunctions,
#     convert_xml_to_json
# )
# import mock
#
#
# class TestAsyncHelperFunctions:
#
#     @pytest.mark.asyncio
#     async def test_api_key_pytest(self) -> None:
#         """
#         Function to test the Upload File Method
#         :return: None
#         """
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         assert len(api_key) == 32
#
#
# class TestTradesOverview:
#
#     @pytest.mark.asyncio
#     async def test_get_trade_symbols(self) -> None:
#         """
#         Function to test obtaining stock symbols
#         :return: None
#         """
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_symbols = TradesOverview(api_key)
#         trade_list = await trade_symbols.get_trade_symbols()
#         assert len(trade_list) > 0
#
#     # @pytest.mark.asyncio
#     # async def test_evaluate_trade_symbols(self) -> None:
#     #     """
#     #     Function to test whether stock can be found
#     #     :return: None
#     #     """
#     #     api_key = await AsyncAPIFunctions.async_load_api_keys()
#     #     trade_symbols = TradesOverview(api_key)
#     #     symbol_true = "MSFT"
#     #     symbol_false = "QiaoKeLi"
#     #     symbol_true_test = await trade_symbols.evaluate_trade_symbols(symbol=symbol_true)
#     #     assert symbol_true_test == symbol_true
#     #
#     #     with warnings.catch_warnings(record=True) as warn:
#     #         # Cause all warnings to always be triggered.
#     #         warnings.simplefilter("always")
#     #         # Trigger a warning
#     #         await trade_symbols.evaluate_trade_symbols(symbol=symbol_false)
#     #         # Verify the fake symbol triggers a warning
#     #         assert len(warn) == 1
#     #         assert issubclass(warn[-1].category, UserWarning)
#     #         assert "symbols" in str(warn[-1].message)
#
#
# class TestDataFrameFunctions:
#
#     DATA_DF1 = {
#         "symbol": ["MSFT", "Alice", "MSFT", "Charlie", "David"],
#         "Age": [34, 30, 40, 40, 45],
#         "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
#     }
#
#     DATA_DF2 = {
#         "symbol": ["MSFT", "Dylan", "MSFT", "Martin", "Peter"],
#         "Age": [20, 15, 25, 43, 15],
#         "City": ["Hong Kong", "Singapore", "Manilla", "KL", "Batam"],
#     }
#
#     DATA_DF3 = {
#         "symbol": ["MSFT", "Dylan", "MSFT", "Martin", "Peter"],
#         "Weight": [80, 95, 75, 84, 50],
#         "Color": ["Brown", "Black", "Blue", "Red", "Purple"],
#     }
#
#     @pytest.mark.asyncio
#     async def test_write_to_dataframe(self) -> None:
#         """
#         Function to test writing to dataframe
#         :return: None
#         """
#         symbol = "MSFT"
#         data = ["Q1", "Q2", "Q3"]
#         df_name = "INCOME_STATEMENT"
#         dataframe = DataFrameFunctions(symbol=symbol)
#         await dataframe.write_to_dataframe(data=data, df_name=df_name)
#         assert len(Globals.DATAFRAME_LIST_GENERAL[0].index) == 3
#         Globals.DATAFRAME_LIST_GENERAL[0].drop(
#             Globals.DATAFRAME_LIST_GENERAL[0].index, inplace=True
#         )
#
#     @pytest.mark.asyncio
#     async def test_transfer_data_dataframes(self) -> None:
#         """
#         Function to test transferring data between dataframes
#         :return: None
#         """
#         symbol = "MSFT"
#         # Create a dictionary with sample data
#
#         # Create the DataFrame
#         df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
#         df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF2)
#         Globals.DATAFRAME_LIST_GENERAL = [df1, df2]
#         Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS = []
#         constraint_type = "UNDERVALUED"
#         dataframe = DataFrameFunctions(symbol=symbol)
#         await dataframe.assign_transfer_dataframes(screener_type=constraint_type)
#
#         # checks whether the dataframe only includes the symbol MSFT
#         filtered_df = Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS[0][Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS[0]['symbol'] != 'MSFT']
#         assert len(filtered_df) == 0
#
#         # Clear the DataFrames
#         Globals.DATAFRAME_LIST_GENERAL.clear()
#         Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS.clear()
#
#     # @pytest.mark.asyncio
#     # async def test_process_api_request(self) -> None:
#     #     """
#     #     Function to test process api request
#     #     :return: None
#     #     """
#     #     symbol = "MSFT"
#     #     # check what result should look like
#     #
#     #     result = [
#     #         {
#     #             "symbol": "MSFT",
#     #             "filingDate": "2024-02-06 18:14:02",
#     #             "transactionDate": "2024-02-02",
#     #             "reportingCik": "0001193119",
#     #             "transactionType": "S-Sale",
#     #             "securitiesOwned": 574129.2701
#     #         },
#     #         {
#     #             "symbol": "MSFT",
#     #             "filingDate": "2024-02-06 18:14:02",
#     #             "transactionDate": "2024-02-05",
#     #             "reportingCik": "0001193119",
#     #             "transactionType": "S-Sale",
#     #             "securitiesOwned": 573051.2701
#     #         },
#     #         {
#     #             "symbol": "MSFT",
#     #             "filingDate": "2024-02-06 18:14:02",
#     #             "transactionDate": "2024-02-05",
#     #             "reportingCik": "0001193119",
#     #             "transactionType": "S-Sale",
#     #             "securitiesOwned": 571626.2701
#     #         },
#     #     ]
#     #
#     #     df_name = "INSIDER_TRADING"
#     #     dataframe = DataFrameFunctions(symbol=symbol)
#     #     process_result = await dataframe.process_api_request(
#     #         result=result, symbol=symbol, df_name=df_name
#     #     )
#     #     assert process_result is True
#
#     @pytest.mark.asyncio
#     async def test_get_df_metrics(self) -> None:
#         """
#         Function to test getting dataframe metrics
#         :return: None
#         """
#
#         # Create the DataFrame
#         df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
#         df1.attrs = {'name': 'INCOME_STATEMENT'}
#         df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF2)
#         df2.attrs = {'name': 'BALANCE_SHEET'}
#         data = [df1, df2]
#         metric_true = "INCOME_STATEMENT"
#         metric_false = "RSI"
#         symbol = "MSFT"
#         dataframe = DataFrameFunctions(symbol=symbol)
#         df_metrics_true = await dataframe.get_df_metrics(data=data, df_name=metric_true)
#         df_metrics_false = await dataframe.get_df_metrics(data=data, df_name=metric_false)
#         assert df_metrics_true['symbol'][0] == symbol
#         assert df_metrics_false.shape[0] == 0
#
#
#     @pytest.mark.asyncio
#     async def test_check_empty_dataframe(self) -> None:
#         symbol = "MSFT"
#         dataframe = DataFrameFunctions(symbol=symbol)
#         df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
#         df2 = pd.DataFrame()
#         data = [df1, df2]
#         empty_check = await dataframe.check_empty_dataframe(list_df=data)
#         assert empty_check is False
#
#     @pytest.mark.asyncio
#     async def test_check_variables_in_dataframe(self) -> None:
#         print("Test Check Variables in Dataframe")
#         symbol = "MSFT"
#         dataframe = DataFrameFunctions(symbol=symbol)
#         df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
#         df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF2)
#         data = [df1, df2]
#         correct_variables = ["Age", "City"]
#         incorrect_variables = ["Age", "RSI"]
#         check_correct_variables = await dataframe.check_variables_in_dataframe(variables=correct_variables, list_df=data)
#         check_incorrect_variables = await dataframe.check_variables_in_dataframe(variables=incorrect_variables, list_df=data)
#         assert check_correct_variables is False
#         assert check_incorrect_variables is True
#
#     # @pytest.mark.asyncio
#     # async def test_set_actual_values(self) -> None:
#     #     symbol = "MSFT"
#     #     dataframe = DataFrameFunctions(symbol=symbol)
#     #     df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
#     #     df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF3)
#     #     data = [df1, df2]
#     #     name_df = ['df1, df2']
#     #     variables = ["Age", "Color"]
#     #     value_type = ["percentage_diff", "iloc"]
#     #     actual_values = await dataframe.set_actual_values(variables=variables, list_df=data, value_type=value_type, name_df=name_df)
#     #     assert actual_values == {'Age': 13.333333333333334, 'Color': 'Brown'}
#
#     def test_set_sheet_name(self):
#         sheet_name_short = "incomestatement"
#         sheet_name_long = "averylongsheetnamewithmorethan31karakters"
#         assert len(GenericFunctions.set_sheet_name(df_name=sheet_name_short)) == 15
#         assert len(GenericFunctions.set_sheet_name(df_name=sheet_name_long)) == 31
#
#
#
# ##TODO:continue with this test
#
#
# class TestExcelOperations:
#
#     @pytest.mark.asyncio
#     async def test_get_abs_path(self) -> None:
#         """
#         Function to test the Upload File Method
#         :return: None
#         """
#         path = ExcelOperations.get_abs_path()
#         path_ending = "data_representation"
#
#         assert str(path).endswith(path_ending)
#
#     @pytest.mark.asyncio
#     async def test_clear_sheets(self) -> None:
#         """
#         Function to test the clear sheets method
#         :return: None
#         """
#
#         # first, execute the method to clear the sheets
#
#         await ExcelOperations.clear_sheets()
#         folder_path = ExcelOperations.get_abs_path()
#
#         # Iterate through the files in the folder to check whether all sheets are cleared
#
#         for file_path in folder_path.iterdir():
#             # Check if it's a file (not a subdirectory)
#
#             if file_path.is_file():
#                 book = openpyxl.load_workbook(file_path)
#
#                 # only the empty Sheet1 should be present
#
#                 assert len(book.sheetnames) == 1
#                 assert book.sheetnames[0] == "Sheet1"
#
# class TestResultsProcessing:
#
#     def test_relative_difference(self) -> None:
#         """
#         Function to test the relative difference method
#         :return: None
#         """
#         value1 = 0.07
#         value2 = 0.13
#         result = ResultsProcessing.relative_difference(x=value1, y=value2)
#         assert result == 1.86
#
#
#
#
# class TestMakeRequest(unittest.TestCase):
#
#     @patch("src.helper_functions.requests.Session")
#     def test_make_request(self, mock_session):
#         # Create a mock response
#
#         mock_response = Mock()
#         mock_response.status_code = 200
#
#         # Configure the mock session to return the mock response
#
#         mock_session.return_value.get.return_value = mock_response
#
#         # Call the function with the mock session
#
#         status_code = make_request("https://google.com")
#
#         print("ok")
#         # Assert that the function returned the expected status code
#         # self.assertEqual(status_code, 200)
#
#         # Optionally, you can assert that the session was used as expected
#
#         mock_session.return_value.get.assert_called_once_with("https://google.com")
#
#
# class TestDoSessionGet(unittest.TestCase):
#
#     @mock.patch("src.helper_functions.requests.session")
#     def test_should_mock_session_get(self, session_mock):
#         session_mock.return_value = mock.MagicMock(
#             get=mock.MagicMock(return_value="bar")
#         )
#
#         self.assertEqual(do_session_get(), "bar")
#
#
# def test_xml_converter():
#     path = Path(__file__).parent / "xml_episode_of_care.xml"
#     test = convert_xml_to_json(path=str(path))
#     print(path)
#
#
#
# # @pytest.fixture
# # def mock_thing() -> AsyncMock:
# #     """
# #     Async Mock Fixture
# #     :return:
# #     """
# #     mock_thing = AsyncMock()
# #     mock_thing.CatFact.get_cat_fact = AsyncMock(
# #         return_value="Mother cats " "teach their kittens " "to use the litter box."
# #     )
# #     return mock_thing
# #
# #
# # @pytest.mark.asyncio
# # async def test_get_cat_fact_mock(mock_thing) -> None:
# #     """
# #     Test for get_cat_fact method using Async Mocking
# #     :param mock_thing: Mock fixture
# #     :return: None
# #     """
# #     result = await mock_thing.CatFact.get_cat_fact()
# #     print('ok')
# #     assert result == "Mother cats teach their kittens to use the litter box."
#
#
# # class TestApiFunction(unittest.TestCase):
# #
# #     @pytest.fixture(scope="class")
# #     def event_loop_instance(self, request):
# #         """ Add the event_loop as an attribute to the unittest style test class. """
# #         request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
# #         yield
# #         request.cls.event_loop.close()
# #
# #     @pytest.mark.usefixtures("event_loop_instance")
# #     class TestTheThings(unittest.TestCase):
# #
# #         def get_async_result(self, coro):
# #             """ Run a coroutine synchronously. """
# #             return self.event_loop.run_until_complete(coro)
# #
# #         def test_an_async_method(self):
# #             result = self.get_async_result(AsyncAPIFunctions.async_load_api_keys())
# #             # result is the actual result, so whatever assertions..
# #             self.assertEqual(result,  "banana")
