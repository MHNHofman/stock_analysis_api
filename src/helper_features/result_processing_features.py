# pylint: disable=line-too-long, missing-docstring
import asyncio
import logging
from collections import OrderedDict
import fmpsdk
import pandas as pd
from src.data_handlers import DataProcessingFunctions
from src.helper_features.common_calculations import get_day_difference


logger = logging.getLogger(__name__)


class ResultsProcessing:
    """Class to process results"""

    @staticmethod
    async def add_key(new_key: list, new_value: list, input_list: list) -> list:
        """Adds keys to the list of results from the API request
        :param list new_key: list of new keys to be added
        :param list new_value: list of new values to be added
        :param list input_list: list of dictionaries to which the new keys and values are added
        :return list: updated list of dictionaries
        """
        updated_list = [
            OrderedDict(
                [(new_key[0], new_value[0])]
                + [(new_key[1], new_value[1])]
                + list(dictionary.items())
            )
            for dictionary in input_list
            if isinstance(dictionary, dict)
        ]
        return updated_list

    @staticmethod
    def reorder_dict(new_order: list, dict_to_update: dict) -> dict:
        """Adds keys to the list of results from the API request
        :param list new_order: list of new keys to be added
        :param list dict_to_update: list of new values to be added
        :return list: updated dictionary
        """
        key_order = {k: v for v, k in enumerate(new_order)}
        new_dict = OrderedDict(
            sorted(dict_to_update.items(), key=lambda i: key_order.get(i[0]))
        )
        return new_dict

    @staticmethod
    async def handle_process_responses(
            responses: tuple | list, dataframe_names: list, symbol: str, name: str
    ) -> int:
        """Function to count the number of api requests and write the symbol name and dataframe name to the global dataframes
        :param tuple responses: tuple of responses from the API requests
        :param list dataframe_names: list of names of the dataframes
        :param str symbol: the symbol of the stock
        :param str name: the name of the stock
        :return int: the number of requests
        """
        number_of_requests = 0
        for index, response in enumerate(responses):
            number_of_requests += 1
            # the rsi list is very long, so we only take the first 21 values

            if dataframe_names[index] == "rsi":
                response = response[0:21]
            # if the response is empty, we skip the stock
            if response is False:
                break
            # add the symbol and name to the response
            # TODO: in case of stock price df, add country and stock exchange #pylint: disable=fixme

            result_added_symbol = await ResultsProcessing.add_key(
                new_key=["symbol", "name"],
                new_value=[symbol, name],
                input_list=response,
            )

            df_name = dataframe_names[index]

            # limits the sheet name to 31 characters
            if len(df_name) > 31:
                sheet_name = df_name[:31]
            else:
                sheet_name = df_name

            # write the results (data) of the requests to the global dataframes
            # all the results are written to the global dataframes, even though the stock screener may not use all of them
            # the results can be used for further analysis using pyspark or other tools

            if len(result_added_symbol) > 0:
                await DataProcessingFunctions.write_to_dataframe(
                    data=result_added_symbol, df_name=sheet_name
                )
        return number_of_requests

    @staticmethod
    def relative_difference(x: float, y: float) -> float:
        """Function to calculate the relative difference between two values with two decimal places
        :param float x: the first value
        :param float y: the second value
        :return float: the relative difference between the two values
        """

        if x == 0.0 or y == 0.0:
            return 0
        if x > y:
            return round(abs(x / y), 2)
        return round(abs(y / x), 2)

    @staticmethod
    def greater_than(x: float, y: float) -> bool:
        """Function to check whether x is greater than y
        :param float x: the first value
        :param float y: the second value
        :return bool: True if x is greater than y, False otherwise
        """
        return x > y

    @staticmethod
    def less_than(x: float, y: float) -> bool:
        """Function to check whether x is less than y
        :param float x: the first value
        :param float y: the second value
        :return bool: True if x is less than y, False otherwise
        """
        return x < y

    @staticmethod
    def equal_to(x: float, y: float) -> bool:
        """Function to check whether x is equal to y
        :param float x: the first value
        :param float y: the second value
        :return bool: True if x is equal to y, False otherwise
        """
        return x == y


