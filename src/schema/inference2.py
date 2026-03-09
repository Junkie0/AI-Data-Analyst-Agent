import pandas as pd

def infer_schema(df: pd.DataFrame) -> dict:

    total_rows = len(df)

    schema = {
        "columns": {},
        "summary": {
            "identifier": [],
            "datetime": [],
            "binary": [],
            "ordinal": [],
            "numeric": [],
            "categorical": [],
            "constant": []
        },
        "warnings": []
    }

    for col in df.columns:
        series = df[col]
        series_clean = series.dropna()
        col_lower = col.lower()
        nunique = series.nunique(dropna=False)
        unique_ratio = nunique / total_rows if total_rows > 0 else 0

        # ---------------------
        # CONSTANT
        # ---------------------
        if nunique == 1:
            schema["summary"]["constant"].append(col)
            schema["columns"][col] = {
                "type": "constant",
                "confidence": 1.0,
                "ambiguous": False,
                "warning": None,
                "reasons": ["only one unique value"]
            }
            continue

        # ---------------------
        # SCORE BOARD
        # ---------------------
        scores = {
            "identifier": 0,
            "datetime": 0,
            "binary": 0,
            "ordinal": 0,
            "numeric": 0,
            "categorical": 0
        }

        reasons = []

        # Name signals
        if any(k in col_lower for k in ["id", "number", "code", "zip", "postal"]):
            scores["identifier"] += 4
            reasons.append("identifier keyword in name")

        if "date" in col_lower:
            scores["datetime"] += 3
            reasons.append("date keyword in name")

        # Dtype signals
        if pd.api.types.is_numeric_dtype(series_clean):
            scores["numeric"] += 2
            reasons.append("numeric dtype")
        else:
            scores["categorical"] += 1

        # Uniqueness signals
        if unique_ratio > 0.95 and pd.api.types.is_numeric_dtype(series):
            scores["identifier"] += 2
            reasons.append("very high uniqueness")

        if nunique == 2:
            scores["binary"] += 4
            reasons.append("exactly two unique values")

        if pd.api.types.is_numeric_dtype(series) and 3 <= nunique <= 10:
            scores["ordinal"] += 2
            reasons.append("small numeric range")

        # Datetime parsing
        if series.dtype == "object" and "date" in col_lower:
            try:
                parsed = pd.to_datetime(series, errors="coerce")
                if parsed.notnull().mean() > 0.8:
                    scores["datetime"] += 6
                    reasons.append("datetime parse success")
            except:
                pass

        # ---------------------
        # FINAL DECISION
        # ---------------------
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        final_type = sorted_scores[0][0]
        max_score = sorted_scores[0][1]
        second_score = sorted_scores[1][1]

        # Dominance-based confidence
        if max_score > 0:
            confidence = round((max_score - second_score) / max_score, 2)
        else:
            confidence = 0

        # Improved ambiguity detection
        ambiguous = False
        if (
                second_score > 0
                and abs(max_score - second_score) <= 1
        ):
            ambiguous = True

        warning = None
        if confidence < 0.7:
            warning = "Low confidence classification"
            schema["warnings"].append(f"{col}: low confidence ({confidence})")

        if ambiguous:
            schema["warnings"].append(
                f"{col}: ambiguous between {sorted_scores[0][0]} and {sorted_scores[1][0]}"
            )

        schema["summary"][final_type].append(col)

        schema["columns"][col] = {
            "type": final_type,
            "confidence": confidence,
            "ambiguous": ambiguous,
            "top_competitor": sorted_scores[1][0],
            "scores": scores,
            "unique_ratio": round(unique_ratio, 3),
            "warning": warning,
            "reasons": reasons
        }

    return schema