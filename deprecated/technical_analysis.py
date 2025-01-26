# """Modules required for code"""
# import asyncio
# import sys
# import fmpsdk
# import pandas as pd
# import requests
# from time import perf_counter
#
# from pydantic import ValidationError
# from src.helper_features.pydantic_functions import ApiHandling
# from src.data_handlers import DataFrameFunctions, ExcelOperations, ResultsProcessing, TradesOverview
# from src.screener.stock_screener import StockScreener
#
#
# class TradeTechnicalRequests:
#     """Handles api requests for technical analysis
#
#     Parameters:
#             api_key (str): api key
#     """
#
#     def __init__(self, api_key: str):
#         """Docstring."""
#         self.api_key = api_key
#
#     async def get_income_statement(self, symbol: str) -> int:
#         """Function to get income statement"""
#         result = fmpsdk.income_statement(
#             apikey=self.api_key, symbol=symbol, period="quarter"
#         )
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_financial_ratios(self, symbol: str) -> int:
#         """Function to get financial ratios"""
#         result = fmpsdk.financial_ratios(
#             apikey=self.api_key, symbol=symbol, period="quarter"
#         )
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_cash_flow_statement(self, symbol: str):
#         """Function to get cash flow statement"""
#         result = fmpsdk.cash_flow_statement(
#             apikey=self.api_key, symbol=symbol, period="quarter"
#         )
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_statistical_indicators(self, symbol):
#         """Function to get technical indicators"""
#         indicators = ["standardDeviation", "rsa", "sma"]
#         # creates a number of coroutines
#         coros = [self.get_technical_indicators(symbol=symbol, statistics_type=i) for i in indicators]
#         for item in coros:
#             # awaits and get the result from the awaitable
#             await item
#         return ResultsProcessing.evaluate_results(result=coros)
#
#     async def get_technical_indicators(self, symbol: str, statistics_type: str):
#         """Function to get statistical indicator"""
#         result = fmpsdk.technical_indicators(
#             apikey=self.api_key, symbol=symbol, statistics_type=statistics_type
#         )
#         result_added_symbol = await ResultsProcessing.add_key(new_key='symbol', new_value=symbol, input_list=result)
#
#         dataframe_functions = DataFrameFunctions(symbol=symbol)
#         await dataframe_functions.process_api_request(result=result_added_symbol[0:60], symbol=symbol, df_name="_".join([sys._getframe().f_code.co_name[4:], statistics_type]))
#         return ResultsProcessing.evaluate_results(result=result)
#
#     async def get_rsi(self, symbol: str):
#         """Function to get rsi, not covered by fmpsdk"""
#         api_url = "https://financialmodelingprep.com/api/v3/technical_indicator/1day/{}?type=rsi&period=10&apikey={}".format(symbol, self.api_key)
#         response = requests.get(api_url)
#         result = response.json()[0:21]
#         result_added_symbol = await ResultsProcessing.add_key(new_key='symbol', new_value=symbol, input_list=result)
#         await ResultsProcessing.process_results(symbol=symbol, result=result_added_symbol, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_stock_price_change(self, symbol: str):
#         """Function to get changges in stock price change, not covered by fmpsdk"""
#         api_url = "https://financialmodelingprep.com/api/v3/stock-price-change/{}?apikey={}".format(symbol, self.api_key)
#         response = requests.get(api_url)
#         result = response.json()
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_insider_trading(self, symbol: str, limit: int) -> int:
#         """Function to get insider trading"""
#         result = fmpsdk.insider_trading(
#             apikey=self.api_key, symbol=symbol, limit=limit
#         )
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_key_metrics(self, symbol: str) -> bool:
#         """Function to get key metrics"""
#         result = fmpsdk.key_metrics(
#             apikey=self.api_key, symbol=symbol, period="quarter"
#         )
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     async def get_stock_price(self, symbol: str):
#         """Function to get stock price"""
#         result = fmpsdk.quote(
#             apikey=self.api_key, symbol=symbol
#         )
#         await ResultsProcessing.process_results(symbol=symbol, result=result, df_name=sys._getframe().f_code.co_name[4:])
#
#     # async def get_trade_info(self, symbol: str):
#     #     """Function to get trade info"""
#     #     # checks whether symbol is within allowed number of characters
#     #     try:
#     #         ApiHandling.check_length_symbol(symbol=symbol)
#     #     except ValidationError as e:
#     #         print(e)
#     #
#     #     # checks whether symbol is valid
#     #     trades = TradesOverview(self.api_key)
#     #     symbol_search = await trades.get_stock_basic_info(symbol=symbol)
#     #     if symbol_search is None:
#     #         print(f'Symbol {symbol} not found, please try again')
#     #         return None
#     #     await self.get_stock_data(symbol=symbol)
#     #     stock_screener = StockScreener(symbol=symbol)
#     #     if len(stock_screener.data) == 0:
#     #         print(f'Symbol {symbol} contains no data')
#     #         return None
#     #     await stock_screener.perform_stock_screener()
#     #     return True
#
#     async def get_stock_data(self, symbol: str):
#         # creates a number of coroutines
#         key_metrics = asyncio.create_task(self.get_key_metrics(symbol=symbol))
#         stock_price_change = asyncio.create_task(self.get_stock_price_change(symbol=symbol))
#         financial_ratios = asyncio.create_task(self.get_financial_ratios(symbol=symbol))
#         income_statement = asyncio.create_task(self.get_income_statement(symbol=symbol))
#         # cash_flow_statement = asyncio.create_task(self.get_cash_flow_statement(symbol=symbol))
#         # statistical_indicators = asyncio.create_task(self.get_statistical_indicators(symbol=symbol))
#         rsi = asyncio.create_task(self.get_rsi(symbol=symbol))
#         # insider_trading = asyncio.create_task(self.get_insider_trading(symbol=symbol, limit=50))
#         # record start time
#         time_start = perf_counter()
#         results = await asyncio.gather(key_metrics, financial_ratios, income_statement,
#                                        # cash_flow_statement,
#                                        # statistical_indicators,
#                                        rsi,
#                                        # insider_trading,
#                                        stock_price_change)
#         # record end time
#         time_end = perf_counter()
#         # calculate the duration
#         time_duration = time_end - time_start
#         # report the duration
#         print(f'Took {time_duration} seconds')
#         completed_tasks_check = list(filter(lambda x: x is False, results))
#         if len(completed_tasks_check) == 0:
#             print(f'All coroutines completed for {symbol}')
#         else:
#             print(f'There are {len(completed_tasks_check)} coroutines not completed for {symbol}')
#
#
# class TradeAnalysis:
#     """ Depreciated class, to be removed in future release
#     Determines whether stock meets criteria for investment
#
#     """
#     def __init__(self):
#         """Docstring."""
#         self.indicators = self.set_indicators()
#
#     @staticmethod
#     def set_indicators():
#         """Function to set indicators"""
#         indicators = ["peRatio", "debtToEquity", "roic", "roe", "grahamNumber", "dividendYield", "payoutRatio"]
#         return indicators
#
#     async def get_key_metrics_deprecated(self):
#         """Function to obtain key metrics"""
#         absolute_path = ExcelOperations.get_abs_path()
#
#         # get the dataframe for key metrics
#         df_key_metrics = pd.read_excel(absolute_path, sheet_name="key_metrics")
#         df_price = pd.read_excel(absolute_path, sheet_name="stock_price")
#         # get the latest key metric for each symbol
#         latest_key_metric = df_key_metrics.groupby('symbol').first().sort_values('date')[self.indicators]
#         merged_df = pd.merge(latest_key_metric, df_price, on="symbol", how="left")
#         # compare price with graham number and use pe ratio to determine whether stock is undervalued
#
#         return merged_df
#
#     async def evaluate_based_on_key_metrics(self, df_key_metrics: pd.DataFrame):
#         """Function to obtain key metrics"""
#         max_pe_ratio = 25
#         pe_filter = df_key_metrics.query('pe < @max_pe_ratio')
#
#
#
# # Stock Grade
# # Get a sense of how professional investors view a company with our Stock Grade endpoint. This endpoint provides a rating of a company given by hedge funds, investment firms, and analysts.
# #
# # Endpoint:
# #
# # https://financialmodelingprep.com/api/v3/grade/AAPL
# #
#
# # to do: find stocks that have growing eps ratios can be found under financial ratios, priceEarningsToGrowthRatio
