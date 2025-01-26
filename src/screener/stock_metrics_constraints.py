# This file contains the constraints for the stock metrics used in the stock screener

# pylint: disable=missing-docstring


class StockScreenerConstraints:
    """Determines whether stock meets criteria for investment"""

    @staticmethod
    def set_constraints_undervalued_stocks() -> tuple:
        """Function to set constraints for undervalued stocks"""

        metrics = {
            "screener": "undervalued",
            "variables": [
                "peRatio",
                "roe",
                "rsi",
                "earningsYield",
                "priceEarningsToGrowthRatio",
            ],
            "dataframes": ["key_metrics", "rsi", "ratios"],
            "dataframe_list": [
                "key_metrics",
                "key_metrics",
                "rsi",
                "key_metrics",
                "ratios",
            ],
            "dataframe_objects": [
                "iloc",
                "iloc",
                "mean",
                "iloc",
                "iloc",
            ],
        }

        constraint_pe_ratio: float = 15
        constraint_roe: float = 0.07
        constraint_rsi: float = 45
        constraint_earnings_yield: float = 0.08
        constraint_peg_ratio: float = 1

        constraints = {
            "peRatio": {
                "df_name": "key_metrics",
                "value": constraint_pe_ratio,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 20,
            },
            "roe": {
                "df_name": "key_metrics",
                "value": constraint_roe,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 20,
            },
            "rsi": {
                "df_name": "rsi",
                "value": constraint_rsi,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 20,
            },
            "earningsYield": {
                "df_name": "key_metrics",
                "value": constraint_earnings_yield,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 20,
            },
            "priceEarningsToGrowthRatio": {
                "df_name": "ratios",
                "value": constraint_peg_ratio,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 20,
            },
        }

        return metrics, constraints

    @staticmethod
    def set_constraints_growth_stocks() -> tuple:
        """Function to set constraints for growth stocks"""

        metrics = {
            "screener": "growth",
            "variables": [
                "peRatio",
                "eps",
                "roic",
                "rsi",
                "priceEarningsToGrowthRatio",
                "piotroskiScore",
            ],
            "dataframes": [
                "key_metrics",
                "income_statement",
                "rsi",
                "ratios",
                "financial_score",
            ],
            "dataframe_list": [
                "key_metrics",
                "income_statement",
                "key_metrics",
                "rsi",
                "ratios",
                "financial_score",
            ],
            "dataframe_objects": [
                "iloc",
                "percentage_diff",
                "iloc",
                "mean",
                "iloc",
                "iloc",
            ],
        }

        constraint_pe_ratio: float = 20
        constraint_eps: float = 0.2
        constraint_roic: float = 0.1
        constraint_rsi: float = 60
        constraint_peg_ratio: float = 1.2
        constraint_piotroski_score: float = 6

        constraints = {
            "peRatio": {
                "df_name": "key_metrics",
                "value": constraint_pe_ratio,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 20,
            },
            "eps": {
                "df_name": "income_statement",
                "value": constraint_eps,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 30,
            },
            "roic": {
                "df_name": "key_metrics",
                "value": constraint_roic,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 20,
            },
            "rsi": {
                "df_name": "rsi",
                "value": constraint_rsi,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 10,
            },
            "priceEarningsToGrowthRatio": {
                "df_name": "income_statement",
                "value": constraint_peg_ratio,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 20,
            },
            "piotroskiScore": {
                "df_name": "financial_score",
                "value": constraint_piotroski_score,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 10,
            },
        }
        return metrics, constraints

    @staticmethod
    def set_constraints_magic_formula() -> tuple:
        """Function to set constraints using the magic formula"""

        metrics = {
            "screener": "magic_formula",
            "variables": [
                "peRatio",
                "earningsYield",
                "roic",
                "returnOnTangibleAssets",
                "debtToEquity",
            ],
            "dataframes": [
                "key_metrics",
                "key_metrics",
                "key_metrics",
                "key_metrics",
                "key_metrics",
            ],
            "dataframe_list": [
                "key_metrics",
                "key_metrics",
                "key_metrics",
                "key_metrics",
                "key_metrics",
            ],
            "dataframe_objects": [
                "iloc",
                "iloc",
                "iloc",
                "iloc",
                "iloc",
            ],
        }

        constraint_pe_ratio: float = 15
        constraint_earnings_yield: float = 0.06
        constraint_roic: float = 0.1
        constraint_return_on_tangible_assets: float = 0.15
        constraint_debt_to_equity_ratio: float = 0.01

        constraints = {
            "peRatio": {
                "df_name": "key_metrics",
                "value": constraint_pe_ratio,
                "comparator": "less_than",
                "actual_value": 0,
                "weight": 20,
            },
            "earningsYield": {
                "df_name": "key_metrics",
                "value": constraint_earnings_yield,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 30,
            },
            "roic": {
                "df_name": "key_metrics",
                "value": constraint_roic,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 20,
            },
            "returnOnTangibleAssets": {
                "df_name": "key_metrics",
                "value": constraint_return_on_tangible_assets,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 20,
            },
            "debtToEquity": {
                "df_name": "key_metrics",
                "value": constraint_debt_to_equity_ratio,
                "comparator": "greater_than",
                "actual_value": 0,
                "weight": 10,
            },
        }

        return metrics, constraints

        # @staticmethod

    # def set_constraints_buy_dip():
    #     """Function to set constraints for buy on the dip stocks"""
    #
    #     constraints = {
    #         "peRatio": {
    #             "df_name": "key_metrics",
    #             "value": 10,
    #             "comparator": "less_than",
    #             "actual_value": 0,
    #         },
    #         # price change over the last month
    #         "1M": {
    #             "df_name": "stock_price",
    #             "value": 80.0,
    #             "comparator": "less_than",
    #             "actual_value": 0,
    #         },
    #         # price change over the last year
    #         "1Y": {
    #             "df_name": "stock_price",
    #             "value": -50.0,
    #             "comparator": "greater_than",
    #             "actual_value": 0,
    #         },
    #         # average rsi
    #         "rsi": {
    #             "df_name": "rsi",
    #             "value": 80,
    #             "comparator": "less_than",
    #             "actual_value": 0,
    #         },
    #     }
    #
    #     return constraints
