import pandas as pd
import numpy as np


def infer_schema(df: pd.DataFrame) -> dict:
    total_rows = len(df)

    schema = {
        "identifier": [],
        "datetime": [],
        "binary": [],
        "ordinal": [],
        "numeric": [],
        "categorical": [],
        "constant": []
    }

    for col in df.columns:
        series = df[col]
        unique_count = series.nunique(dropna=False)
        unique_ratio = unique_count / total_rows
        col_lower = col.lower()

        # -------------------------
        # 0️⃣ Constant Column
        # -------------------------
        if unique_count <= 1:
            schema["constant"].append(col)
            continue

        # -------------------------
        # 1️⃣ Datetime Detection
        # -------------------------
        if series.dtype == "object":
            parsed = pd.to_datetime(series, errors="coerce")
            if parsed.notna().mean() > 0.8:
                schema["datetime"].append(col)
                continue

        # -------------------------
        # 2️⃣ Identifier Detection
        # -------------------------
        if (
            unique_ratio > 0.98
            or any(keyword in col_lower for keyword in ["id", "number"])
        ):
            schema["identifier"].append(col)
            continue

        # -------------------------
        # 3️⃣ Numeric Columns
        # -------------------------
        if np.issubdtype(series.dtype, np.number):

            # Small numeric range → ordinal
            if unique_count <= 10:
                schema["ordinal"].append(col)
            else:
                schema["numeric"].append(col)

            continue

        # -------------------------
        # 4️⃣ Binary (only for non-numeric)
        # -------------------------
        if unique_count == 2:
            schema["binary"].append(col)
            continue

        # -------------------------
        # 5️⃣ Categorical
        # -------------------------
        schema["categorical"].append(col)

    return schema