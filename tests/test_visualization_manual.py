from src.ingestion.loader import DataLoader
from src.schema.inference2 import infer_schema
from src.visualization.auto_viz import generate_visualizations

df = DataLoader.load("data/sample/232/rideshare_dataset.csv")

schema = infer_schema(df)

plots = generate_visualizations(df, schema)

print("Generated plots:")
print(plots)