"""Module to get earnings calendar and earnings surprises"""
import asyncio
from datetime import datetime
from codetiming import Timer
import fmpsdk
from dateutil.relativedelta import relativedelta
from src.helper_features.api_features import SyncAPIFunctions
from stock_main_run import run_stock_api

class Shares:
    """Class to store shares with earnings surprises"""
    earnings_shares = []


class EarningsCalendar(SyncAPIFunctions):
    """Class to get earnings calendar and earnings surprises"""

    def __init__(self):
        super().__init__()
        self.api_key = self.sync_load_api_keys()
        self.symbols = []
        self.shares_with_earnings_surprises = []
        self.start_date = (datetime.now() + relativedelta(days=10)).strftime("%Y-%m-%d")
        self.end_date = (datetime.now() + relativedelta(days=42)).strftime("%Y-%m-%d")

    async def get_stock_name(self, stock_symbol_list: list):
        """Function to get stock name"""
        for share in stock_symbol_list:
            names = fmpsdk.search_ticker(apikey=self.sync_load_api_keys(), query=share)
            if names and len(names) > 0:
                # we take the first name in the list of results for names

                inner_list = [share, names[0]["name"]]
            else:
                inner_list = [share, "name not found"]
            self.symbols.append(inner_list)

    async def async_get_earnings_surprises(self, share: str):
        """Function to get earnings surprises"""
        share_earnings = fmpsdk.earnings_surprises(apikey=self.api_key, symbol=share)
        if share_earnings:
            calculate_surprise = await self.calculate_earnings_surprise(
                earnings_result=share_earnings[0]
            )
            if calculate_surprise is True:
                self.shares_with_earnings_surprises.append(share)

    @classmethod
    async def calculate_earnings_surprise(cls, earnings_result: dict):
        """Function to calculate whether the last earning call resulted in an earnings surprise"""

        if (
                "estimatedEarning" in earnings_result
                and "actualEarningResult" in earnings_result
        ):
            estimated = earnings_result["estimatedEarning"]
            actual = earnings_result["actualEarningResult"]
            if isinstance(actual, (int, float)) and isinstance(estimated, (int, float)):
                difference = actual - estimated

                if difference > 0:
                    return True
        return False

    async def earnings_analysis(self):
        """Function to get earnings calendar and earnings surprises"""
        earnings_calendar_overview = fmpsdk.earning_calendar(
            apikey=self.api_key, from_date=self.start_date, to_date=self.end_date
        )
        stock_symbol_list = [s["symbol"] for s in earnings_calendar_overview][:40]

        tasks = [
            self.async_get_earnings_surprises(share) for share in stock_symbol_list
        ]
        await asyncio.gather(*tasks)
        await self.get_stock_name(self.shares_with_earnings_surprises)
        Shares.earnings_shares = self.symbols


async def earnings_calendar_run():
    """Function to run earnings calendar"""
    earnings = EarningsCalendar()
    await earnings.earnings_analysis()


if __name__ == "__main__":
    print("start run")
    t = Timer(name="class")
    t.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(earnings_calendar_run())
    t.stop()
    duration_seconds = round(t.last, 2)
    run_stock_api(
        predefined_symbols=Shares.earnings_shares,
        duration_previous_run=duration_seconds,
    )

    # earnings_surprises = earnings.get_earnings_surprises(symbols_earnings_calendar)
    # run_stock_api(predefined_symbols=earnings_surprises)
    # def sync_calculate_earnings_surprise(self, earnings_result: dict):
    #
    #     if 'estimatedEarning' in earnings_result and 'actualEarningResult' in earnings_result:
    #         estimated = earnings_result['estimatedEarning']
    #         actual = earnings_result['actualEarningResult']
    #         if isinstance(actual, (int, float)) and isinstance(estimated, (int, float)):
    #             difference = actual - estimated
    #
    #             if difference > 0:
    #                 return True
    #     return False

    # async def async_task(self, share):
    #     names = fmpsdk.search_ticker(apikey=self.api_key, query=share)
    #     if len(names) == 0:
    #         inner_list = [share, 'name not found']
    #     else:
    #         inner_list = [share, names[0]['name']]
    #     self.symbols.append(share)

    # async def get_earnings_calendar(self):
    #     """Function to get insider trading"""
    #     print("start get_earnings_calendar")
    #     earnings_calendar_overview = fmpsdk.earning_calendar(
    #         apikey=self.api_key, from_date=self.start_date, to_date=self.end_date
    #     )
    #     stock_symbol_list = [s["symbol"] for s in earnings_calendar_overview]
    #     shares_list = await self.get_stock_name(
    #         stock_symbol_list=stock_symbol_list[:40]
    #     )
    #     return shares_list

    # def get_earnings_surprises(self, shares: list):
    #     shares_with_earnings_surprises = []
    #     print("start get_earnings_surprises")
    #     for share in shares:
    #         share_earnings = fmpsdk.earnings_surprises(
    #             apikey=self.api_key, symbol=share[0]
    #         )
    #         if len(share_earnings) > 0:
    #             calculate_surprise = self.calculate_earnings_surprise(
    #                 earnings_result=share_earnings[0]
    #             )
    #             if calculate_surprise is True:
    #                 shares_with_earnings_surprises.append(share)
    #     return shares_with_earnings_surprises
