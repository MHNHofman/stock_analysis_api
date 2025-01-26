# here we are creating stock screeners. Based on predefined constraints
# we can filter stocks that meet our criteria.

# pylint: disable=missing-docstring, line-too-long, too-many-locals


import asyncio
import logging
import pandas as pd
from src.data_handlers import Globals
from src.data_handlers import (
    DataFrameFunctions,
    GenericFunctions,
    DataProcessingFunctions,
)
from src.screener.stock_metrics_constraints import StockScreenerConstraints
from src.helper_features.result_processing_features import (
    ResultsProcessing,
    InsiderTrading,
)


logger = logging.getLogger(__name__)


class StockScreener(DataFrameFunctions):
    """Class to define the variables, dataframes and constraints for stock screening.
    screen the stocks based on the constraints"""

    def __init__(self, symbol: str, api_key: str):
        """Inherits classes and obtains collected data from the dataframes"""
        super().__init__(symbol)
        self.symbol: str = symbol
        self.api_key: str = api_key
        self.data: list = Globals.STOCK_DATAFRAMES
        self.constraints = StockScreenerConstraints()

    async def run_screeners(self):
        """Perform screening on stocks based on predefined constraints"""
        # create tasks for each analysis

        undervalued_analysis = asyncio.create_task(
            self.execute_screening(screener_type="undervalued")
        )

        growth_analysis = asyncio.create_task(
            self.execute_screening(screener_type="growth")
        )

        magic_formula_analysis = asyncio.create_task(
            self.execute_screening(screener_type="magic_formula")
        )

        await asyncio.gather(
            undervalued_analysis,
            # magic_formula_analysis,
            # growth_analysis
        )

    async def execute_screening(self, screener_type: str):
        """Execute the screening based on the constraints defined for the screener type
        :param screener_type: str
        """

        screener_metrics, screener_constraints = self.get_metrics_constraints(
            screener_type
        )

        if "dataframes" not in screener_metrics:
            logger.warning(
                "dataframes not in screener metrics for type %s", screener_type
            )
        df_list = self.fill_data_in_dataframes(
            dataframes=screener_metrics["dataframes"]
        )

        # if not all data is available, discontinue the analysis

        if df_list is False:
            return False
        actual_values = DataProcessingFunctions.set_actual_values(
            variables=screener_metrics["variables"],
            list_df=df_list,
            name_df=screener_metrics["dataframe_list"],
            value_type=screener_metrics["dataframe_objects"],
        )

        stock_evaluation = StockEvaluation(symbol=self.symbol, api_key=self.api_key)
        evaluation_value_constraint = await stock_evaluation.loop_trough_evaluations(
            constraints=screener_constraints,
            variables=screener_metrics["variables"],
            actual_values=actual_values,
            screener_type=screener_type,
        )

        if evaluation_value_constraint is True:
            logger.info(
                "Stock %s MEETS the criteria for screener type %s",
                self.symbol,
                screener_type,
            )
            await self.assign_transfer_dataframes(screener_type=screener_type)
        return evaluation_value_constraint

    def get_metrics_constraints(self, screener_type: str) -> tuple:
        """Get the metrics and constraints for the screener type"""

        screener_metrics: dict = {}
        screener_constraints: dict = {}

        if screener_type == "undervalued":
            screener_metrics, screener_constraints = (
                self.constraints.set_constraints_undervalued_stocks()
            )
        if screener_type == "growth":
            screener_metrics, screener_constraints = (
                self.constraints.set_constraints_growth_stocks()
            )
        if screener_type == "magic_formula":
            screener_metrics, screener_constraints = (
                self.constraints.set_constraints_magic_formula()
            )
        return screener_metrics, screener_constraints

    def fill_data_in_dataframes(self, dataframes: list) -> list | bool:
        """Fill the data in the dataframes for a particular share"""
        df_list = []
        for df_name in dataframes:
            df = self.get_df_metrics(data=self.data, df_name=df_name)
            df_list.append(df)
        check_dataframes = self.check_empty_dataframe(
            list_df=df_list, dataframes=dataframes
        )

        if check_dataframes is False:
            logger.warning(
                "Not all dataframes contain data for: %s - therefore no analysis possible",
                self.symbol,
            )
            return False
        return df_list


