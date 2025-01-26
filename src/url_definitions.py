"""This module defines the URLs for the stock analysis API"""

#pylint: disable=too-few-public-methods, line-too-long

class StockAnalysisURLs:
    """Defines the URLs for the stock analysis API"""
    MainAnalysisURLs = [
        "https://financialmodelingprep.com/api/v3/income-statement/{}?period=annual&apikey={}",
        "https://financialmodelingprep.com/api/v3/ratios/{}?period=quarter&limit=20&apikey={}",
        "https://financialmodelingprep.com/api/v3/technical_indicator/1day/{}?type=rsi&period=20&apikey={}",
        "https://financialmodelingprep.com/api/v3/stock-price-change/{}?apikey={}",
        "https://financialmodelingprep.com/api/v3/key-metrics/{}?period=quarter&apikey={}",
        "https://financialmodelingprep.com/api/v3/grade/{}?limit=50&apikey={}",
        "https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/{}?apikey={}",
        "https://financialmodelingprep.com/api/v4/score?symbol={}&apikey={}"
    ]

    EarningsCalendarURLs = [
        "https://financialmodelingprep.com/api/v3/earning_calendar?from={}&to={}&apikey={}",
    ]
