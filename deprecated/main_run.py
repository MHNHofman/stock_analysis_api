# """Modules required for code"""
# import asyncio
# from codetiming import Timer
# from time import perf_counter
# from src.helper_functions import AsyncAPIFunctions, ExcelOperations, TradesOverview, Globals
# from src.technical_analysis import TradeTechnicalRequests
#
#
# async def main_stock_analysis() -> None:
#     """Function to run main"""
#     t = Timer(name="class")
#     t.start()
#     excel_operations = ExcelOperations()
#     api_function = AsyncAPIFunctions()
#     api_key = await api_function.async_load_api_keys()
#     trades = TradesOverview(api_key=api_key)
#     print('now get trades')
#     # get all symbols, or the selected ones based on cli or for test purposes
#     if len(Globals.STOCK_LIST) > 0:
#         symbol_list = await trades.get_trade_symbols()
#     else:
#         symbol_list = Globals.STOCK_LIST
#
#     trades_request = TradeTechnicalRequests(api_key=api_key)
#     await asyncio.gather(*(trades_request.get_trade_info(symbol) for symbol in symbol_list))
#     await excel_operations.clear_sheets()
#     await excel_operations.load_dataframes_into_excel()
#     t.stop()
#     return
#
#
# if __name__ == "__main__":
#     asyncio.run(main_stock_analysis(symbol=None), debug=True)
