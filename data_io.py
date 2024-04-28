import json
import pandas as pd


def jsonl_to_df(file_path: str) -> pd.DataFrame:
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return pd.DataFrame(data)
