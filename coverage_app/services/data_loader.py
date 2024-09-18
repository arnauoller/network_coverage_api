import os
import pandas as pd


def load_coverage_data_csv():
    data_file = os.path.join("data", "preprocessed_coverage_data.csv")
    return pd.read_csv(data_file)
