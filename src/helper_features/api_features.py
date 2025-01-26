# pylint: disable=missing-docstring, too-few-public-methods, line-too-long

import os
import time
import logging
import json
from datetime import datetime
import asyncio
import aiohttp
from dotenv import load_dotenv
from src.data_handlers import Globals, GenericFunctions
from src.helper_features.result_processing_features import ResultsProcessing
from src.screener.stock_screener import StockScreener

logger = logging.getLogger(__name__)


class AsyncAPIFunctions:
    """Class for all general API related functions"""

    @classmethod
    async def async_load_api_keys(cls) -> str | None:
        """Function to load API Key"""
        load_dotenv()
        api_key = os.getenv("FMP_API_KEY")
        return api_key

    @classmethod
    async def is_valid_json(cls, response):
        """Function to check if response is valid JSON
        :param response: response from API
        :return: True if response is valid JSON, False otherwise
        """
        try:
            await response.json()
            return True
        except aiohttp.ContentTypeError:
            logger.warning("response is not valid JSON")
            return False
        except json.JSONDecodeError:
            return False

    @classmethod
    async def fetch_url(cls, session, url, symbol):
        """Fetch an url, using specified ClientSession. If the response is 429, return False.
        :param session: aiohttp.ClientSession
        :param url: URL as string
        :param symbol: company stock symbol
        :return: dict or bool
        """
        async with session.get(url) as response:

            if response.status == 429:
                logger.warning("Rate limit exceeded for symbol: %s", symbol)
                time_str = response.headers.get("Date")
                time_format = "%a, %d %b %Y %H:%M:%S %Z"
                time_obj = datetime.strptime(time_str, time_format)
                seconds_passed = time_obj.second
                logger.warning("We are already at seconds passed: %s", seconds_passed)
                await asyncio.sleep(60 - seconds_passed + 1)
                return False
            if await AsyncAPIFunctions.is_valid_json(response):
                return await response.json(content_type=None)
            return False

    @classmethod
    async def handle_api_exceed_rate(cls, duration: float):
        # if the duration is < 60 seconds, wait for the remaining time to complete the 60 seconds

        if duration < 60:
            time_needed = 60 - duration + 1
            logger.info("Retrying after %s seconds...", int(round(time_needed)))
            await asyncio.sleep(60 - duration + 1)
        # in the unlikely event that the duration is more than 60 seconds, print a warning and retry

        else:
            time_needed = 60 - (duration - 60)
            logger.warning(msg="WATCH OUT 60 seconds passed!")
            logger.info("Retrying after %s seconds...", int(round(time_needed)))
            await asyncio.sleep(duration - 60)


class SyncAPIFunctions:
    """Class for all general API related functions"""

    @classmethod
    def sync_load_api_keys(cls) -> str | None:
        """Function to load API Key
        :return: str api key
        """
        load_dotenv()
        api_key = os.getenv("FMP_API_KEY")
        return api_key

    @classmethod
    def calculate_duration(cls, start_time, number_of_requests: int) -> float:
        """Function to handle API rate limit
        :param start_time: start time of function
        :param number_of_requests: number of requests made
        :return: duration of function
        """

        end_time = time.time()
        duration = end_time - start_time
        print(f"Function took {duration:.6f} seconds to execute")
        print(f"Total number of requests: {number_of_requests}")
        return duration


class StockUrlRequestHandling:

    def __init__(self, symbol_list: list, api_key: str, urls: list, session):
        self.symbol_list = symbol_list
        self.number_of_requests = 0
        self.api_key = api_key
        self.urls = urls
        self.session = session
        self.dataframe_names = GenericFunctions.set_dataframe_names()
        self.number_of_requests = 0
        self.number_of_stcoks = 0

    async def run_urls(self) -> int:
        # loop through the symbols and make the requests listed in the urls

        for symbol, name in self.symbol_list:
            self.number_of_requests += 1
            self.number_of_stcoks += 1
            modified_urls = [u.format(symbol, self.api_key) for u in self.urls]
            tasks = [
                asyncio.ensure_future(
                    AsyncAPIFunctions.fetch_url(self.session, url, symbol)
                )
                for url in modified_urls
            ]

            responses = await asyncio.gather(*tasks)
            logger.info("Stock %s will be analyzed", symbol)
            logger.info(
                "This is number %s in the total list of stocks", self.number_of_stcoks
            )

            # if the responses are empty, continue to the next symbol

            if responses == "" or responses is None:
                logger.warning("Stock has no response: %s", symbol)
                continue
            # check if the responses are empty, excluding the grades and recommendations given by analysts

            insufficient_data = GenericFunctions.check_empty_lists(responses[0:4])
            # if the symbol does not return any data from the executed urls, print a warning and continue to the next symbol

            if insufficient_data is True:
                logger.warning("Symbol %s contains insufficient data", symbol)
                continue
            # handle the responses and write the data to the global dataframes

            requests = await ResultsProcessing.handle_process_responses(
                responses=responses,
                dataframe_names=self.dataframe_names,
                symbol=symbol,
                name=name,
            )
            self.number_of_requests += requests

            stock_screener = StockScreener(symbol=symbol, api_key=self.api_key)
            # run the stock screeners set in the stock_metrics_constrains.py file

            await stock_screener.run_screeners()
            # clear the dataframes for the stock after the stock screener has run

            Globals.STOCK_DATAFRAMES.clear()
        return self.number_of_requests
