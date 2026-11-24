import pandas as pd

data = pd.read_csv(
    "dataset.csv",
    encoding="latin1"
)

print(data.columns.tolist())