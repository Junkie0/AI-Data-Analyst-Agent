"""
Test Phase 4: Detailed Insights Analysis

Shows more complete insights from different dataset types
"""

from src.ingestion.loader import DataLoader
from src.schema.inference2 import infer_schema
from src.eda.basic_eda import run_basic_eda
from src.insights.insight_engine import InsightEngine
import json


def test_dataset(filepath, name):
    """Test insights on a single dataset"""
    
    print("\n" + "=" * 70)
    print(f"TESTING: {name}")
    print("=" * 70)
    
    try:
        df = DataLoader.load(filepath)
        print(f"✓ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
        
        schema = infer_schema(df)
        print(f"✓ Schema inferred")
        
        eda_results = run_basic_eda(df, schema)
        print(f"✓ EDA complete")
        
        # Verify EDA outputs
        print(f"\nEDA Outputs Available:")
        for key in ['numeric_summary', 'categorical_summary', 'cardinality_report', 
                    'duplicate_summary', 'strong_correlations']:
            has_key = key in eda_results
            count = len(eda_results.get(key, {})) if has_key else 0
            print(f"  {key:25} : {count:5} items" if has_key else f"  {key:25} : Missing")
        
        # Generate insights
        engine = InsightEngine(df=df, schema=schema)
        insights = engine.generate_insights(eda_results)
        
        print(f"\n{'─' * 70}")
        print(f"INSIGHTS SUMMARY")
        print(f"{'─' * 70}")
        print(f"Total Insights  : {insights['count']}")
        print(f"Summary: {insights['summary']}")
        
        # Show by severity
        severity_counts = insights['metadata']['by_severity']
        print(f"\nBy Severity:")
        for severity in ['critical', 'high', 'medium', 'low']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                print(f"  {severity.upper():8} : {count}")
        
        # Show natural language insights (top 5)
        print(f"\nTop Insights (Natural Language):")
        for i, insight_text in enumerate(insights['natural_language'][:5], 1):
            severity = insight_text['severity'].upper()
            text = insight_text['text'][:80]  # Truncate for display
            print(f"  [{i}] [{severity}] {text}...")
        
        return insights
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return None


# =========================================================================
# Test Multiple Datasets
# =========================================================================

print("\n" + "="*70)
print("PHASE 4: MULTI-DATASET INSIGHT ANALYSIS")
print("="*70)

datasets = [
    ("data/sample/consumer_complaints_messy.csv", "Consumer Complaints (Messy)"),
    ("data/sample/hr_attrition_categorical.csv", "HR Attrition"),
    ("data/sample/superstore_clean.csv", "Superstore Sales"),
    ("data/sample/Smartphone_Usage_Productivity_Dataset_50000.csv", "Smartphone Usage"),
]

all_results = {}

for filepath, name in datasets:
    result = test_dataset(filepath, name)
    if result:
        all_results[name] = result

# =========================================================================
# Comparative Summary
# =========================================================================

print("\n" + "=" * 70)
print("COMPARATIVE ANALYSIS")
print("=" * 70)

print(f"\n{'Dataset':<35} {'Total':<8} {'High':<8} {'Medium':<8} {'Low':<8}")
print("─" * 70)

for name, result in all_results.items():
    total = result['count']
    high = result['metadata']['by_severity'].get('high', 0)
    medium = result['metadata']['by_severity'].get('medium', 0)
    low = result['metadata']['by_severity'].get('low', 0)
    print(f"{name:<35} {total:<8} {high:<8} {medium:<8} {low:<8}")

print("\n✓ Phase 4 Multi-Dataset Test Complete")
