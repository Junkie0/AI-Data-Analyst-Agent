from src.ingestion.loader import DataLoader
from src.validation.schema import inspect_schema
from src.utils.pretty_print import print_schema

df = DataLoader.load("data/sample/superstore_clean.csv")
schema = inspect_schema(df)

print_schema(schema)