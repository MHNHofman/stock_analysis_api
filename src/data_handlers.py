"""Modules to handle data"""

# pylint: disable=line-too-long, too-few-public-methods, missing-docstring, too-many-locals

import logging
import pandas as pd
import fmpsdk

logger = logging.getLogger(__name__)


class Globals:
    """Definition of dataframes and stock lists"""

    DATAFRAME_LIST_UNDERVALUED_STOCKS: list = []
    DATAFRAME_LIST_GROWTH_STOCKS: list = []
    DATAFRAME_LIST_DIP_STOCKS: list = []
    DATAFRAME_LIST_MAGIC_FORMULA: list = []
    DATAFRAME_LIST_GENERAL: list = []
    STOCK_LIST: list = []
    STOCK_DATAFRAMES: list = []
    ANALYSIS_TYPE: str


class TradesOverview:
    """Obtains stock symbols for analysis

    Parameters:
            api_key (str): api key
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.trade_list: list = []
        # list of exchanges to include
        self.exchange_list_to_include: list = ["NYSE", "NASDAQ", "AMEX", "EURONEXT", "LSE"]
        # list of exchanges not to include (deprecated)
        # self.exchange_list_not_include: list = ["BSE", "JKT", "NSE", "TLV", "JNB"]


    async def check_and_get_symbols(self) -> list:
        """Function to check whether a symbol is valid - for cli or for test purposes
        :return list of symbols
        """

        symbols: list = []

        for symbol in Globals.STOCK_LIST:
            search_result = fmpsdk.search(apikey=self.api_key, query=symbol)
            if len(search_result) == 0:
                logger.info("Stock %s has no results from search request", symbol)
                continue
            # TODO: check whether the search_result can be defined as a pydantic object #pylint: disable=fixme
            # if the search result is not empty and the name is not empty, append the symbol to the list #pylint: disable=fixme

            if search_result and search_result[0]["name"]:
                inner_list = [symbol, search_result[0]["name"]]
                symbols.append(inner_list)
            # otherwise, the symbol is not considered valid

            else:
                logger.warning(
                    "Stock %s contains results that are not considered valid", symbol
                )
        return symbols

    async def get_trade_symbols(self) -> list:
        """Get all stocks that are available by the FMP API
        :return list of symbols
        """
        self.trade_list = fmpsdk.available_traded_list(apikey=self.api_key)
        # now we filter for stocks that are traded within the preferred list of stock exchanges

        stock_list = [
            share
            for share in self.trade_list
            if share["type"] == "stock"
               and share["exchangeShortName"] in self.exchange_list_to_include
        ]


        symbols = []
        count = 0
        # set the maximum number of symbols to include in the analysis
        max_symbols = 10
        # iterate through the trade list and append the symbols to the list

        logger.info("Number of symbols in trade list: %s", len(stock_list))
        logger.info("Max number of %s symbols included in analysis", max_symbols)

        for count, trade in enumerate(stock_list):

            # if the count is greater than a certain number, break the loop - the number of symbols can be adjusted

            if count > max_symbols:
                break
            inner_list = [trade["symbol"], trade["name"]]
            symbols.append(inner_list)
            count += 1
        return symbols

    async def get_symbol_name(self, symbol: str) -> bool:
        """Function to check whether a symbol is valid
        :param symbol: stock symbol
        :return: boolean if the stock symbol was found True, otherwise False
        """
        search_result = fmpsdk.search(apikey=self.api_key, query=symbol)
        if search_result:
            return True
        return False


class DataFrameFunctions:
    """Write data to dataframe

    Parameters:
            symbol (str): stock symbol
    """

    def __init__(self, symbol: str):
        self.symbol = symbol

    async def transfer_dataframes(self, data: list):
        """Function to transfer data to the global dataframes that belongs to stock screeners
        :param data: list of dataframes containing the results of the API requests
        """
        for index, dataframe in enumerate(Globals.DATAFRAME_LIST_GENERAL):
            # get dataframe for only the relevant stock

            filtered_df = dataframe[dataframe["symbol"] == self.symbol]

            # TODO: define a pydantic object for the filtered_df dataframe #pylint: disable=fixme
            # in case the dataframe not yet exists, append new dataframe to the respective global dataframe of the stock screener

            if len(data) < len(Globals.DATAFRAME_LIST_GENERAL):
                data.append(filtered_df)
            else:
                # in case the dataframe already exists, add the new data to the corresponding dataframe, e.g. income_statement
                if filtered_df.attrs["name"] == data[index].attrs["name"]:
                    data[index] = pd.concat(
                        [data[index], filtered_df],
                        names=filtered_df.attrs["name"],
                        ignore_index=True,
                    )
        return

    async def assign_transfer_dataframes(self, screener_type: str):
        """Function to transfer data to dataframes that belongs to stock screeners
        :param screener_type type of stock screener - e.g. undervalued
        """
        if "dip" in screener_type.lower():
            await self.transfer_dataframes(data=Globals.DATAFRAME_LIST_DIP_STOCKS)
        if "growth" in screener_type.lower():
            await self.transfer_dataframes(data=Globals.DATAFRAME_LIST_GROWTH_STOCKS)
        if "undervalued" in screener_type.lower():
            await self.transfer_dataframes(
                data=Globals.DATAFRAME_LIST_UNDERVALUED_STOCKS
            )
        if "magic" in screener_type.lower():
            await self.transfer_dataframes(data=Globals.DATAFRAME_LIST_MAGIC_FORMULA)

    def get_df_metrics(self, data: list, df_name: str) -> pd.DataFrame:
        """Function to get metrics for dataframe
        :param data: list of dataframes containing the results of the API requests
        :param df_name: name of the df
        :return: Dataframe filtered by name of the dataframe required
        """
        # filter dataframe based on metric and stock symbol
        # TODO: define a pydantic object for filter_df #pylint: disable=fixme

        filter_df = [df for df in data if df.attrs["name"] == df_name]
        # is nothing is found after filtering, return empty dataframe

        if len(filter_df) == 0:
            # logger.warning("DataFrame %s is empty", df_name)

            return pd.DataFrame()
        # return the filtered dataframe
        # TODO: filtering doesn't work, need to fix this #pylint: disable=fixme

        return filter_df[0]
        # (filter_df[0].loc)[filter_df[0]["symbol"] == self.symbol]

    def check_empty_dataframe(self, list_df: list, dataframes: list) -> bool:
        """Function to check whether the dataframe is empty
        :param list_df: list of dataframes containing the results of the API requests
        :param dataframes: list of names of the dataframes
        :return: boolean if the dataframe is empty True, otherwise False
        """

        for idx, df in enumerate(list_df):
            if df.empty:
                logger.warning(
                    "DataFrame in this stock is empty for %s", dataframes[idx]
                )
                return False
        return True

    async def check_variables_in_dataframe(
            self, variables: list, list_df: list
    ) -> bool:
        """Function to check whether the dataframe is empty
        :param variables: list of variables to check
        :param list_df: list of dataframes containing the results of the API requests
        :return: boolean if the variable is not in the dataframe True, otherwise False
        """

        # Loop with index using enumerate()

        for index, variable in enumerate(variables):
            if variable not in list_df[index].columns:
                logger.warning(
                    "The variable %s is not in dataframe for stock %s",
                    variable,
                    self.symbol,
                )
                return True
        return False


class GenericFunctions:
    """Functions that are generic in nature"""

    @staticmethod
    def percentage_difference(value1: int | float, value2: int | float) -> int | float:
        """Function to calculate the percentage difference between two values
        :param value1: first value
        :param value2: second value
        :return: percentage difference between the two values
        """
        difference = value2 - value1
        if difference > 0 and value1 != 0:
            positive_percentage = (difference / abs(value1)) * 100
            return positive_percentage
        if difference < 0 and value1 != 0:
            negative_percentage = (difference / abs(value1)) * 100
            return -abs(negative_percentage)
        # if the difference is 0, return 0
        return 0

    @staticmethod
    def is_dataframe(variable):
        """Function to check if a variable is a pandas DataFrame
        :param variable: variable to check
        :return: boolean if the variable is a DataFrame True, otherwise False
        """
        return isinstance(variable, pd.DataFrame)

    @staticmethod
    def set_sheet_name(df_name: str) -> str:
        """Function to set the name of the sheet
        :param df_name: name of the DataFrame
        :return: name of the sheet
        """
        if len(df_name) > 31:
            return df_name[:31]
        return df_name

    @staticmethod
    def set_dataframe_names() -> list:
        """Define the names of the dataframes
        :return: list of names of the dataframes
        """
        dataframe_names = [
            "income_statement",
            "ratios",
            "rsi",
            "stock_price",
            "key_metrics",
            "grades",
            "analyst_recommendations",
            "financial_score",
            "insider_trading",
        ]
        return dataframe_names

    @staticmethod
    def check_empty_lists(responses: list) -> bool:
        """Function to check whether a list is empty
        :param responses: list of responses
        :return: boolean if the list is empty True, otherwise False
        """
        check_empty = any(not response for response in responses)
        if check_empty:
            return True
        return False

    @staticmethod
    def check_constraint_in_variables(
            constraint_name: str, variables: list, value: float
    ) -> bool:
        """Function to check whether a constraint is in the variables
        :param constraint_name: name of the constraint
        :param variables: list of variables
        :param value: value of the constraint
        :return: boolean if the constraint is in the variables True, otherwise False
        """
        # check if constraint is in the variables and whether the value is None

        if constraint_name not in variables or value is None:
            return False
        return True

    @staticmethod
    def define_dataframe_weighted_scores(
            columns: list, screener_type: str
    ) -> pd.DataFrame:
        """Function to add the weighed scores to the DataFrame
        :param columns: list of columns
        :param screener_type: type of stock screener
        :return: DataFrame with weighted scores
        """

        # Create an empty DataFrame

        df = pd.DataFrame()

        # Define column names dynamically

        column_names = columns

        df["symbol"] = None
        df["total_score"] = None

        # Loop through the column names and add them to the DataFrame

        for column_name in column_names:
            df[f"{column_name}_score"] = None
            df[f"{column_name}_weight"] = None
        df.attrs["name"] = f"weighted_scores_{screener_type}"
        return df


class DataProcessingFunctions:
    """Functions to calculate data"""

    @staticmethod
    async def write_to_dataframe(data: list | pd.DataFrame, df_name: str):
        """Function to write the api request results to the main dataframe
        :param data: list of dataframes containing the results of the API requests
        :param df_name: name of the DataFrame
        """

        df_check = GenericFunctions.is_dataframe(data)

        if df_check is False:
            # Create a DataFrame from the data

            df = pd.DataFrame(data)
            # Set the name of the DataFrame

            df.attrs["name"] = df_name
        else:
            df = data
        # TODO: define a pydantic model for df as dataframe #pylint: disable=fixme

        for index, dataframe in enumerate(Globals.DATAFRAME_LIST_GENERAL):
            # in case the dataframe already exists, add the new data to it

            if dataframe.attrs["name"] == df_name:

                if df.empty:
                    return
                existing_df = Globals.DATAFRAME_LIST_GENERAL[index]

                Globals.DATAFRAME_LIST_GENERAL[index] = pd.concat(
                    [existing_df, df],
                    names=[df_name],
                    ignore_index=True,
                )

                # Append the dataframe to the list of dataframes for the stock currently analyzed

                Globals.STOCK_DATAFRAMES.append(df)

                return
        # in all other cases create a new dataframe

        Globals.DATAFRAME_LIST_GENERAL.append(df)

        return

    @staticmethod
    def set_actual_values(
            variables: list, list_df: list, name_df: list, value_type: list
    ) -> dict:
        """Function to set actual values for dataframe
        :param variables: list of variables
        :param list_df: list of dataframes containing the results of the API requests
        :param name_df: list of names of the dataframes
        :param value_type: list of value types
        :return actual values for the dataframe
        """
        # get the actual values for the dataframe

        actual_values: dict = {}

        # Loop to fill the dictionary with actual values

        for index, variable in enumerate(variables):

            filtered_df = [df for df in list_df if df.attrs["name"] == name_df[index]]
            required_df = filtered_df[0]

            # TODO: define a pydantic for required_df dataframe #pylint: disable=fixme

            if value_type[index] == "mean":
                value = required_df[variable].mean()
            elif value_type[index] == "percentage_diff":
                # check whether the dataframe has at least 3 values

                if len(required_df) < 3:
                    actual_values[variable] = 0
                    continue
                value0 = required_df[variable].iloc[2]
                value1 = required_df[variable].iloc[1]
                value2 = required_df[variable].iloc[0]
                diff_last_eps = GenericFunctions.percentage_difference(value1, value2)
                diff_previous_eps = GenericFunctions.percentage_difference(
                    value0, value1
                )
                # here we test whether the last eps difference is positive and the previous eps difference is negative

                a = diff_last_eps > 0
                b = diff_previous_eps < 0

                if a and b:
                    value = diff_last_eps
                else:
                    value = 0
            else:
                value = required_df[variable].iloc[0]
            actual_values[variable] = value
        return actual_values
