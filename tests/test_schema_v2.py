from src.ingestion.loader import DataLoader
from src.schema.inference2 import infer_schema
from src.eda.basic_eda import run_basic_eda


# print("\n================ HR Dataset ================")
#
# df_hr = DataLoader.load("data/sample/hr_attrition_categorical.csv")
#
# schema_hr = infer_schema(df_hr)
# print(schema_hr)
#
# eda_hr = run_basic_eda(df_hr, schema_hr["summary"])
# print(eda_hr)
#
#
#
# print("\n================ Superstore Dataset ================")
#
# df_super = DataLoader.load("data/sample/superstore_clean.csv")
#
# schema_super = infer_schema(df_super)
# print(schema_super)
#
# eda_super = run_basic_eda(df_super, schema_super["summary"])
# print(eda_super)
#
#
#
# print("\n================ Complaints Dataset ================")
#
# df_complaints = DataLoader.load("data/sample/consumer_complaints_messy.csv")
#
# schema_complaints = infer_schema(df_complaints)
# print(schema_complaints)
#
# eda_complaints = run_basic_eda(df_complaints, schema_complaints["summary"])
# print(eda_complaints)

print("\n================ Rideshare Dataset ================")

df_complaints = DataLoader.load("data/sample/3/user_music_listen_data.csv")

schema_complaints = infer_schema(df_complaints)
print(schema_complaints)

eda_complaints = run_basic_eda(df_complaints, schema_complaints["summary"])
print(eda_complaints)