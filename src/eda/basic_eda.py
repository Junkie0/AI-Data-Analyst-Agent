import pandas as pd


def split_column_types(df: pd.DataFrame) -> dict:
    """
    Split DataFrame columns into numerical and categorical groups.
    """

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

    return {
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns
    }


def numeric_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for numeric columns.
    """

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.empty:
        return {"numeric_summary": {}}

    summary = numeric_df.describe().T
    summary["missing_ratio"] = numeric_df.isnull().mean()

    return {
        "numeric_summary": summary.round(3).to_dict(orient="index")
    }


def categorical_summary(df: pd.DataFrame, top_n: int = 5) -> dict:
    """
    Generate summary statistics for categorical columns.
    """

    categorical_df = df.select_dtypes(exclude=["number"])

    summary = {}

    for col in categorical_df.columns:
        value_counts = categorical_df[col].value_counts(dropna=False)

        summary[col] = {
            "unique_values": int(categorical_df[col].nunique(dropna=False)),
            "top_values": value_counts.head(top_n).to_dict(),
            "missing_ratio": round(categorical_df[col].isnull().mean(), 3)
        }

    return {
        "categorical_summary": summary
    }
def cardinality_report(df: pd.DataFrame, high_cardinality_threshold: float = 0.5) -> dict:
    """
    Report unique value counts and ratios for each column.
    Flags high-cardinality columns based on a ratio threshold.
    """

    total_rows = len(df)
    report = {}

    for col in df.columns:
        unique_count = df[col].nunique(dropna=False)
        unique_ratio = round(unique_count / total_rows, 3)

        report[col] = {
            "unique_count": int(unique_count),
            "unique_ratio": unique_ratio,
            "high_cardinality": unique_ratio >= high_cardinality_threshold
        }

    return {
        "threshold": high_cardinality_threshold,
        "cardinality_report": report
    }


def duplicate_summary(df: pd.DataFrame) -> dict:
    """
    Detect duplicate rows in the dataset.
    """

    duplicate_mask = df.duplicated()
    duplicate_count = int(duplicate_mask.sum())

    return {
        "total_rows": len(df),
        "duplicate_rows": duplicate_count,
        "duplicate_ratio": round(duplicate_count / len(df), 3)
    }

def correlation_analysis(
        df: pd.DataFrame,
        method: str = "pearson",
        threshold: float = 0.5
) -> dict:
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        return{
            "method" : method,
            "strong_correlations" : {},
            "correlation_matrix" : {}
        }

    corr_matrix = numeric_df.corr(method=method)

def correlation_analysis(
    df: pd.DataFrame,
    method: str = "pearson",
    threshold: float = 0.5
) -> dict:
    """
    Compute correlation matrix for numeric columns and
    extract strongly correlated feature pairs.
    """

    numeric_df = df.select_dtypes(include=["number"])

    # Need at least 2 numeric columns to compute correlation
    if numeric_df.shape[1] < 2:
        return {
            "method": method,
            "strong_correlations": {},
            "correlation_matrix": {}
        }

    corr_matrix = numeric_df.corr(method=method)

    strong_pairs = {}

    for col in corr_matrix.columns:
        for other_col in corr_matrix.columns:
            if col == other_col:
                continue

            corr_value = corr_matrix.loc[col, other_col]

            if abs(corr_value) >= threshold:
                pair_key = tuple(sorted([col, other_col]))
                strong_pairs[pair_key] = round(corr_value, 3)

    return {
        "method": method,
        "threshold": threshold,
        "strong_correlations": strong_pairs,
        "correlation_matrix": corr_matrix.round(3).to_dict()
    }