class InsiderTrading:

    def __init__(self, symbol: str, api_key: str):
        self.symbol = symbol
        self.api_key = api_key

    # TODO: check return int value #pylint: disable=fixme

    async def get_insider_trading(self, limit: int):
        """Function to get insider trading
        :param int limit: the number of results to be returned
        """

        result = fmpsdk.insider_trading(
            apikey=self.api_key, symbol=self.symbol, limit=limit
        )

        if result is None:
            return
        list_one_to_six_months = []
        list_six_to_twelve_months = []

        for transaction in result:
            if "transactionDate" not in transaction:
                continue
            # TODO: define a pydantic object for transaction
            diff_days = get_day_difference(
                target_date_str=transaction["transactionDate"]
            )

            # if the transaction is older than 365 days, we break the loop
            if diff_days > 365:
                break
            # if the transaction is older than 180 days, we add it to the list of transactions between 6 and 12 months
            if 365 > diff_days > 180:
                list_six_to_twelve_months.append(transaction)
                continue
            # if the transaction is newer than 180 days, we add it to the list of transactions of the last 6 months
            list_one_to_six_months.append(transaction)
        calc_1_6_months = asyncio.create_task(
            self.calculate_transactions(
                transactions=list_one_to_six_months, period="0-6"
            )
        )
        calc_6_12_months = asyncio.create_task(
            self.calculate_transactions(
                transactions=list_six_to_twelve_months, period="6-12"
            )
        )

        await asyncio.gather(calc_1_6_months, calc_6_12_months)

    async def calculate_transactions(self, transactions: list, period: str) -> None:
        """Function to calculate the total stocks bought and sold and the average buying and selling price
        :param list transactions: list of transactions for the stock
        :param str period: the period in months when the transactions have taken place
        """
        total_bought = 0
        total_sold = 0
        total_bought_price = 0
        total_sold_price = 0
        average_buying_price = 0
        average_selling_price = 0
        # Initialize index counter

        index_bought = 0
        index_sold = 0

        for transaction in transactions:
            # TODO: define a pydantic object for transaction #pylint: disable=fixme

            if transaction["acquistionOrDisposition"] == "A":
                total_bought += transaction["securitiesTransacted"]
                total_bought_price += transaction["price"]
                # only if price is listed, then we increment the index to calculate the average price

                if transaction["price"] > 0:
                    index_bought += 1
            else:
                total_sold += transaction["securitiesTransacted"]
                total_sold_price += transaction["price"]
                # only if price is listed, then we increment the index to calculate the average price

                if transaction["price"] > 0:
                    index_sold += 1
        # Calculate the average buying and selling price

        if index_bought > 0 and total_bought_price > 0:
            average_buying_price = total_bought_price / index_bought
        if index_sold > 0 and total_sold_price > 0:
            average_selling_price = total_sold_price / index_sold
        data = {
            "symbol": [self.symbol],
            "time period": [period],
            "total stocks bought": [total_bought],
            "total stocks sold": [total_sold],
            "average buying price": [average_buying_price],
            "average selling price": [average_selling_price],
        }

        df = pd.DataFrame(data)
        # Set the name of the DataFrame using attrs

        df.attrs["name"] = "insider_trading"
        await DataProcessingFunctions.write_to_dataframe(
            data=df, df_name="insider_trading"
        )

    # @staticmethod
    # def convert_list_tuples_to_dict(list_of_tuples: list) -> dict:
    #     """Function to convert list of tuples to dictionary - currently not used"""
    #     result_dict = {}
    #     for key, value in list_of_tuples:
    #         if key in result_dict:
    #             # Handle duplicate keys
    #
    #             if not isinstance(result_dict[key], list):
    #                 # If the value is not a list, convert it to a list
    #
    #                 result_dict[key] = [result_dict[key]]
    #             result_dict[key].append(value)
    #         else:
    #             result_dict[key] = value
    #     return result_dict
