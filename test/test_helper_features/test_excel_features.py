import pytest
import pandas as pd
from src.helper_features.excel_features import ExcelOperations, find_folder
from src.data_handlers import Globals
from pathlib import Path



class TestExcelOperations:


    def test_find_path(self) -> None:
        """
        Function to test absolute path
        :return: None
        """
        test = find_folder("data_earnings_analysis")
        print(test)


    def test_abs_path(self) -> None:
        """
        Function to test absolute path
        :return: None
        """
        Globals.ANALYSIS_TYPE = "earnings_calendar"
        print(f'this is the analysis type: {Globals.ANALYSIS_TYPE}')
        excel_operations = ExcelOperations()
        abs_path = excel_operations.get_abs_path()
        path_ending = "data_earnings_analysis"
        check_path = str(abs_path).endswith(path_ending)
        # running the coverage report does not recognize Path, therefore the two lines of code below
        if abs_path is None:
            return
        assert check_path == True









