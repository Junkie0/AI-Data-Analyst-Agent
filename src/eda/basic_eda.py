import pandas as pd
from scipy import stats


# ---------------------------------------------------
# Numeric Summary (Schema-Driven)
# ---------------------------------------------------
def numeric_summary(df, schema):
    numeric_cols = schema.get("numeric", []) + schema.get("ordinal", [])

    summary = {}

    for col in numeric_cols:

        # Force numeric conversion (handles bools like True/False)
        series = pd.to_numeric(df[col], errors="coerce").astype(float)

        if series.dropna().empty:
            continue

        summary[col] = {
            "count": int(series.count()),
            "mean": series.mean(),
            "std": series.std(),
            "min": series.min(),
            "25%": series.quantile(0.25),
            "50%": series.quantile(0.50),
            "75%": series.quantile(0.75),
            "max": series.max(),
            "missing_ratio": round(series.isnull().mean(), 3),
            "skewness": round(stats.skew(series.dropna()), 3),
            "kurtosis": round(stats.kurtosis(series.dropna()), 3)
        }

    return {"numeric_summary": summary}


# ---------------------------------------------------
# Categorical Summary (Schema-Driven)
# ---------------------------------------------------
def categorical_summary(df, schema):
    categorical_cols = schema.get("categorical", []) + schema.get("binary", [])

    summary = {}

    for col in categorical_cols:
        series = df[col]

        summary[col] = {
            "unique_values": series.nunique(),
            "missing_ratio": round(series.isnull().mean(), 3),
            "top_values": series.value_counts().head(5).to_dict()
        }

    return {"categorical_summary": summary}


# ---------------------------------------------------
# Cardinality Report (Optional Schema Upgrade Later)
# ---------------------------------------------------
def cardinality_report(df: pd.DataFrame, high_cardinality_threshold: float = 0.5) -> dict:
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


# ---------------------------------------------------
# Duplicate Summary
# ---------------------------------------------------
def duplicate_summary(df: pd.DataFrame) -> dict:
    duplicate_count = int(df.duplicated().sum())

    return {
        "duplicate_summary": {
            "total_rows": len(df),
            "duplicate_rows": duplicate_count,
            "duplicate_ratio": round(duplicate_count / len(df), 3)
        }
    }


# ---------------------------------------------------
# Correlation Analysis (Schema-Driven)
# ---------------------------------------------------
def correlation_analysis(
    df,
    schema,
    method: str = "pearson",
    threshold: float = 0.5
) -> dict:

    numeric_cols = schema.get("numeric", []) + schema.get("ordinal", [])

    if len(numeric_cols) < 2:
        return {
            "method": method,
            "threshold": threshold,
            "strong_correlations": {},
            "correlation_matrix": {}
        }

    corr_matrix = df[numeric_cols].corr(method=method)

    strong_pairs = {}

    for col1 in corr_matrix.columns:
        for col2 in corr_matrix.columns:
            if col1 >= col2:
                continue

            corr_value = corr_matrix.loc[col1, col2]

            if abs(corr_value) >= threshold:
                strong_pairs[(col1, col2)] = round(corr_value, 3)

    return {
        "method": method,
        "threshold": threshold,
        "strong_correlations": strong_pairs,
        "correlation_matrix": corr_matrix.round(3).to_dict()
    }

# ---------------------------------------------------
# MASTER EDA ENGINE
# ---------------------------------------------------
def run_basic_eda(df, schema):

    results = {}
    
    # Extract the summary dict if full schema is passed
    schema_summary = schema.get("summary", schema) if isinstance(schema, dict) else schema

    results.update(numeric_summary(df, schema_summary))
    results.update(categorical_summary(df, schema_summary))
    results.update(cardinality_report(df))
    results.update(duplicate_summary(df))
    results.update(correlation_analysis(df, schema_summary))
    
    # Include schema summary for insights
    results["summary"] = schema_summary

    return results