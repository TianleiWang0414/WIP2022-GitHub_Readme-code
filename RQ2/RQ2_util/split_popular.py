import pandas as pd


def get_popular(data: pd.DataFrame) -> pd.DataFrame:
    return data.loc[data['star'] != 0]


def get_non_popular(data: pd.DataFrame) -> pd.DataFrame:
    return data.loc[data['star'] == 0]
