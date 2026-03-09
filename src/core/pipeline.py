"""
Core Pipeline Orchestration

Main orchestration layer that ties all phases together.
Provides unified interface for the entire analysis pipeline.
"""

from typing import Dict, Any, Optional
import json
from datetime import datetime
import os
from pathlib import Path

from src.ingestion.loader import DataLoader
from src.schema.inference2 import infer_schema
from src.eda.basic_eda import run_basic_eda
from src.insights.insight_engine import InsightEngine
from src.reporting.report_writer import ReportWriter
from src.visualization.orchestrator import VisualizationOrchestrator


class AnalysisPipeline:
    """
    Complete data analysis pipeline from ingestion to insights to reports.
    
    Orchestrates all 5 phases:
    1. Ingestion
    2. Schema Inference
    3. EDA
    4. Insight Generation
    5. Natural Language Reporting
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize pipeline with optional configuration
        
        Args:
            config: Pipeline configuration dictionary
        """
        self.config = config or self._default_config()
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def _default_config(self) -> Dict[str, Any]:
        """Default pipeline configuration"""
        return {
            "output_dir": "outputs/analysis",
            "save_intermediate": True,
            "verbose": True,
            "insight_threshold": {
                "correlation": 0.5,
                "missing_ratio": 0.3,
                "cardinality_ratio": 0.95
            }
        }
    
    def run(self, filepath: str, dataset_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the complete analysis pipeline
        
        Args:
            filepath: Path to data file
            dataset_name: Optional name for the dataset
            
        Returns:
            Dictionary with all analysis results
        """
        
        self.start_time = datetime.now()
        dataset_name = dataset_name or Path(filepath).stem
        
        if self.config.get("verbose"):
            print(f"\n{'='*70}")
            print(f"ANALYSIS PIPELINE: {dataset_name}")
            print(f"{'='*70}")
        
        try:
            # Phase 1-2: Ingestion & Schema
            if self.config.get("verbose"):
                print("\n[Phase 1-2] Data Ingestion & Schema Inference...")
            df = DataLoader.load(filepath)
            schema = infer_schema(df)
            self.results["dataframe_shape"] = df.shape
            self.results["schema"] = schema
            
            if self.config.get("verbose"):
                print(f"  ✓ Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")
                print(f"  ✓ Inferred schema for {len(schema['columns'])} columns")
            
            # Phase 3: EDA
            if self.config.get("verbose"):
                print("\n[Phase 3] Exploratory Data Analysis...")
            eda_results = run_basic_eda(df, schema)
            self.results["eda"] = eda_results
            
            if self.config.get("verbose"):
                num_numeric = len(eda_results.get("numeric_summary", {}))
                num_categorical = len(eda_results.get("categorical_summary", {}))
                num_corr = len(eda_results.get("strong_correlations", {}))
                print(f"  ✓ Numeric columns: {num_numeric}")
                print(f"  ✓ Categorical columns: {num_categorical}")
                print(f"  ✓ Correlations: {num_corr}")
            
            # Phase 3.5: Visualization (Enhanced)
            if self.config.get("verbose"):
                print("\n[Phase 3.5] Visualization Engine...")
            
            viz_orchestrator = VisualizationOrchestrator(
                output_dir=self.config.get("viz_output_dir", "outputs/visualizations")
            )
            viz_results = viz_orchestrator.generate_all(df, schema, dataset_name)
            self.results["visualizations"] = viz_results
            
            if self.config.get("verbose"):
                print(f"  ✓ Generated {viz_results['total_plots_generated']} visualizations")
                print(f"  ✓ Saved to: {viz_results['output_dir']}")
            
            # Phase 4: Insights
            if self.config.get("verbose"):
                print("\n[Phase 4] Insight Generation...")
            engine = InsightEngine(df=df, schema=schema)
            insights_result = engine.generate_insights(eda_results)
            self.results["insights"] = insights_result
            
            if self.config.get("verbose"):
                print(f"  ✓ Generated {insights_result['count']} insights")
                sev = insights_result['metadata']['by_severity']
                if sev.get('critical', 0) > 0:
                    print(f"    ⚠️  {sev.get('critical', 0)} CRITICAL")
                if sev.get('high', 0) > 0:
                    print(f"    ⚡ {sev.get('high', 0)} HIGH")
                if sev.get('medium', 0) > 0:
                    print(f"    ℹ️  {sev.get('medium', 0)} MEDIUM")
            
            # Phase 5: Reports
            if self.config.get("verbose"):
                print("\n[Phase 5] Natural Language Report Generation...")
            
            # Reconstruct insights list for reporter
            insights_list = []
            from src.insights.insight_types import Insight
            for insight_dict in insights_result["insights"]:
                insight = Insight(
                    type=insight_dict["type"],
                    severity=insight_dict["severity"],
                    column=insight_dict["column"],
                    title=insight_dict["title"],
                    description=insight_dict.get("description", ""),
                    value=insight_dict["value"],
                    context=insight_dict["context"]
                )
                insights_list.append(insight)
            
            reporter = ReportWriter()
            report = reporter.generate_full_report(
                insights_list,
                eda_results,
                dataset_name
            )
            self.results["report"] = report
            
            if self.config.get("verbose"):
                print(f"  ✓ Generated {len(report)} report sections")
            
            # Set end time before saving
            self.end_time = datetime.now()
            
            # Save results
            self._save_results(dataset_name)
            
            if self.config.get("verbose"):
                elapsed = (self.end_time - self.start_time).total_seconds()
                print(f"\n{'='*70}")
                print(f"✓ ANALYSIS COMPLETE in {elapsed:.1f}s")
                print(f"{'='*70}\n")
            
            return self.results
        
        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")
            raise
    
    def _save_results(self, dataset_name: str):
        """Save analysis results to output directory"""
        
        if not self.config.get("save_intermediate"):
            return
        
        output_dir = Path(self.config["output_dir"]) / dataset_name / datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save insights JSON
        insights_file = output_dir / "insights.json"
        with open(insights_file, "w", encoding="utf-8") as f:
            insights_data = {
                "count": self.results["insights"]["count"],
                "summary": self.results["insights"]["summary"],
                "metadata": self.results["insights"]["metadata"],
                "insights": self.results["insights"]["insights"]
            }
            json.dump(insights_data, f, indent=2, default=str)
        
        # Save report text
        report_file = output_dir / "report.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            for section_name, section_text in self.results["report"].items():
                f.write(f"\n{section_text}\n")
                f.write("\n" + "─"*70 + "\n")
        
        # Save summary
        summary_file = output_dir / "summary.txt"
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"Dataset: {dataset_name}\n")
            f.write(f"Shape: {self.results['dataframe_shape']}\n")
            f.write(f"Insights: {self.results['insights']['count']}\n")
            f.write(f"Visualizations Generated: {self.results['visualizations']['total_plots_generated']}\n")
            f.write(f"Visualization Output: {self.results['visualizations']['output_dir']}\n")
            f.write(f"Analysis Time: {(self.end_time - self.start_time).total_seconds():.1f}s\n")
        
        if self.config.get("verbose"):
            print(f"\n  Files saved to: {output_dir}")
    
    def print_report(self):
        """Print the natural language report to console"""
        
        if "report" not in self.results:
            print("No report available. Run pipeline first.")
            return
        
        report = self.results["report"]
        viz_results = self.results.get("visualizations", {})
        
        print("\n" + "="*70)
        
        # Include visualization summary
        if viz_results:
            print(f"\nVISUALIZATIONS GENERATED: {viz_results.get('total_plots_generated', 0)} plots")
            print(f"Output Directory: {viz_results.get('output_dir', 'N/A')}\n")
        
        for section_name, section_text in report.items():
            print(section_text)
            print("─"*70)
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Get insights summary"""
        return self.results.get("insights", {})
    
    def get_report(self) -> Dict[str, str]:
        """Get full report"""
        return self.results.get("report", {})
