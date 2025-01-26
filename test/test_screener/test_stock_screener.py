import pytest
import pandas as pd


from src.screener.stock_screener import (
    StockScreener
)
from src.data_handlers import Globals
from src.helper_features.api_features import AsyncAPIFunctions

# next up, ensure that the test screening scripts are working as expected


class TestStockScreenerExecution:

    @pytest.mark.asyncio
    async def test_run_screener(self) -> None:
        """
        Function to test the evaluate_stock_undervalued_metrics method
        :return: None
        """

        # ['key_metrics', 'income_statement', 'rsi', 'ratios']

        df_rsi = {
            "symbol": ["MSFT", "MSFT", "MSFT"],
            "date": [
                "2024-11-01",
                "2024-10-01",
                "2024-09-01"
            ],
            "rsi": [40, 43, 41],
        }

        df_ratios = {
            "symbol": ["MSFT", "MSFT", "MSFT"],
            "peRatio": [8, 13, 12],
            "eps": [7.4, 6.5, 8.3],
            "roic": [0.10, 0.23, 0.14],
            "rsi": [50, 60, 70],
            "priceEarningsToGrowthRatio": [1.0, 1.2, 1.3],
            "marketCap": [900000000, 700000000, 1500000000]
        }

        df_key_metrics = {
            "symbol": ["MSFT", "MSFT", "MSFT"],
            "year": [2023, 2022, 2021],
            "peRatio": [8, 13, 12],
            "roic": [0.10, 0.23, 0.14],
            "earningsYield": [0.10, 0.23, 0.14],
            "returnOnTangibleAssets": [0.10, 0.23, 0.14],
            "enterpriseValueOverEBITDA": [5.0, 6.0, 7.0],
            "marketCap": [900000000, 700000000, 1500000000],
        }

        df_income_statement = {
            "symbol": ["MSFT", "MSFT", "MSFT"],
            "date": [
                "2024-11-01",
                "2024-10-01",
                "2024-09-01"
            ],
            "eps": [7.4, 6.5, 8.3]
        }

        df_rsi = pd.DataFrame(df_rsi)
        df_rsi.attrs["name"] = "rsi"
        df_key_metrics = pd.DataFrame(df_key_metrics)
        df_key_metrics.attrs["name"] = "key_metrics"
        df_income_statement = pd.DataFrame(df_income_statement)
        df_income_statement.attrs["name"] = "income_statement"
        df_ratios = pd.DataFrame(df_ratios)
        df_ratios.attrs["name"] = "ratios"
        df_list = [df_key_metrics, df_income_statement, df_rsi, df_ratios]
        Globals.DATAFRAME_LIST_GENERAL = []
        symbol = "MSFT"
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        stock_screener = StockScreener(symbol=symbol, api_key=api_key)
        stock_screener.symbol = symbol
        stock_screener.data = df_list
        screening_outcome = await stock_screener.execute_screening(screener_type="growth")
        assert screening_outcome is False
        # Clear the DataFrames
        Globals.DATAFRAME_LIST_GENERAL.clear()


class TestStockScreener:

    KEY_METRICS = {
        "symbol": ["MSFT", "MSFT", "MSFT"],
        "year": [2022, 2023, 2024],
        "peRatio": [12, 13, 12],
        "earningsYield": [0.03, 0.06, 0.08],
        "roe": [0.15, 0.22, 0.31],
        "roic": [0.40, 0.23, 0.34],
    }

    INCOME_STATEMENT = {
        "symbol": ["MSFT", "MSFT", "MSFT"],
        "year": [2022, 2023, 2024],
        "eps": [3, 1, 8]
    }

    RSI = {
        "symbol": ["MSFT", "MSFT", "MSFT"],
        "date": ["2024-11-01", "2024-10-01", "2024-09-01"],
        "rsi": [50, 60, 65],
    }

    RATIOS = {
        "symbol": ["MSFT", "MSFT", "MSFT"],
        "date": ["2024-11-01", "2024-10-01", "2024-09-01"],
        "priceEarningsToGrowthRatio": [0.1, 0.1, 0.1],
    }

    FINANCIAL_SCORE = {
        "symbol": ["MSFT", "MSFT", "MSFT"],
        "date": ["2024-11-01", "2024-10-01", "2024-09-01"],
        "piotroskiScore": [6,7,5],
    }


    @pytest.mark.asyncio
    async def test_evaluate_stock_growth_metrics(self) -> None:
        """
        Function to test the evaluate_stock_undervalued_metrics method
        :return: None
        """
        symbol = "MSFT"
        df_key_metrics = pd.DataFrame(self.KEY_METRICS)
        df_key_metrics.attrs["name"] = "key_metrics"
        df_income_statement = pd.DataFrame(self.INCOME_STATEMENT)
        df_income_statement.attrs["name"] = "income_statement"
        df_rsi = pd.DataFrame(self.RSI)
        df_rsi.attrs["name"] = "rsi"
        df_ratios = pd.DataFrame(self.RATIOS)
        df_ratios.attrs["name"] = "ratios"
        df_financials = pd.DataFrame(self.FINANCIAL_SCORE)
        df_financials.attrs["name"] = "financial_score"
        data = [df_key_metrics, df_income_statement, df_rsi, df_ratios, df_financials]
        api_key = await AsyncAPIFunctions.async_load_api_keys()
        stock_screener = StockScreener(symbol=symbol, api_key=api_key)
        stock_screener.data = data
        growth_test = (
                await stock_screener.execute_screening(screener_type="growth")
            )
        assert growth_test is True


    # @pytest.mark.asyncio
    # async def test_evaluate_stock_growth_metrics(self) -> None:
    #     """
    #     Function to test the evaluate_stock_growth_metrics method
    #     :return: None
    #     """
    #     symbol = "MSFT"
    #     df_key_metrics = pd.DataFrame(self.KEY_METRICS)
    #     df_key_metrics.attrs["name"] = "key_metrics"
    #     df_rsi = pd.DataFrame(self.RSI)
    #     df_rsi.attrs["name"] = "rsi"
    #     df_ratios = pd.DataFrame(self.RATIOS)
    #     df_ratios.attrs["name"] = "ratios"
    #     df_financials = pd.DataFrame(self.FINANCIAL_SCORE)
    #     df_financials.attrs["name"] = "financial_score"
    #     data = [df_key_metrics, df_rsi, df_ratios, df_financials]
    #     api_key = await AsyncAPIFunctions.async_load_api_keys()
    #     stock_screener = StockScreener(symbol=symbol, api_key=api_key)
    #     stock_screener.data = data
    #     growth_test = (
    #         await stock_screener.execute_screening(screener_type="growth")
    #     )
    #     assert growth_test is False