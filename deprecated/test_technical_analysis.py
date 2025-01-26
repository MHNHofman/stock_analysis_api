# import pytest
# from src.data_handlers import (
#     AsyncAPIFunctions
# )
# from src.deprecated.technical_analysis import TradeTechnicalRequests, TradeAnalysis
#
#
# class TestTradeTechnicalRequests:
#     @pytest.mark.asyncio
#     async def test_get_income_statement(self) -> None:
#         """
#         Function to test the Upload File Method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         income_statement = await trade_request.get_income_statement(symbol=symbol)
#         assert income_statement == 10
#
#     @pytest.mark.asyncio
#     async def test_get_financial_ratios(self) -> None:
#         """
#         Function to test the Upload File Method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         financial_ratios = await trade_request.get_financial_ratios(symbol=symbol)
#         assert financial_ratios is None
#
#     @pytest.mark.asyncio
#     async def test_get_trade_info(self) -> None:
#         """
#         Function to test the trade info method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         trade_info = await trade_request.get_trade_info(symbol=symbol)
#         assert trade_info is None
#
#
#     @pytest.mark.asyncio
#     async def test_get_stock_price_change(self) -> None:
#         """
#         Function to test the trade info method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         stock_price = await trade_request.get_stock_price_change(symbol=symbol)
#         assert stock_price is None
#
#     @pytest.mark.asyncio
#     async def test_get_statistical_indicators(self) -> None:
#         """
#         Function to test the statistical indicators method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         statistical_method = await trade_request.get_statistical_indicators(symbol=symbol)
#         assert statistical_method is None
#
#     @pytest.mark.asyncio
#     async def test_get_rsi(self) -> None:
#         """
#         Function to test the get_rsi method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         rsi_ratio = await trade_request.get_rsi(symbol=symbol)
#         assert rsi_ratio is True
#
#     @pytest.mark.asyncio
#     async def test_get_insider_trading(self) -> None:
#         """
#         Function to test insider trading method
#         :return: None
#         """
#         symbol = "MSFT"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         insider_trading = await trade_request.get_insider_trading(
#             symbol=symbol, limit=100
#         )
#         print(insider_trading)
#         assert insider_trading is True
#
#     @pytest.mark.asyncio
#     async def test_get_key_metrics(self) -> None:
#         """
#         Function to test key metrics method
#         :return: None
#         """
#         symbol = "NVA"
#         api_key = await AsyncAPIFunctions.async_load_api_keys()
#         trade_request = TradeTechnicalRequests(api_key)
#         key_metrics = await trade_request.get_key_metrics(symbol=symbol)
#         print("ok")
#         # assert insider_trading == 100
#
#
#
#
#
#
#
#
# def test_simple():
#     list_of_dicts = [
#         {"name": "Alice", "age": 30},
#         {"name": "Bob", "age": 25},
#         {"name": "Charlie", "age": 35},
#     ]
#
#     dict_list = [
#         {
#             "symbol": "MSFT",
#             "date": "2023-12-31",
#             "calendarYear": "2024",
#             "period": "Q2",
#             "revenuePerShare": 8.344994617868675,
#             "netIncomePerShare": 2.942680301399354,
#             "operatingCashFlowPerShare": 2.5367330462863293,
#             "freeCashFlowPerShare": 1.2268568353067815,
#             "cashPerShare": 10.896393972012918,
#             "bookValuePerShare": 32.05974165769645,
#             "tangibleBookValuePerShare": 12.034580193756728,
#             "shareholdersEquityPerShare": 32.05974165769645,
#             "interestDebtPerShare": 12.01332077502691,
#             "marketCap": 2794729280000,
#             "enterpriseValue": 2865798280000,
#             "peRatio": 31.94706538637403,
#             "priceToSalesRatio": 45.06174266365689,
#             "pocfratio": 148.23790802524798,
#             "pfcfRatio": 306.50683044527307,
#             "pbRatio": 11.729352158074102,
#             "ptbRatio": 11.729352158074102,
#             "evToSales": 46.207647210577235,
#             "enterpriseValueOverEBITDA": 85.40345333174395,
#             "evToOperatingCashFlow": 152.00754680952633,
#             "evToFreeCashFlow": 314.3011932441325,
#             "earningsYield": 0.00782544490320007,
#             "freeCashFlowYield": 0.0032625700332591786,
#             "debtToEquity": 0.37090167374553024,
#             "debtToAssets": 0.18780681658796577,
#             "netDebtToEBITDA": 2.1179222791751102,
#             "currentRatio": 1.2179629139948436,
#             "interestCoverage": 29.73817381738174,
#             "incomeQuality": 0.8620484682213078,
#             "dividendYield": 0.0019944686735453676,
#             "payoutRatio": 0.25486968449931413,
#             "salesGeneralAndAdministrativeToRevenue": 0.031876813930990004,
#             "researchAndDdevelopementToRevenue": 0.11515640116091583,
#             "intangiblesToTotalAssets": 0.31627769584195786,
#             "capexToOperatingCashFlow": -0.5163634434837957,
#             "capexToRevenue": -0.1569654950016124,
#             "capexToDepreciation": -1.6336633663366336,
#             "stockBasedCompensationToRevenue": 0.04559819413092551,
#             "grahamNumber": 46.07260933017851,
#             "roic": 0.06539724203865166,
#             "returnOnTangibleAssets": 0.06797604209728003,
#             "grahamNetNet": -15.928047631862217,
#             "workingCapital": 26377000000,
#             "tangibleAssetValue": 89441000000,
#             "netCurrentAssetValue": -84897000000,
#             "investedCapital": 0.37090167374553024,
#             "averageReceivables": 39892000000,
#             "averagePayables": 18501000000,
#             "averageInventory": 2307500000,
#             "daysSalesOutstanding": 62.153982586262494,
#             "daysPayablesOutstanding": 81.1573153951995,
#             "daysOfInventoryOnHand": 7.407124292921571,
#             "receivablesTurnover": 1.4480166234736522,
#             "payablesTurnover": 1.1089573325798248,
#             "inventoryTurnover": 12.15046439628483,
#             "roe": 0.09178739906323971,
#             "capexPerShare": -1.3098762109795479,
#         },
#         {
#             "symbol": "MSFT",
#             "date": "2023-09-30",
#             "calendarYear": "2024",
#             "period": "Q1",
#             "revenuePerShare": 7.580899466648787,
#             "netIncomePerShare": 2.990000000195837,
#             "operatingCashFlowPerShare": 4.102246198285823,
#             "freeCashFlowPerShare": 2.772030864656012,
#             "cashPerShare": 19.30804136324928,
#             "bookValuePerShare": 29.605439865561166,
#             "tangibleBookValuePerShare": 19.319308690871033,
#             "shareholdersEquityPerShare": 29.605439865561166,
#             "interestDebtPerShare": 11.47040778864774,
#             "marketCap": 2353974330949.5,
#             "enterpriseValue": 2358511330949.5,
#             "peRatio": 26.40050167051164,
#             "priceToSalesRatio": 41.650730416503,
#             "pocfratio": 76.97002684332799,
#             "pfcfRatio": 113.90565813168973,
#             "pbRatio": 10.665269674553947,
#             "ptbRatio": 10.665269674553947,
#             "evToSales": 41.73100714739813,
#             "enterpriseValueOverEBITDA": 76.53528462323143,
#             "evToOperatingCashFlow": 77.11837723406795,
#             "evToFreeCashFlow": 114.12519747166844,
#             "earningsYield": 0.00946951702358143,
#             "freeCashFlowYield": 0.008779195137469555,
#             "debtToEquity": 0.38506392888534485,
#             "debtToAssets": 0.19065020133023766,
#             "netDebtToEBITDA": 0.14722871235721702,
#             "currentRatio": 1.663455990768639,
#             "interestCoverage": 51.22857142857143,
#             "incomeQuality": 1.371988694989009,
#             "dividendYield": 0.0021457328287698987,
#             "payoutRatio": 0.22659369252164552,
#             "salesGeneralAndAdministrativeToRevenue": 0.02608064830051135,
#             "researchAndDdevelopementToRevenue": 0.11782295592476599,
#             "intangiblesToTotalAssets": 0.1720223874737822,
#             "capexToOperatingCashFlow": -0.32426511460615376,
#             "capexToRevenue": -0.17546932781287047,
#             "capexToDepreciation": -2.5292017342514663,
#             "stockBasedCompensationToRevenue": 0.044358334660367676,
#             "grahamNumber": 44.628533104798315,
#             "roic": 0.06884046304460768,
#             "returnOnTangibleAssets": 0.060392847466811166,
#             "grahamNetNet": -6.963107869102604,
#             "workingCapital": 82794000000,
#             "tangibleAssetValue": 144029000000,
#             "netCurrentAssetValue": -17485000000,
#             "investedCapital": 0.38506392888534485,
#             "averageReceivables": 42820500000,
#             "averagePayables": 18701000000,
#             "averageInventory": 2750000000,
#             "daysSalesOutstanding": 58.84548012102554,
#             "daysPayablesOutstanding": 106.58998895841,
#             "daysOfInventoryOnHand": 16.562384983437614,
#             "receivablesTurnover": 1.5294292750250318,
#             "payablesTurnover": 0.8443569689749831,
#             "inventoryTurnover": 5.434,
#             "roe": 0.10099495274427539,
#             "capexPerShare": -1.3302153336298108,
#         }
#     ]
#
#     # List comprehension to iterate through the list of dictionaries
#     metrics = ['symbol', 'date', 'peRatio']
#     result = [(key, value) for d in list_of_dicts for key, value in d.items()]
#     test = [d for d in dict_list]
#     print(test)
#     dict_test = [(key, value) for d in dict_list for key, value in d.items() if key in metrics]
#
#     print(result)
#
#
#
#
# # these are deprecated functions
# class TestDeprecatedFunctions:
#
#     @pytest.mark.asyncio
#     async def test_get_key_metrics(self) -> None:
#         """
#         Function to test key metrics
#         :return: None
#         """
#         trade_analysis = TradeAnalysis()
#         metrics = await trade_analysis.get_key_metrics_deprecated()
#         check_missing_values = metrics["symbol"].isnull().values.any() is False
#
#         assert check_missing_values is False
#         print("ok")
#
#     @pytest.mark.asyncio
#     async def test_evaluate_based_on_key_metrics(self) -> None:
#         """
#         Function to obtain key metrics
#         :return: None
#         """
#         trade_analysis = TradeAnalysis()
#         metrics = await trade_analysis.get_key_metrics_deprecated()
#         filter_metrics = await trade_analysis.evaluate_based_on_key_metrics(
#             df_key_metrics=metrics
#         )
#         print("ok")
#         # return
#
#         # for count, trade in enumerate(key_metric):
#         #
#         #     # get the list for the spefic key metric
#         #     overview_of_key_metric = df.groupby(['symbol', 'date', f'{key_metric[count]}']).size().reset_index().sort_values(['symbol', 'date'], ascending=[True, False])
#         #
#         #     print(trade)
#         #
#         # # get the mean, standard deviation, min and max for a key metric
#         # statistical_indicators = df.groupby(["symbol"])[key_metric].agg(
#         #     [np.mean, np.std, np.min, np.max]
#         # )
#         #
#         # # set the limit for pe_ration that we are interested in
#         # pe_ratio = np.where(statistical_indicators["peRatio"]["mean"] < 15)
#         #
#         # print("ok")
