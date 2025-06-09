import pandas as pd

def read_file(file_name: str) -> pd.DataFrame:
    """
    Returns a dataframe from given csv file

    :param file_name: Name or path to csv file
    :return: The data frame object
    """
    df = pd.read_csv(file_name)
    return df