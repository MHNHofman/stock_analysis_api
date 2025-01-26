from rich.theme import Theme
from rich.console import Console
from src.cli.cli_main import RichText
from datetime import datetime

custom_theme = Theme({"info": "bold cyan", "warning": "magenta", "danger": "bold red"})
console = Console(theme=custom_theme, color_system="truecolor")


class CLIPracticeFunctions:
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
    def check_data_type(cls, user_input) -> str:
        """checks whether input is of the correct data type
        Arguments:
        user_input: the input given by the user
        """

        if user_input.isdigit():
            return "int"
        return "str"

    @classmethod
    def get_number_of_visitors(cls) -> str:
        """Sets number of visitors"""
        # user_input = input("How many visitors are you expecting?")
        user_input = input("How many family members are you expecting?")

        if user_input.isdigit():
            return user_input
        print(
            "Hmmm, that doesn't look correct, as you did not entered a number. Please try again."
        )
        return (
            CLIPracticeFunctions.get_number_of_visitors()
        )  # Recursively call the function again

    @classmethod
    def get_name(cls):
        user_input = input("Could you please enter your name: ")

        if user_input.isdigit():
            print(
                "Hmmm, that doesn't look like you entered your name, as you entered a number. Please try again."
            )
            return (
                CLIPracticeFunctions.get_name()
            )  # Recursively call the function again
        return user_input

    @classmethod
    def get_visitor_names(cls, number_of_visitors: str) -> str | list:
        """Sets the names of the visitors"""
        visitor_list = []

        for x in range(1, int(number_of_visitors) + 1):
            prompt = console.input(
                f"{RichText.CONSOLE_TEXT_TAG_START}"
                # f"Please enter the name for visitor {x}:"
                f"Please enter the name of the family member {x}:"
                f"{RichText.CONSOLE_TEXT_TAG_END}\n"
            )
            visitor_list.append(prompt)
        if number_of_visitors == "1":
            return str(visitor_list[0])
        comma_separated_list = ",".join(map(str, visitor_list[:-1]))
        all_names = comma_separated_list + " and " + visitor_list[-1]
        return all_names

    @classmethod
    def get_arrival_date(cls, visitors):
        user_input_year = input(f"In which year are you expecting the wedding to take place?")

        if user_input_year.isdigit():
            year = int(user_input_year)
        else:
            print(
                "Hmmm, that doesn't look like you entered a number. Please try again."
            )
            return (
                CLIPracticeFunctions.get_arrival_date()
            )  # Recursively call the function again
        user_input_month = input(
            "In which month would that be? Please use the month number, which is inbetween 1 and 12"
        )

        if user_input_year.isdigit():
            month = int(user_input_month)
        else:
            print(
                "Hmmm, that doesn't look like you entered a number. Let's start again."
            )
            return (
                CLIPracticeFunctions.get_arrival_date()
            )  # Recursively call the function again
        user_input_day = input(
            f"On which day would that be? Please use the number of that day, somewhere in between 1 and 31"
        )

        if user_input_day.isdigit():
            day = int(user_input_day)
        else:
            print(
                "Hmmm, that doesn't look like you entered a number. Let's start again."
            )
            return (
                CLIPracticeFunctions.get_arrival_date()
            )  # Recursively call the function again
        return [year, month, day]

    @classmethod
    def get_time_diff(cls, arrival_date: list):
        """Calculates the time difference between the current date and the arrival date"""
        print(arrival_date)
        # Set the specific date (e.g., January 1, 2025)

        set_date = datetime(arrival_date[0], arrival_date[1], arrival_date[2])

        # Get the current date and time

        now = datetime.now()

        # Calculate the difference in days

        difference = (set_date - now).days + 1
        return difference


