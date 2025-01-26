import pytest
import pandas as pd
from src.helper_features.api_features import AsyncAPIFunctions
from src.data_handlers import (
    TradesOverview,
    DataFrameFunctions,
    Globals,
    DataProcessingFunctions,
)
from src.cli.cli_functions import cli_check_and_get_symbols


# def test_cli() -> None:
#     """
#     Function to test obtaining stock symbols
#     :return: None
#     """
#     symbol_list = ["MSFT", "III"]
#     symbol_check = cli_check_and_get_symbols(symbol_list)
#
#     for stock in symbol_check:
#         for item in stock:
#             print(item)
#
#     print('ok')



class TestTradesOverview:

    @pytest.mark.asyncio
    async def test_get_trade_symbols(self) -> None:
        """
        Function to test obtaining stock symbols
        :return: None
        """
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        trade_symbols = TradesOverview(api_key)
        trade_list = await trade_symbols.get_trade_symbols()
        assert len(trade_list) > 0

    @pytest.mark.asyncio
    async def test_evaluate_trade_symbols(self) -> None:
        """
        Function to test whether stock can be found
        :return: None
        """
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        trade_symbols = TradesOverview(api_key)
        Globals.STOCK_LIST = ["MSFT"]
        test = 'test'

        if str(type(test)) == 'str':
            print('ok')

        symbol_true_test = await trade_symbols.check_and_get_symbols()
        assert symbol_true_test == [["MSFT", "Microsoft Corporation"]]

        # Globals.STOCK_LIST = ["QiaoKeLi"]
        # with warnings.catch_warnings(record=True) as warn:
        #     # Cause all warnings to always be triggered.
        #     warnings.simplefilter("always")
        #     # Trigger a warning
        #     await trade_symbols.check_and_get_symbols()
        #     # Verify the fake symbol triggers a warning
        #     assert len(warn) == 1
        #     assert issubclass(warn[-1].category, UserWarning)
        #     assert "QiaoKeLi" in str(warn[-1].message)

    @pytest.mark.asyncio
    async def test_symbol_name(self) -> None:
        """
        Function to test obtaining stock symbols
        :return: None
        """
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        trade_symbols = TradesOverview(api_key)
        correct_symbol = "MSFT"
        incorrect_symbol = "VSEEQQ"
        check_correct_symbol = await trade_symbols.get_symbol_name(
            symbol=correct_symbol
        )
        check_incorrect_symbol = await trade_symbols.get_symbol_name(
            symbol=incorrect_symbol
        )

        assert check_correct_symbol == True
        assert check_incorrect_symbol == False


class TestDataFrameFunctions:

    DATA_DF1 = {
        "symbol": ["MSFT", "Alice", "MSFT", "Charlie", "David"],
        "Age": [34, 30, 40, 40, 45],
        "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    }

    DATA_DF2 = {
        "symbol": ["MSFT", "Dylan", "MSFT", "Martin", "Peter"],
        "Age": [20, 15, 25, 43, 15],
        "City": ["Hong Kong", "Singapore", "Manilla", "KL", "Batam"],
    }

    DATA_DF3 = {
        "symbol": ["MSFT", "Dylan", "MSFT", "Martin", "Peter"],
        "Weight": [80, 95, 75, 84, 50],
        "Color": ["Brown", "Black", "Blue", "Red", "Purple"],
    }

    @pytest.mark.asyncio
    async def test_transfer_data_dataframes(self) -> None:
        """
        Function to test transferring data between dataframes
        :return: None
        """
        symbol = "MSFT"

        # Create the DataFrame

        df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
        df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF2)
        Globals.DATAFRAME_LIST_GENERAL = [df1, df2]
        Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS = []
        constraint_type = "UNDERVALUED"
        dataframe = DataFrameFunctions(symbol=symbol)
        await dataframe.assign_transfer_dataframes(screener_type=constraint_type)

        # checks whether the dataframe only includes the symbol MSFT

        filtered_df = Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS[0][
            Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS[0]["symbol"] != "MSFT"
            ]
        assert len(filtered_df) == 0

        # Clear the DataFrames

        Globals.DATAFRAME_LIST_GENERAL.clear()
        Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS.clear()

    def test_get_df_metrics(self) -> None:
        """
        Function to test getting dataframe metrics
        :return: None
        """

        # Create the DataFrame

        df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
        df1.attrs = {"name": "INCOME_STATEMENT"}
        df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF2)
        df2.attrs = {"name": "BALANCE_SHEET"}
        data = [df1, df2]
        metric_true = "INCOME_STATEMENT"
        metric_false = "RSI"
        symbol = "MSFT"
        dataframe = DataFrameFunctions(symbol=symbol)
        # get df metrics with correct dataframe name

        df_metrics_true = dataframe.get_df_metrics(data=data, df_name=metric_true)
        # get df metrics with incorrect dataframe name

        df_metrics_false = dataframe.get_df_metrics(
            data=data, df_name=metric_false
        )
        # check whether the dataframe is returned with the correct symbol

        assert df_metrics_true["symbol"][0] == symbol
        # check whether the dataframe is empty

        assert df_metrics_false.shape[0] == 0

    @pytest.mark.asyncio
    async def test_write_to_dataframe(self) -> None:
        """
        Function to test writing to dataframe
        :return: None
        """
        data = ["Q1", "Q2", "Q3"]
        df_name = "INCOME_STATEMENT"
        await DataProcessingFunctions.write_to_dataframe(data=data, df_name=df_name)
        assert len(Globals.DATAFRAME_LIST_GENERAL[0].index) == 3
        Globals.DATAFRAME_LIST_GENERAL[0].drop(
            Globals.DATAFRAME_LIST_GENERAL[0].index, inplace=True
        )


    @pytest.mark.asyncio
    async def test_check_variables_in_dataframe(self) -> None:
        symbol = "MSFT"
        dataframe = DataFrameFunctions(symbol=symbol)
        df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
        df2 = pd.DataFrame(TestDataFrameFunctions.DATA_DF2)
        data = [df1, df2]
        correct_variables = ["Age", "City"]
        incorrect_variables = ["Age", "RSI"]
        check_correct_variables = await dataframe.check_variables_in_dataframe(variables=correct_variables, list_df=data)
        check_incorrect_variables = await dataframe.check_variables_in_dataframe(variables=incorrect_variables, list_df=data)
        assert check_correct_variables is False
        assert check_incorrect_variables is True

    @pytest.mark.asyncio
    async def test_check_empty_dataframe(self) -> None:
        symbol = "MSFT"
        dataframe = DataFrameFunctions(symbol=symbol)
        df1 = pd.DataFrame(TestDataFrameFunctions.DATA_DF1)
        df2 = pd.DataFrame()
        data = [df1, df2]
        dataframes = ['normai', 'empty']
        empty_check = dataframe.check_empty_dataframe(list_df=data, dataframes=dataframes)
        assert empty_check is False


class TestDataProcessingFunctions:

    @pytest.mark.asyncio
    async def test_write_to_dataframe(self) -> None:
        """
        Function to test writing to dataframe
        :return: None
        """
        data = ["Q1", "Q2", "Q3"]
        df_name = "INCOME_STATEMENT"
        await DataProcessingFunctions.write_to_dataframe(data=data, df_name=df_name)
        assert len(Globals.DATAFRAME_LIST_GENERAL[0].index) == 3
        Globals.DATAFRAME_LIST_GENERAL[0].drop(
            Globals.DATAFRAME_LIST_GENERAL[0].index, inplace=True
        )
