# Parent class (superclass)
import pathlib
import pandas as pd
import requests
import xml.etree.ElementTree as ET

from pandantic import BaseModel
from pydantic import ValidationError, field_validator
from pydantic.types import StrictInt


# pylint: skip-file
from pathlib import Path
import openpyxl
import pandas as pd


def get_excel():

    print('ok')

    current_path = Path.cwd()
    path_ending = "api_stock_from_scratch"
    absolute_path = None

    for file_path in current_path.iterdir():
        # print(file_path)
        if 'dbir' in file_path.name:
            print(file_path)
            # book = openpyxl.load_workbook(file_path)
            # sheet = book["Opties"]  # Replace "Sheet1" with your sheet name
            #
            # # Specify the column to loop through (e.g., column "A")
            # for row in sheet.iter_rows(min_col=1, max_col=1, values_only=True):
            #     value = row[0]  # Extract the cell value
            #     print(value)

            # Load the Excel file into a DataFrame
            df = pd.read_excel(file_path, sheet_name="Opties")  # Replace "Sheet1" with your sheet name
            concept = []
            # Loop through a specific column (e.g., "Column1")
            for index, value in enumerate(df["VARIABELE"]):
                values = {}
                print(value)
                if value == "surgbignumber":
                    print("found it")
                    code = df["WAARDE"].iloc[index]
                    text = df["LABEL"].iloc[index]
                    values["code"] = code
                    values["display"] = text

                    concept.append(values)

            print('ok')




class DataFrameSchema(BaseModel):
    """Example schema for testing."""

    example_str: str
    example_int: StrictInt

    @classmethod
    @field_validator("example_int")
    def validate_even_integer(
            cls, x: int
    ) -> int:
        """Example custom validator to validate if int is even."""
        if x % 2 != 0:
            raise ValidationError(f"example_int must be even, is {x}.")
        return x

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} is speaking"


# Child class (subclass) inheriting from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        # Call the __init__() method of the parent class using super()
        super().__init__(name)
        # Initialize additional attribute specific to Dog
        self.breed = breed


# Recursively loop through files in the folder
def get_files(folder):
    for path_to_file in folder.iterdir():
        if path_to_file.is_file():
            yield path_to_file
        elif path_to_file.is_dir():
            yield from get_files(path_to_file)


def loop_through_files():
    # Specify the path to the folder
    folder_path = pathlib.Path(__file__).parent
    # Use generator to loop through files
    for file_path in get_files(folder_path):
        # Do something with the file
        print(file_path)

def make_request(url):
    with requests.Session() as session:
        response = session.get(url)
        print(response.status_code)
        return response.status_code


def do_session_get():
    session = requests.session()
    response = session.get("foo")
    return session.get("foo")



def convert_xml_to_json(path: str):

    tree = ET.parse(path)
    root = tree.getroot()
    d = {}
    for child in root:
        if child.tag not in d:
            d[child.tag] = []
        dic = {}
        for child2 in child:
            if child2.tag not in dic:
                dic[child2.tag] = child2.text
        d[child.tag].append(dic)
    print(d)

def process_chunk(chunk):
    # Perform operations on each chunk
    pass

def process_large_dataset():
    chunk_size = 1000
    reader = pd.read_csv('large_dataset.csv', chunksize=chunk_size)
    for chunk in reader:
        process_chunk(chunk)


def fetch_data():
    # Imagine this function fetches data from an external source
    return {"key": "value"}

def process_data():
    data = fetch_data()
    # Process the data somehow
    processed_data = {"processed_key": data["key"].upper()}
    return processed_data

from rich.console import Console
from rich.theme import Theme


def run_print():
    from colorama import init, Fore, Style

    # Initialize colorama
    init()


    custom_theme = Theme({
        "info": "dim cyan",
        "warning": "magenta",
        "danger": "bold red"
    })
    console = Console(theme=custom_theme)
    console.print("This is information", style="info")
    console.print("[warning]The pod bay doors are locked[/warning]")
    console.print("Something terrible happened!", style="danger")
    print(Fore.RED + 'some red text')
    print(Style.RESET_ALL)




