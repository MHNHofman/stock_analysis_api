"""Common calculations for the helper features."""

from datetime import datetime
from dateutil import parser
from src.data_handlers import Globals


def get_day_difference(target_date_str: str) -> int:
    """Calculate the difference in days between today and a target date.
    :param target_date_str: The target date in string format.
    :return: The difference in days between today and the target date.
    """
    # Get today's date
    today = datetime.now().date()
    # Parse the target date from a string
    target_date = parser.parse(target_date_str).date()
    # Calculate the difference
    difference = today - target_date
    return difference.days


def get_analysis_type(predefined_symbols: list | None) -> str:
    """Calculate the difference in days between today and a target date.
    :param predefined_symbols: If present, the shares that have been collected in an earlier step.
    :return: The type of stock analysis to be conducted.
    """
    if len(Globals.STOCK_LIST) == 0 and predefined_symbols is None:
        analysis_type = "full"
    elif predefined_symbols is not None:
        analysis_type = "earnings_calendar"
    else:
        analysis_type = "cli"
    return analysis_type
