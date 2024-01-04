#  Copyright (c) 2024.  @Author: Aashish Mahajan
#
import pandas as pd


def calculate_mean_and_standard_deviation(data):
    """Calculates the mean and standard deviation of a numerical column."""
    try:
        df = pd.DataFrame(data)
        mean = df.mean(axis=0)
        std = df.std(axis=0)
        return mean, std
    except Exception as e:
        raise ValueError("Invalid input data") from e


def filter_by_condition(df, column_name, condition):
    """Filters a DataFrame based on a condition on a column."""

    return df[df[column_name] > condition]
