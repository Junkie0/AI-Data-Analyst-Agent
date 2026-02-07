import pandas as pd


def high_missing_columns(df: pd.DataFrame, threshold: float = 0.5) -> dict:
    """
    Identify columns with missing value ratio above a given threshold.
    Default threshold = 50%.
    """

    missing_ratio = df.isnull().mean()

    flagged = {
        col: round(ratio, 3)
        for col, ratio in missing_ratio.items()
        if ratio > threshold
    }

    return {
        "threshold": threshold,
        "flagged_columns": flagged
    }


def constant_columns(df: pd.DataFrame) -> dict:
    """
    Identify columns that contain only a single unique value.
    """

    constants = [
        col for col in df.columns
        if df[col].nunique(dropna=False) == 1
    ]

    return {
        "constant_columns": constants
    }


def id_like_columns(df: pd.DataFrame, threshold: float = 0.9) -> dict:
    """
    Identify columns where the ratio of unique values to total rows
    is higher than the given threshold.
    """

    total_rows = len(df)
    id_like = {}

    for col in df.columns:
        unique_ratio = df[col].nunique(dropna=False) / total_rows

        if unique_ratio >= threshold:
            id_like[col] = round(unique_ratio, 3)

    return {
        "threshold": threshold,
        "id_like_columns": id_like
    }


def string_date_columns(df: pd.DataFrame) -> dict:
    """
    Identify columns that are likely dates but stored as strings.
    """

    potential_dates = []

    for col in df.columns:
        if df[col].dtype == "object":
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                non_null_ratio = parsed.notnull().mean()

                if non_null_ratio > 0.8:
                    potential_dates.append(col)
            except Exception:
                continue

    return {
        "string_date_columns": potential_dates
    }