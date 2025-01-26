"""Main CLI module for the stock analysis tool"""

import logging
from rich.console import Console
from rich.theme import Theme
from src.data_handlers import Globals
from stock_main_run import start_main_run

logger = logging.getLogger(__name__)

custom_theme = Theme({"info": "bold cyan", "warning": "magenta", "danger": "bold red"})

console = Console(theme=custom_theme, color_system="truecolor")

# pylint: disable=line-too-long, too-few-public-methods, unused-argument, consider-using-with


class RichText:
    """Sets the rich color scheme"""

    CONSOLE_TEXT_TAG_START = "[bold yellow]"
    CONSOLE_TEXT_TAG_END = "[/bold yellow]"
    CONSOLE_VALUE_TAG_START = "[bold blue3]"
    CONSOLE_VALUE_TAG_END = "[/bold blue3]"
    CONSOLE_EXIT_SESSION_TAG_START = "[blue_violet]"
    CONSOLE_EXIT_SESSION_TAG_END = "[/blue_violet]"
    CONSOLE_WARNING_TAG_START = "[bold red3]"
    CONSOLE_WARNING_TAG_END = "[/bold red3]"


class CLIFunctions:
    """collections of functions required for the CLI"""

    @classmethod
    def set_options(cls, options: dict, added_option: str) -> dict:
        """Sets current options and optional additional options, such as exit
        Arguments:
        options: the list of options that are derived from a query or function
        added_option: additional options, for example the option to exit the program
        """
        if added_option:
            key = list(options)[-1] + 1
            options.update({key: added_option})
        return options

    @classmethod
    def get_stock_symbol(cls, number_of_stocks: int) -> str | list:
        """Sets the stock symbol or multiple stock symbols"""
        symbol_list = []

        for x in range(1, number_of_stocks + 1):
            prompt = console.input(
                f"{RichText.CONSOLE_TEXT_TAG_START}"
                f"Please enter the stock symbol or name for stock number {x}:"
                f"{RichText.CONSOLE_TEXT_TAG_END}\n"
            )
            symbol_list.append(prompt)
        return symbol_list

    @classmethod
    def get_number_of_stocks(cls) -> int:
        """Sets and returns the chosen environment"""
        allowed_number = 25
        while True:
            try:
                prompt = console.input(
                    prompt=f"{RichText.CONSOLE_TEXT_TAG_START}"
                           f"How many stocks would you like to analyze? Please choose a number below {allowed_number}"
                           f"{RichText.CONSOLE_TEXT_TAG_END}\n"
                )

                value = int(prompt)
                if value < allowed_number:
                    print(f"Your entered value {value} which is valid.")
                    break  # Exit the loop when the condition is met

                print(
                    f"Value {value} is not within the range of 0 to 25, please try again."
                )
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        return int(value)


def cli_main():
    """Main function for the CLI"""
    from src.cli.cli_functions import cli_check_and_get_symbols # pylint: disable=import-outside-toplevel

    console.print("Simple Stock CLI", style="info")
    print("----------------------")
    # Clear the log file before the process starts

    open("cli_stock_api_log.log", "w", encoding="utf-8").close()
    logging.basicConfig(
        filename="cli_stock_api_log.log",
        format="%(levelname)s - %(asctime)s - %(message)s",
        level=logging.INFO,
        force=True,
    )
    logger.info("Start with stock analysis run")
    cli = CLIFunctions()
    number_of_stocks = cli.get_number_of_stocks()
    entered_symbols = cli.get_stock_symbol(number_of_stocks)
    check_symbols = cli_check_and_get_symbols(entered_symbols)
    Globals.STOCK_LIST = check_symbols
    Globals.ANALYSIS_TYPE = "cli"
    start_main_run()
    print("operation complete")


if __name__ == "__main__":
    cli_main()
