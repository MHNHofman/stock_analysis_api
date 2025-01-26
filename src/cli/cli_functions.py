"""This module contains the functions that are used in the CLI for the stock selection process"""

import fmpsdk
from rich.console import Console
from src.helper_features.api_features import SyncAPIFunctions
from src.cli.cli_main import RichText

# pylint: disable=line-too-long


console = Console(style=None)


def run_stock_list(list_symbols: list):
    """Function to run the stock list and informs which stocks are available for selection"""
    question_prompt = []
    for item in list_symbols:
        question_prompt.append(
            f"{item['index']}: Symbol with name {RichText.CONSOLE_VALUE_TAG_START}{item['name']}{RichText.CONSOLE_VALUE_TAG_END}, symbol {RichText.CONSOLE_VALUE_TAG_START}{item['symbol']}{RichText.CONSOLE_VALUE_TAG_END} active on exchange {RichText.CONSOLE_VALUE_TAG_START}{item['exchange']}{RichText.CONSOLE_VALUE_TAG_END} \n"
        )
    # Concatenating strings using join

    result = " ".join(question_prompt)
    return result


def cli_check_and_get_symbols(list_symbols) -> list:
    """Function to check whether a symbol is valid"""

    api_key = SyncAPIFunctions.sync_load_api_keys()
    chosen_symbols = []

    for _, symbol in enumerate(list_symbols):
        console.print(
            f"Checking symbol: {RichText.CONSOLE_VALUE_TAG_START}{symbol}{RichText.CONSOLE_VALUE_TAG_END}"
        )

        search_result = fmpsdk.search(apikey=api_key, query=symbol)

        # if multiple options for the search request were found, choose the correct one

        if len(search_result) > 1:
            share = choose_share(search_result=search_result, symbol=symbol)
            if share:
                chosen_symbols.append(share)
        else:
            chosen_symbols.append(symbol)
    return chosen_symbols


def get_symbol_from_list(number_of_options: int) -> int:
    """Choose the correct symbol from the list of available symbols"""
    while True:
        try:
            prompt = console.input(
                prompt=f"Please choose the correct one by entering a number between 0 and {(number_of_options - 1)}"
            )
            value = int(prompt)
            if value <= (number_of_options - 1):
                print(f"Great! Your entry {value} is valid.")
                break  # Exit the loop when the condition is met
            print(
                f"{value} is not within the range of 0 to {(number_of_options - 1)}, please try again."
            )
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return value


def choose_share(search_result: list, symbol: str):
    """Obtain the choosen symbol from the search result"""
    stock_entry = []

    for index, item in enumerate(search_result):

        stock_info = {}
        stock_info["index"] = index
        stock_info["name"] = item["name"]
        stock_info["symbol"] = item["symbol"]
        stock_info["exchange"] = item["stockExchange"]
        stock_entry.append(stock_info)
    list_options = run_stock_list(list_symbols=stock_entry)

    console.print(
        f"We found multiple stocks for symbol {RichText.CONSOLE_VALUE_TAG_START}{symbol}{RichText.CONSOLE_VALUE_TAG_END}\n"
        f"{list_options}"
    )

    symbol_check = get_symbol_from_list(number_of_options=len(search_result))
    return stock_entry[int(symbol_check)]["symbol"]
