# # pylint: disable=missing-docstring, too-few-public-methods
#
# from typing import List
# from pydantic import BaseModel, ValidationError, validator
#
#
# class ApiHandling(BaseModel):
#     """Write data to dataframe
#
#     Parameters:
#             BaseModel
#     """
#
#     api_key: str
#     tradeslist: List[int] = []
#     trade: str
#
#     @validator("trade")
#     def check_length_symbol(self, symbol: str):
#         """Checks whether the symbol is not too long"""
#         if len(symbol) > 20:
#             raise ValidationError(f"this symbol is too long: {symbol}")
#         return symbol


from pandantic import BaseModel
# from pydantic import ValidationError, field_validator
from pydantic.types import StrictInt

class DataFrameSchema(BaseModel):
    """Example schema for testing."""

    example_str: str
    example_int: StrictInt


def is_convertible_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
