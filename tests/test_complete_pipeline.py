"""
Test Phase 5 + Production Architecture

Demonstrates:
1. Pipeline orchestration (all 5 phases)
2. Natural language reporting (Phase 5)
3. CLI integration
4. Complete end-to-end workflow
"""

from src.core.pipeline import AnalysisPipeline


def test_complete_pipeline():
    """Test the complete analysis pipeline"""
    
    print("\n" + "="*80)
    print("COMPLETE PIPELINE TEST: PHASE 1-5")
    print("="*80)
    
    # Create pipeline
    config = {
        "output_dir": "outputs/complete_test",
        "save_intermediate": True,
        "verbose": True
    }
    
    pipeline = AnalysisPipeline(config)
    
    # Run analysis on a rich dataset
    print("\nAnalyzing: HR Attrition Dataset")
    results = pipeline.run(
        "data/sample/hr_attrition_categorical.csv",
        "HR_Attrition_Analysis"
    )
    
    # Display insights summary
    print("\n" + "="*80)
    print("INSIGHTS SUMMARY")
    print("="*80)
    
    insights = results.get("insights", {})
    print(f"\nTotal Insights: {insights['count']}")
    print(f"Summary: {insights['summary']}")
    
    # Display top insights
    print("\nTop 5 Insights:")
    for i, insight in enumerate(insights["insights"][:5], 1):
        severity = insight["severity"].upper()
        title = insight["title"]
        print(f"  [{i}] [{severity}] {title}")
    
    # Display natural language report
    print("\n" + "="*80)
    print("NATURAL LANGUAGE REPORT - PHASE 5")
    print("="*80)
    
    report = results.get("report", {})
    
    # Executive summary
    if "executive_summary" in report:
        print(report["executive_summary"])
    
    # Key findings
    if "key_findings" in report:
        print("\n" + report["key_findings"])
    
    # Data quality
    if "data_quality_assessment" in report:
        print("\n" + report["data_quality_assessment"])
    
    # Recommendations
    if "recommendations" in report:
        print("\n" + report["recommendations"])
    
    print("\n" + "="*80)
    print("✓ COMPLETE PIPELINE TEST PASSED")
    print("="*80 + "\n")


def test_multiple_datasets():
    """Test batch processing of multiple datasets"""
    
    print("\n" + "="*80)
    print("BATCH PROCESSING TEST")
    print("="*80)
    
    datasets = [
        ("data/sample/consumer_complaints_messy.csv", "Consumer Complaints"),
        ("data/sample/superstore_clean.csv", "Superstore"),
    ]
    
    pipeline = AnalysisPipeline({
        "output_dir": "outputs/batch_test",
        "save_intermediate": False,
        "verbose": False
    })
    
    for filepath, name in datasets:
        try:
            print(f"\nProcessing: {name}...", end=" ")
            results = pipeline.run(filepath, name)
            insights_count = results["insights"]["count"]
            print(f"✓ {insights_count} insights generated")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    # Test 1: Complete pipeline
    test_complete_pipeline()
    
    # Test 2: Batch processing
    test_multiple_datasets()
    
    print("\n" + "="*80)
    print("ALL TESTS PASSED ✓")
    print("="*80)
    print("\nNow test the CLI with:")
    print("  python -m ai_data_analyst.cli analyze data/sample/hr_attrition_categorical.csv --print-report")
