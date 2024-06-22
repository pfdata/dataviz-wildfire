import common_paths
import sys

from typing import List
import pandas as pd
from pandas import DataFrame
import re


class WildFire:
    """Description of the wild fire"""

    def __init__(self) -> None:
        self.table_description = {
            "1B": "Forest fire areas by stand type",
            "2B": "Causes",
            "5B": "Forest fires in the individual months of the calendar year - number",
            "6B": "Forest fires in the individual months of the calendar year - area",
        }

    def get_all_csv(self, table_name) -> List:
        """"""
        if table_name in self.table_description.keys():
            pathlist = [
                str(file) for file in common_paths.BMEL.rglob(f"*{table_name}.csv")
            ]
            pathlist.sort()
            if len(pathlist) == 0:
                sys.exit(f"Could not any *{table_name}.csv file at {common_paths.BMEL}")
            return pathlist
        else:
            sys.exit(
                f"Table name not mapped. Is must be one of: {self.table_description.keys()}"
            )

    def merge_csv_to_dfs(self, csv_list: List) -> DataFrame:
        """"""
        df_list = []
        for path in csv_list:
            year = re.search(r"\d{4}", path)[0]
            df_ffa = pd.read_csv(path, index_col=0)
            df_ffa["Year"] = year
            df_list.append(df_ffa)

        return pd.concat(df_list)

    def get_all_ffa(self) -> DataFrame:
        return self.merge_csv_to_dfs(self.get_all_csv("1B"))

    def get_all_causes(self) -> DataFrame:
        return self.merge_csv_to_dfs(self.get_all_csv("2B"))

    def get_montly_numbers(self) -> DataFrame:
        return self.merge_csv_to_dfs(self.get_all_csv("5B"))

    def get_monthly_area(self) -> DataFrame:
        return self.merge_csv_to_dfs(self.get_all_csv("6B"))

    def get_monthly_data(self) -> DataFrame:

        df_5B = self.get_montly_numbers()
        df_6B = self.get_monthly_area()

        # Merge the data frames on the 'Land' column
        merged_df = pd.merge(
            df_5B, df_6B, on=["Land", "Year"], suffixes=("_number", "_area")
        )

        return merged_df