def cli_practice_main():
    """Main function for the CLI"""
    console.print("Hi there, let's get started!", style="info")
    print("----------------------")
    cli = CLIPracticeFunctions()
    name = cli.get_name()
    console.print(
        # f"Hello {name}, I heard you are expecting some visitors soon! Let's find out how long we have to wait for this great moment!",
        f"Hello {name}, I heard you are planning a wedding party in China! Let's find out how long we have to wait for this great moment!",
        style="info",
    )
    number_visitors = cli.get_number_of_visitors()
    console.print(
        # f"Alright {name}, you are expecting {number_visitors} visitors, let's see who!", style="info",
        f"Alright {name}, you are expecting {number_visitors} family members joining the wedding, let's see who!", style="info",
    )
    visitors_names = cli.get_visitor_names(number_of_visitors=number_visitors)
    console.print(
        f"That's exciting {name}, you must be thrilled with your loved ones {visitors_names} being there!!!",
        style="info",
    )
    console.print(f"Let's have a look at the wedding date!", style="info")
    arrival_date = cli.get_arrival_date(visitors=visitors_names)
    time_diff_days = cli.get_time_diff(arrival_date)
    time_diff_hours = time_diff_days * 60
    time_diff_minutes = time_diff_hours * 60

    console.print(f"Great, let's see the results", style="info")
    console.print(
        f"In {time_diff_days} days, you will enjoy your wedding with {visitors_names} by your side!",
        style="info",
    )
    console.print(
        f"That's equivalent to {time_diff_hours} hours or {time_diff_minutes} minutes from now!",
        style="info",
    )
    console.print(
        f"Well {name}, I hope you all have a great time together!", style="info"
    )


if __name__ == "__main__":
    cli_practice_main()

    # @classmethod
    # def get_ones_name(cls) -> str:
    #     """Sets name"""
    #     prompt = console.input(
    #         f"{RichText.CONSOLE_TEXT_TAG_START}"
    #         "Could you please enter your name:"
    #         f"{RichText.CONSOLE_TEXT_TAG_END}\n"
    #     )
    #
    #     console.print(prompt)
    #     name = CLIPracticeFunctions.handle_name_input(
    #         prompt=prompt, data_type_input="str"
    #     )
    #     return name

    # @classmethod
    # def handle_name_input(cls, prompt: str, data_type_input: str):
    #     """Operator to process the input from a click prompt
    #     Arguments:
    #     prompt: the prompt for the particular click command
    #     data_type_input: defines which type of input is expected
    #     """
    #     prompt = prompt.strip()
    #
    #     data_type_name = ""
    #
    #     if data_type_input == "int":
    #         data_type_name = "integer"
    #     if data_type_input == "str":
    #         data_type_name = "string"
    #     if len(prompt) < 1:
    #         console.print(
    #             f"{RichText.CONSOLE_WARNING_TAG_START} You didn't enter any name, please try again"
    #             f"{RichText.CONSOLE_WARNING_TAG_END}"
    #         )
    #         CLIPracticeFunctions.get_ones_name()
    #     check_data_type = CLIPracticeFunctions.check_data_type(user_input=prompt)
    #     console.print(f"type of input {check_data_type}")
    #
    #     if check_data_type != data_type_input:
    #         console.print(
    #             f"{RichText.CONSOLE_WARNING_TAG_START}Sorry, you entered the wrong data type. Please enter a valid {data_type_name}:"
    #             f"{RichText.CONSOLE_WARNING_TAG_END}"
    #         )
    #
    #         CLIPracticeFunctions.get_ones_name()
    #     return prompt

    # @classmethod
    # def handle_number_of_visitors_input(
    #         cls, prompt: str, data_type_input: str
    # ):
    #     """Operator to process the input from a click prompt for number of visitors
    #     Arguments:
    #     prompt: the prompt for the particular click command
    #     data_type_input: defines which type of input is expected
    #     """
    #     prompt = prompt.strip()
    #     data_type_name = ''
    #
    #     if data_type_input == 'int':
    #         data_type_name = 'integer'
    #
    #     if data_type_input == 'str':
    #         data_type_name = 'string'
    #
    #     if len(prompt) < 1:
    #         console.print(
    #             f"{RichText.CONSOLE_WARNING_TAG_START} You didn't enter any number, please try again"
    #             f"{RichText.CONSOLE_WARNING_TAG_END}"
    #         )
    #         CLIPracticeFunctions.get_number_of_visitors()
    #
    #     check_data_type = CLIPracticeFunctions.check_data_type(user_input=prompt)
    #
    #     if check_data_type != data_type_input:
    #         console.print(
    #             f"{RichText.CONSOLE_WARNING_TAG_START}Sorry, you entered the wrong data type. Please enter a valid {data_type_name}:"
    #             f"{RichText.CONSOLE_WARNING_TAG_END}"
    #         )
    #
    #         CLIPracticeFunctions.get_number_of_visitors()
    #
    #     return prompt
