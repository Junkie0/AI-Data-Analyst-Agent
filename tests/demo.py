#!/usr/bin/env python3
"""
FINAL DEMO: Complete AI Data Analyst System (Phase 1-5)
Shows the complete pipeline with production architecture
"""

from src.core.pipeline import AnalysisPipeline


def main():
    """Run final demo showing all phases working together"""
    
    print("\n" + "="*80)
    print("AI DATA ANALYST AGENT - FINAL DEMONSTRATION")
    print("Phase 1-5 + Production Architecture".center(80))
    print("="*80)
    
    # Create pipeline with configuration
    pipeline = AnalysisPipeline({
        "output_dir": "outputs/demo",
        "save_intermediate": True,
        "verbose": True
    })
    
    # Run analysis
    print("\n[STARTING] Complete Analysis Pipeline...")
    results = pipeline.run(
        "data/sample/superstore_clean.csv",
        "Superstore_Sales_Demo"
    )
    
    # Show insights summary
    print("\n" + "="*80)
    print("INSIGHTS SUMMARY")
    print("="*80)
    
    insights = results['insights']
    print(f"\nTotal Insights: {insights['count']}")
    print(f"Summary: {insights['summary']}")
    
    print("\nInsights by Severity:")
    for severity, count in insights['metadata']['by_severity'].items():
        if count > 0:
            print(f"  {severity.upper():10} : {count}")
    
    # Show top insights
    print("\nTop 5 Insights Generated:")
    for i, insight in enumerate(insights['insights'][:5], 1):
        print(f"  [{i}] {insight['title']} (Severity: {insight['severity']})")
    
    # Show report sections
    print("\n" + "="*80)
    print("NATURAL LANGUAGE REPORT GENERATED")
    print("="*80)
    
    report = results['report']
    print(f"\nReport sections generated: {len(report)}")
    for section_name in report.keys():
        print(f"  - {section_name}")
    
    # Show executive summary
    if 'executive_summary' in report:
        print("\n" + "-"*80)
        print("EXECUTIVE SUMMARY (from Natural Language Report):")
        print("-"*80)
        print(report['executive_summary'][:500] + "...")
    
    # Final message
    print("\n" + "="*80)
    print("DEMONSTRATION COMPLETE")
    print("="*80)
    print("""
System Successfully Demonstrated:

WHAT WAS BUILT:
 - Phase 1: Data Ingestion (CSV/Excel loading)
 - Phase 2: Schema Inference (type detection)
 - Phase 3: EDA (numeric + categorical analysis)
 - Phase 4: Insight Generation (14 insight types)
 - Phase 5: Natural Language Reports (NEW)
 - Production Architecture (CLI + packaging)

PRODUCTION-GRADE FEATURES:
 - CLI Tool: ai-analyst (multiple commands)
 - Python Packaging: setup.py + pyproject.toml
 - Configuration System: YAML-based
 - Pipeline Orchestration: Unified API
 - Error Handling: Robust + UTF-8 support
 - Performance: <10s per dataset

HOW TO USE:

  Option 1 - Programmatic (Python):
    from src.core.pipeline import AnalysisPipeline
    pipeline = AnalysisPipeline()
    results = pipeline.run('data/file.csv')

  Option 2 - Command Line:
    python -m ai_data_analyst.cli analyze data/file.csv --print-report
    python -m ai_data_analyst.cli batch data/sample/ --recursive

  Option 3 - After pip install:
    ai-analyst analyze data/file.csv --verbose

OUTPUT ARTIFACTS:
  - Structured insights (JSON)
  - Natural language report (TXT)
  - Analysis summary (TXT)
  - Automatic output organization with timestamps

This system is recruitment-ready and demonstrates:
  - End-to-end ML engineering
  - Production software architecture
  - Python best practices
  - Data analysis pipeline design
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
