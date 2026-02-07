from src.ingestion.loader import DataLoader
from src.validation.quality_checks import (
    high_missing_columns,
    constant_columns,
    id_like_columns,
    string_date_columns
)

df = DataLoader.load("data/sample/consumer_complaints_messy.csv")

print("\nHigh Missing Columns:")
print(high_missing_columns(df))

print("\nConstant Columns:")
print(constant_columns(df))

print("\nID-like Columns:")
print(id_like_columns(df))

print("\nString Date Columns:")
print(string_date_columns(df))
