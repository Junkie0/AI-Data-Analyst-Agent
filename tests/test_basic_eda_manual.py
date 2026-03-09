from src.ingestion.loader import DataLoader
from src.schema.inference2 import infer_schema

from src.eda.basic_eda import (
    numeric_summary,
    categorical_summary,
    cardinality_report,
    duplicate_summary,
    correlation_analysis
)

# Load dataset
df = DataLoader.load("data/sample/consumer_complaints_messy.csv")

schema = infer_schema(df)

print("\n========================================")
print("INFERRED SCHEMA")
print("========================================")
print(schema)

# -----------------------------
# Column Type Separation
# -----------------------------
print("\n" + "=" * 40)
print("COLUMN TYPES")
print("=" * 40)
print(infer_schema(df))

# -----------------------------
# Numeric Summary
# -----------------------------
print("\n" + "=" * 40)
print("NUMERIC SUMMARY")
print("=" * 40)

numeric = numeric_summary(df, schema)
for col, stats in numeric["numeric_summary"].items():
    print(f"\n{col}")
    for k, v in stats.items():
        print(f"  {k}: {v}")

# -----------------------------
# Categorical Summary (sample)
# -----------------------------
print("\n" + "=" * 40)
print("CATEGORICAL SUMMARY (SAMPLE)")
print("=" * 40)

categorical = categorical_summary(df, schema)
for col, stats in list(categorical["categorical_summary"].items())[:3]:
    print(f"\n{col}")
    print(f"  Unique Values: {stats['unique_values']}")
    print(f"  Missing Ratio: {stats['missing_ratio']}")
    print(f"  Top Values:")
    for val, cnt in stats["top_values"].items():
        print(f"    {val}: {cnt}")

# -----------------------------
# Cardinality Report (sample)
# -----------------------------
print("\n" + "=" * 40)
print("CARDINALITY REPORT (SAMPLE)")
print("=" * 40)

cardinality = cardinality_report(df)
for col, info in list(cardinality["cardinality_report"].items())[:5]:
    print(f"\n{col}")
    print(f"  Unique Count: {info['unique_count']}")
    print(f"  Unique Ratio: {info['unique_ratio']}")
    print(f"  High Cardinality: {info['high_cardinality']}")

# -----------------------------
# Duplicate Summary
# -----------------------------
print("\n" + "=" * 40)
print("DUPLICATE SUMMARY")
print("=" * 40)
print(duplicate_summary(df))

# -----------------------------
# Correlations Analysis
# -----------------------------
print("\n" + "=" * 40)
print("CORRELATION ANALYSIS")
print("=" * 40)

correlation = correlation_analysis(df, schema, threshold=0.5)

print("\nStrong Correlations:")
for pair, value in correlation["strong_correlations"].items():
    print(f"{pair}: {value}")