# @classmethod
# def convert_list_to_dict_with_index(cls, list_to_dict: list) -> dict:
#     """
#     Converts a given list to a dict with the list index indexes as the keys
#     """
#     set_dict = {k: v for v, k in enumerate(list_to_dict)}
#     inverted_dict = {v: k for k, v in set_dict.items()}
#
#     return inverted_dict



# @classmethod
# def ask_correct_symbol(cls, stock_list: list) -> list:
#     """Sets the stock symbol or multiple stock symbols"""
#     correct_symbol_list = []
#
#     for _, stock in enumerate(stock_list):
#         prompt = console.input(
#             f"{RichText.CONSOLE_TEXT_TAG_START}"
#             f"We found multiple stocks for symbol {stock}: please choose the correct one by entering the number:"
#             f"{RichText.CONSOLE_TEXT_TAG_END}\n"
#         )
#
#         console.print(prompt)
#         correct_symbol_list.append(prompt)
#     return correct_symbol_list


# @classmethod
# def handle_input(
#         cls, prompt: str, options: Optional[dict], is_dict: bool, multiple_choice: bool
# ):
#     """Operator to process the input from a click prompt
#     Arguments:
#     prompt: the prompt for the particular click command
#     options: the options given
#     is_dict: defines whether the list of options is a dictionary or a list
#     multiple_choice: defines whether the user can select multiple options
#     """
#     prompt = prompt.strip()
#     if len(prompt) < 1:
#         console.print(
#             f"{RichText.CONSOLE_WARNING_TAG_START}No input given, please retry:"
#             f"{RichText.CONSOLE_WARNING_TAG_END}"
#         )
#         return "Empty"
#
#     return prompt


# @classmethod
# def handle_input(
#         cls, prompt: str, options: Optional[dict], is_dict: bool, multiple_choice: bool
# ) -> str:
#     """Operator to process the input from a click prompt
#     Arguments:
#     prompt: the prompt for the particular click command
#     options: the options given
#     is_dict: defines whether the list of options is a dictionary or a list
#     multiple_choice: defines whether the user can select multiple options
#     """
#     try:
#         int(prompt)
#         return prompt
#     except ValueError:
#         print("Invalid input. Please enter a valid integer.")
#         CLIFunctions.get_number_of_stocks()


# dataframe_names = GenericFunctions.set_dataframe_names()

# # loop through the symbols and make the requests listed in the urls
# for symbol, name in symbol_list:
#     number_of_requests += 1
#     modified_urls = [u.format(symbol, api_key) for u in urls]
#     tasks = [
#         asyncio.ensure_future(AsyncAPIFunctions.fetch_url(session, url, symbol)) for url in modified_urls
#     ]
#
#     responses = await asyncio.gather(*tasks)
#     logger.info("Stock %s will be analyzed", symbol)
#
#     # if the responses are empty, continue to the next symbol
#     if responses == "" or responses is None:
#         logger.warning("Stock has no response: %s", symbol)
#         continue
#
#     # check if the responses are empty, excluding the grades and recommendations given by analysts
#     insufficient_data = GenericFunctions.check_empty_lists(responses[0:4])
#     # if the symbol does not return any data from the executed urls, print a warning and continue to the next symbol
#     if insufficient_data is True:
#         logger.warning("Symbol %s contains insufficient data", symbol)
#         continue
#
#     # handle the responses and write the data to the global dataframes
#     requests = await ResultsProcessing.handle_process_responses(
#         responses=responses,
#         dataframe_names=dataframe_names,
#         symbol=symbol,
#         name=name,
#     )
#     number_of_requests += requests
#     stock_screener = StockScreener(symbol=symbol)
#     # run the stock screeners set in the stock_metrics_constrains.py file
#     await stock_screener.run_screeners()
#     # clear the dataframes for the stock after the stock screener has run
#     Globals.STOCK_DATAFRAMES.clear()