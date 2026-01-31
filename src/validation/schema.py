import pandas as pd

def inspect_schema(df: pd.DataFrame) -> dict:
    """
    Inspect structural metadata of a DataFrame.
    Does NOT modify data.
    """

    column_details = {}

    for col in df.columns:
        column_details[col] = {
            "dtype": str(df[col].dtype),
            "non_null_count": int(df[col].notnull().sum()),
            "null_count": int(df[col].isnull().sum()),
            "unique_values": int(df[col].nunique(dropna=False))
        }

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_usage_kb": round(df.memory_usage(deep=True).sum() / 1024, 2),
        "columns_detail": column_details
    }
