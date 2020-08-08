from typing import List
import pandas as pd


def optimize_floats(df: pd.DataFrame) -> pd.DataFrame:
    """Downcast floats to optimize memory usage

    :param df: pandas DataFrame
    :return: pandas DataFrame with optimized floats
    """
    floats = df.select_dtypes(include=["float64"]).columns.tolist()
    df[floats] = df[floats].apply(pd.to_numeric, downcast="float")
    return df


def optimize_ints(df: pd.DataFrame) -> pd.DataFrame:
    """Downcast integers to optimize memory usage

    :param df: pandas DataFrame
    :return: pandas DataFrame with optimized integers
    """
    ints = df.select_dtypes(include=["int64"]).columns.tolist()
    df[ints] = df[ints].apply(pd.to_numeric, downcast="integer")
    return df


def optimize_objects(df: pd.DataFrame, exclude: List[str]) -> pd.DataFrame:
    """Downcast objects to optimize memory usage

    :param df: pandas DataFrame
    :param exclude: features which are datetime instead of object
    :return: pandas DataFrame with optimized objects
    """
    for col in df.select_dtypes(include=["object"]):
        if col not in exclude:
            num_unique_values = len(df[col].unique())
            num_total_values = len(df[col])
            if float(num_unique_values) / num_total_values < 0.5:
                df.loc[:, col] = df[col].astype("category")
    return df


def optimize_all(df: pd.DataFrame, exclude: List[str] = None):
    """Combine optimize_floats, optimize_ints, optimize_objects to optimize the dataframe

    :param df: pandas dataframe
    :param exclude: features which are datetime
    :return: pandas DataFrame optimized for all types
    """
    if not exclude:
        exclude = []

    return df.pipe(optimize_floats).pipe(optimize_ints).pipe(optimize_objects, exclude)