#
# class StockScreener(DataFrameFunctions):
#     """Initiates. performs and evaluates screening on stocks based on predefined constraints
#
#     Parameters:
#             symbol (str): symbol of stock
#     """
#
#     def __init__(self, symbol: str):
#         """Docstring."""
#         super().__init__(symbol)
#         self.symbol: str = symbol
#         self.data: list = Globals.DATAFRAME_LIST_GENERAL
#         self.undervalued_metrics = (
#             StockScreenerConstraints.set_constraints_undervalued_stocks()
#         )
#         self.growth_stocks_metrics = (
#             StockScreenerConstraints.set_constraints_growth_stocks()
#         )
#         self.dip_metrics = StockScreenerConstraints.set_constraints_buy_dip()
#
#         self.undervalued_variables: list = ["peRatio", "roe", "rsi"]
#         self.dip_variables: list = ["peRatio", "1M", "1Y", "rsi"]
#         self.growth_stocks_variables: list = [
#             "peRatio",
#             "eps",
#             "roe",
#             "rsi",
#             "ebitdaratio",
#             "marketCap",
#         ]
#
#     async def perform_stock_screener(self):
#         """Perform screening on stocks based on predefined constraints"""
#
#         # create tasks for each analysis
#
#         undervalued_analysis = asyncio.create_task(
#             self.evaluate_stock_undervalued_metrics()
#         )
#         growth_analysis = asyncio.create_task(self.evaluate_stock_growth_metrics())
#         buy_on_the_dip_analysis = asyncio.create_task(
#             self.evaluate_stock_buy_on_the_dip_metrics()
#         )
#
#         await asyncio.gather(
#             undervalued_analysis, buy_on_the_dip_analysis, growth_analysis
#         )
#
#
# async def evaluate_stock_undervalued_metrics(self):
#     """Evaluate stock based on undervalued metrics"""
#
#     # which df to use for the metrics
#     # which variables to use for the metrics
#     # which dataframe object to use for the metrics
#     # check empty dataframe
#     # set variables for dataframes
#     # check if variables are in the dataframe
#     # set values for the variables
#     # evaluate values against constraints
#     # if meet constraints, write to global dataframe
#
#     print("now evaluating undervalued metrics")
#     # get the dataframes for the key metrics and rsi
#
#     key_metrics_df = await self.get_df_metrics(
#         data=self.data, df_name="key_metrics"
#     )
#     rsi_df = await self.get_df_metrics(data=self.data, df_name="rsi")
#
#     list_df = [key_metrics_df, rsi_df]
#     list_value_in_df = ["iloc", "iloc", "mean"]
#
#     # common function Check if an existing DataFrame is empty
#
#     check_dataframes = await self.check_empty_dataframe(list_df=list_df)
#     df_variable_list = [key_metrics_df, key_metrics_df, rsi_df]
#     check_variables = await self.check_variables_in_dataframe(
#         variables=self.undervalued_variables, list_df=df_variable_list
#     )
#
#     # if the dataframe is empty or the variables are not in the dataframe, return
#
#     if check_variables is True or check_dataframes is True:
#         return
#     # get the actual values for the variables
#
#     actual_values = await self.set_actual_values(
#         variables=self.undervalued_variables,
#         list_df=df_variable_list,
#         value_type=list_value_in_df,
#     )
#
#     # get the constraints for undervalued stocks
#
#     undervalued_constraints = (
#         StockScreenerConstraints.set_constraints_undervalued_stocks()
#     )
#
#     evaluation_value_constraint = await StockEvaluation.loop_trough_evaluations(
#         constraints=undervalued_constraints,
#         variables=self.undervalued_variables,
#         actual_values=actual_values,
#         symbol=self.symbol,
#     )
#
#     # separate function when stock meets the criteria, add the stock to the corresponding list
#
#     if evaluation_value_constraint is True:
#         await self.assign_transfer_dataframes(
#             constraint_type=self.evaluate_stock_undervalued_metrics.__name__
#         )
#
# async def evaluate_stock_growth_metrics(self):
#     """Evaluate stock based on growth metrics"""
#     # which df to use for the metrics
#     # which variables to use for the metrics
#     # which dataframe object to use for the metrics
#     # check empty dataframe
#     # set variables for dataframes
#     # check if variables are in the dataframe
#     # set values for the variables
#     # evaluate values against constraints
#     # if meet constraints, write to global dataframe
#
#     print("now evaluating growth metrics")
#
#     # get the dataframes for the key metrics and rsi
#
#     key_metrics_df = await self.get_df_metrics(
#         data=self.data, df_name="key_metrics"
#     )
#
#     income_statement_df = await self.get_df_metrics(
#         data=self.data, df_name="income_statement"
#     )
#
#     rsi_df = await self.get_df_metrics(data=self.data, df_name="rsi")
#
#     list_df = [
#         key_metrics_df,
#         income_statement_df,
#         key_metrics_df,
#         rsi_df,
#         income_statement_df,
#         key_metrics_df,
#     ]
#     list_value_in_df = ["iloc", "percentage_diff", "iloc", "mean", "iloc", "iloc"]
#
#     # common function Check if an existing DataFrame is empty
#
#     check_dataframes = await self.check_empty_dataframe(list_df=list_df)
#     df_variable_list = [
#         key_metrics_df,
#         income_statement_df,
#         key_metrics_df,
#         rsi_df,
#         income_statement_df,
#         key_metrics_df,
#     ]
#     check_variables = await self.check_variables_in_dataframe(
#         variables=self.growth_stocks_variables, list_df=df_variable_list
#     )
#
#     # if the dataframe is empty or the variables are not in the dataframe, return
#
#     if check_variables is True or check_dataframes is True:
#         return
#     # get the actual values for the variables
#
#     actual_values = await self.set_actual_values(
#         variables=self.growth_stocks_variables,
#         list_df=df_variable_list,
#         value_type=list_value_in_df,
#     )
#
#     # get the constraints for undervalued stocks
#
#     growth_stock_constraints = (
#         StockScreenerConstraints.set_constraints_growth_stocks()
#     )
#
#     evaluation_value_constraint = await StockEvaluation.loop_trough_evaluations(
#         constraints=growth_stock_constraints,
#         variables=self.growth_stocks_variables,
#         actual_values=actual_values,
#         symbol=self.symbol,
#     )
#
#     # separate function when stock meets the criteria, add the stock to the corresponding list
#
#     if evaluation_value_constraint is True:
#         await self.assign_transfer_dataframes(
#             constraint_type=self.evaluate_stock_growth_metrics().__name__
#         )
#
# async def evaluate_stock_buy_on_the_dip_metrics(self):
#     """Evaluate stock based on buy on the dip metrics"""
#
#     # get the dataframes for the key metrics and rsi
#
#     key_metrics_df = await self.get_df_metrics(
#         data=self.data, df_name="key_metrics"
#     )
#     stock_price_df = await self.get_df_metrics(
#         data=self.data, df_name="stock_price_change"
#     )
#     rsi_df = await self.get_df_metrics(data=self.data, df_name="rsi")
#     list_df = [key_metrics_df, stock_price_df, rsi_df]
#     list_value_in_df = ["iloc", "iloc", "iloc", "mean"]
#
#     # common function Check if an existing DataFrame is empty
#
#     check_dataframes = await self.check_empty_dataframe(list_df=list_df)
#     df_variable_list = [key_metrics_df, stock_price_df, stock_price_df, rsi_df]
#     check_variables = await self.check_variables_in_dataframe(
#         variables=self.dip_variables, list_df=df_variable_list
#     )
#
#     # if the dataframe is empty or the variables are not in the dataframe, return
#
#     if check_variables is True or check_dataframes is True:
#         return
#     # get the actual values for the variables
#
#     actual_values = await self.set_actual_values(
#         variables=self.dip_variables,
#         list_df=df_variable_list,
#         value_type=list_value_in_df,
#     )
#
#     # get the constraints for undervalued stocks
#
#     dip_constraints = StockScreenerConstraints.set_constraints_buy_dip()
#
#     evaluation_value_constraint = await StockEvaluation.loop_trough_evaluations(
#         constraints=dip_constraints,
#         variables=self.dip_variables,
#         actual_values=actual_values,
#         symbol=self.symbol,
#     )
#
#     # separate function when stock meets the criteria, add the stock to the corresponding list
#
#     if evaluation_value_constraint is True:
#         await self.assign_transfer_dataframes(
#             constraint_type=self.evaluate_stock_buy_on_the_dip_metrics().__name__
#         )