"""Main file to run the stock analysis"""

import sys
import os
# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import warnings
import logging
import asyncio
import aiohttp
from codetiming import Timer
from src.data_handlers import TradesOverview, Globals
from src.url_definitions import StockAnalysisURLs
from src.helper_features.excel_features import ExcelOperations
from src.helper_features.api_features import AsyncAPIFunctions, StockUrlRequestHandling
from src.helper_features.logging import LoggingFunctions
from src.helper_features.common_calculations import get_analysis_type

logger = logging.getLogger(__name__)

# pylint: disable=line-too-long


async def main(input_symbols: list | None) -> None:
    """Main function to run the program."""

    # standard type of analysis is a full analysis of all stocks collected

    async with aiohttp.ClientSession() as session:
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        trades = TradesOverview(api_key=api_key)

        # get all symbols, or the selected ones already listed in the global stock list based on cli or for test purposes

        if Globals.ANALYSIS_TYPE == "full":

            logger.info(msg="Running a full analysis for all stocks available")
            trades = TradesOverview(api_key=api_key)
            symbol_list = await trades.get_trade_symbols()
        elif Globals.ANALYSIS_TYPE == "earnings_calendar":
            symbol_list = input_symbols
        else:
            # in case of usage of cli or for test purposes, check if the symbols provided are valid

            symbol_list = await trades.check_and_get_symbols()
            if len(symbol_list) == 0:
                logger.warning(msg="None of the symbols provided were valid")
                warnings.warn("None of the symbols provided were valid", UserWarning)
            stock_names = "".join(str(x) for x in symbol_list)
            logger.info(
                "Running the cli for test purposes or with the CLI. The analyzed symbols are: %s ",
                stock_names,
            )
        request_handling = StockUrlRequestHandling(
            symbol_list=symbol_list,
            api_key=api_key,
            urls=StockAnalysisURLs.MainAnalysisURLs,
            session=session,
        )

        # by running the urls, the analysis is performed

        number_of_requests = await request_handling.run_urls()

        ######################################################################################
        # here you can perform the final operations

        excel_operations = ExcelOperations()
        await excel_operations.clear_sheets()
        await excel_operations.load_dataframes_into_excel()
        print(
            f"Stock analysis run completed. Total number of requests: {number_of_requests}"
        )
        logger.warning("Total number of requests: %s", number_of_requests)


def start_main_run():
    """Function to run the main analysis"""
    t = Timer(name="class")
    t.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(input_symbols=None))
    t.stop()


def run_stock_api(
        predefined_symbols: list | None, duration_previous_run: float | None = None
):
    """Function to run the stock analysis"""

    # determine the type of analysis based on the symbols provided

    Globals.ANALYSIS_TYPE = get_analysis_type(predefined_symbols=predefined_symbols)
    file_name = LoggingFunctions.determine_log_file_name()
    # Clear the log file before the process starts

    if Globals.ANALYSIS_TYPE != "cli":
        open(file_name, "w", encoding="utf-8").close()
        logging.basicConfig(
            filename=file_name,
            format="%(levelname)s - %(asctime)s - %(message)s",
            level=logging.INFO,
            force=True,
        )

        if Globals.ANALYSIS_TYPE == "earnings_calendar":
            logger.info(
                "Starting a stock analysis run based on the earnings calender with: %s number of shares",
                len(predefined_symbols),
            )
        else:
            logger.info("Start with stock analysis run")
    t = Timer(name="class")
    t.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(input_symbols=predefined_symbols))
    t.stop()
    logger.info("Finished stock analysis run")

    duration_stock_analysis_seconds = round(t.last, 2)
    duration_stock_analysis_minutes = round(duration_stock_analysis_seconds / 60, 2)
    if duration_previous_run:
        # duration_minutes = round((duration_previous_run + duration_stock_analysis_seconds) / 60, 2)

        duration_previous_run_minutes = round(duration_previous_run / 60, 2)
        logger.info(
            "Duration of the earnings_calendar run: %s seconds",
            str(duration_previous_run),
        )
        logger.info(
            "That is equivalent to %s minutes", str(duration_previous_run_minutes)
        )
    # logger.info("This is equivalent to %s minutes", str(duration_minutes))

    logger.info(
        "Duration of the stock api run: %s seconds",
        str(duration_stock_analysis_seconds),
    )
    logger.info(
        "The stock api run is equivalent to %s minutes",
        str(duration_stock_analysis_minutes),
    )


if __name__ == "__main__":
    START_SYMBOLS = None
    run_stock_api(predefined_symbols=START_SYMBOLS, duration_previous_run=None)