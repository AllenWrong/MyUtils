from typing import List, Union


def _info_check_meta(df, cols: Union[List, str], _fn, *args, **kwargs):
    if isinstance(cols, list):
        for col in cols:
            _fn(df, col, *args, **kwargs)
    elif isinstance(cols, str):
        _fn(df, cols, *args, **kwargs)
    else:
        raise ValueError(f'Unsupported cols type {type(cols)}')
        

def nan_info(df, cols: Union[List, str]):
    """Check nan ratio in pandas DataFrame"""
    def _fn(df, col):
        print(f'- nan ratio in {col}:', df[col].isna().mean())
    _info_check_meta(df, cols, _fn)


def substr_info(df, cols: Union[List, str], substr:str):
    """Check specific str ratio in pandas DataFrame"""
    def _fn(df, col, substr):
        print(f'- {substr} ratio in {col}:', (df[col] == substr).mean())
    _info_check_meta(df, cols, _fn, substr=substr)

