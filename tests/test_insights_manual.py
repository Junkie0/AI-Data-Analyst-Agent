"""
Test Phase 4: Insight Generation Engine

Demonstrates the complete pipeline:
Data -> Ingestion -> Schema -> Validation -> EDA -> Insights
"""

from src.ingestion.loader import DataLoader
from src.schema.inference2 import infer_schema
from src.eda.basic_eda import run_basic_eda
from src.insights.insight_engine import InsightEngine
import json


# Load dataset
print("\n" + "=" * 60)
print("PHASE 4: INSIGHT GENERATION ENGINE TEST")
print("=" * 60)

df = DataLoader.load("data/sample/consumer_complaints_messy.csv")
print(f"\n✓ Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")

# Infer schema
schema = infer_schema(df)
print(f"✓ Inferred schema: {len(schema['columns'])} columns classified")

# Run EDA
eda_results = run_basic_eda(df, schema)
print(f"✓ EDA complete")

# =========================================================================
# PHASE 4: GENERATE INSIGHTS
# =========================================================================

print("\n" + "=" * 60)
print("GENERATING INSIGHTS...")
print("=" * 60)

engine = InsightEngine(df=df, schema=schema)
insights = engine.generate_insights(eda_results)

# =========================================================================
# Display Results
# =========================================================================

print("\n" + "=" * 60)
print("EXECUTIVE SUMMARY")
print("=" * 60)
print(f"\n{insights['summary']}")

print("\n" + "=" * 60)
print("INSIGHTS BY SEVERITY")
print("=" * 60)

severity_counts = insights['metadata']['by_severity']
for severity in ['critical', 'high', 'medium', 'low']:
    count = severity_counts.get(severity, 0)
    if count > 0:
        print(f"  {severity.upper():8} : {count} insights")

print("\n" + "=" * 60)
print("INSIGHTS BY TYPE")
print("=" * 60)

type_counts = insights['metadata']['by_type']
for insight_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {insight_type:30} : {count}")

print("\n" + "=" * 60)
print("NATURAL LANGUAGE INSIGHTS (Top 10)")
print("=" * 60)

for i, insight_text in enumerate(insights['natural_language'][:10], 1):
    severity = insight_text['severity'].upper()
    text = insight_text['text']
    print(f"\n[{i}] [{severity}] {text}")

# =========================================================================
# Show structured insights (first 5)
# =========================================================================

print("\n" + "=" * 60)
print("STRUCTURED INSIGHTS (First 5)")
print("=" * 60)

for i, insight in enumerate(insights['insights'][:5], 1):
    print(f"\n[{i}]")
    print(f"  Type     : {insight['type']}")
    print(f"  Severity : {insight['severity']}")
    print(f"  Column   : {insight['column']}")
    print(f"  Title    : {insight['title']}")
    print(f"  Value    : {insight['value']}")
    print(f"  Context  : {insight['context']}")

# =========================================================================
# Save full results to JSON
# =========================================================================

output_path = "outputs/insights_test.json"
with open(output_path, "w") as f:
    # Remove DataFrames that can't be serialized
    insights_copy = insights.copy()
    json.dump(insights_copy, f, indent=2, default=str)

print(f"\n✓ Full results saved to: {output_path}")

print("\n" + "=" * 60)
print("PHASE 4 TEST COMPLETE")
print("=" * 60)