class StockEvaluation(DataFrameFunctions):
    """Evaluates stock based on predefined constraints"""

    def __init__(self, symbol: str, api_key: str):
        """Inherits the symbol from the parent class"""
        super().__init__(symbol)
        self.symbol: str = symbol
        self.api_key: str = api_key
        self.total_score: float = 0
        self.constraint_evaluations: list = []

    @staticmethod
    async def evaluate_values_versus_constraints(
            variable_value: float, constraint_value: float, constraint_comparator: str
    ) -> tuple:
        """Evaluate the variable value versus the set constraint
        :param variable_value: float value of the variable
        :param constraint_value: float value of the constraint to compare against
        :param constraint_comparator: str comparator to use for the evaluation
        :return: tuple with the comparison and the relative difference
        """
        comparison = []

        # calculate relative difference between the variable and the constraint

        relative_difference = ResultsProcessing.relative_difference(
            variable_value, constraint_value
        )

        if constraint_comparator == "less_than":
            comparison = ResultsProcessing.less_than(variable_value, constraint_value)
        if constraint_comparator == "greater_than":
            comparison = ResultsProcessing.greater_than(
                variable_value, constraint_value
            )
        if constraint_comparator == "equal_to":
            comparison = ResultsProcessing.equal_to(variable_value, constraint_value)
        return comparison, relative_difference

    async def loop_trough_evaluations(
            self,
            constraints: dict,
            variables: list,
            actual_values: dict,
            screener_type: str,
    ):
        """Loop through the constraints and evaluate the variables versus the constraints
        :param constraints: dict with the constraints
        :param variables: list with the variables
        :param actual_values: dict with the actual values of the variables
        :param screener_type: str with the screener type
        """

        # Create two empty dictionaries to add the results of the evaluation if the constraints are met

        new_row = {}
        evaluation_dict = {}

        # Create a new DataFrame to set the columns for the weighted scores

        df_weighed_scores = GenericFunctions.define_dataframe_weighted_scores(
            columns=variables,
            screener_type=screener_type,
        )

        for constraint_name, item in constraints.items():
            check_constraint = GenericFunctions.check_constraint_in_variables(
                constraint_name=constraint_name,
                variables=variables,
                value=actual_values[constraint_name],
            )

            # if the constraint is not in the variables, continue to the next constraint

            if check_constraint is False:
                continue
            outcome_evaluation = await self.value_vs_constraint_evaluation(
                item, actual_values, constraint_name
            )
            evaluation_dict.update(outcome_evaluation)
        # check if all constraints are met

        if all(self.constraint_evaluations):
            # Append the new row to the DataFrame

            new_row["symbol"] = self.symbol
            new_row["total_score"] = self.total_score
            # Append new_dict to existing_dict

            merged_dict = {
                key: value
                for d in (evaluation_dict, new_row)
                for key, value in d.items()
            }

            # Convert scalar values to lists

            scores_dict = {k: [v] for k, v in merged_dict.items()}

            # create an ordered dictionary with the new order of the columns and their values

            new_dict = ResultsProcessing.reorder_dict(
                new_order=df_weighed_scores.columns.tolist(), dict_to_update=scores_dict
            )

            # Convert OrderedDict to DataFrame

            df = pd.DataFrame(new_dict)

            # # when the dataframe for weighed scores is empty, append the new row to it rather than concat
            # if df_weighed_scores.shape[0] == 0:
            #     # df = df_weighed_scores.append(merged_df, ignore_index=True)
            #     # df = pd.concat([df_weighed_scores, merged_df], ignore_index=True)
            #     df = df_weighed_scores.loc[0] = [1, 2, 3]  # First row
            #
            # else:
            #
            #     # when the scores for evaluation of the stock are known, add them to the weighed scores for stocks
            #     if not merged_df.empty:
            #         # Concatenate DataFrames
            #         df = pd.concat([df_weighed_scores, merged_df], ignore_index=True)
            #
            #     else:
            #         df = df_weighed_scores

            df.attrs["name"] = df_weighed_scores.attrs["name"]

            # Write the DataFrame to the list of dataframes

            await DataProcessingFunctions.write_to_dataframe(
                data=df, df_name=df_weighed_scores.attrs["name"]
            )

            # Get insider trading for those stocks that meet the criteria

            insider_trading = InsiderTrading(symbol=self.symbol, api_key=self.api_key)
            await insider_trading.get_insider_trading(limit=1000)

            return True

        # When the constraints are not met, log the symbol
        logger.info(
            "Stock %s DOES NOT MEET the criteria for screener type %s",
            self.symbol,
            screener_type,
        )
        return False

    async def value_vs_constraint_evaluation(
            self, item, actual_values, constraint_name: str
    ) -> dict:
        """Evaluate the variable value versus the set constraint
        :param item: dict with the constraint details
        :param actual_values: dict with the actual values of the variables
        :param constraint_name: str with the name of the constraint
        :return: dict with the evaluation results
        """
        dict_constraint: dict = {}
        constraint_value = item["value"]
        constraint_comparator = item["comparator"]
        constraint_weight = item["weight"]

        evaluation_value_constraint = (
            await StockEvaluation.evaluate_values_versus_constraints(
                actual_values[constraint_name],
                constraint_value,
                constraint_comparator,
            )
        )

        value = evaluation_value_constraint[1]
        weight_value = value * (constraint_weight / 100)
        self.total_score += weight_value

        # add the constraint score and weight to the new row

        constraint_score_name = f"{constraint_name}_score"
        constraint_weight_name = f"{constraint_name}_weight"

        # add the constraint value and weight to the new row
        dict_constraint[constraint_score_name] = weight_value
        dict_constraint[constraint_weight_name] = constraint_weight

        self.constraint_evaluations.append(evaluation_value_constraint[0])
        return dict_constraint
