"""
Visualization Orchestrator - Unified Interface

Automatically generates all visualizations for a dataset
and manages output organization.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

from src.visualization import plots
from src.visualization.plots import (
    plot_numeric_histogram,
    plot_numeric_boxplot,
    plot_numeric_violin,
    plot_categorical_barplot,
    plot_correlation_heatmap,
    plot_missing_heatmap,
    plot_pairplot,
    plot_summary_statistics,
    get_visualization_columns
)


class VisualizationOrchestrator:
    """
    Orchestrates all visualization generation
    
    Automatically generates:
    - Histograms + KDE for numeric columns
    - Boxplots with outliers for numeric columns
    - Violin plots for distribution shape
    - Barplots for categorical columns
    - Correlation heatmap
    - Missing data patterns
    - Pairplots for relationships
    - Summary statistics
    """
    
    def __init__(self, output_dir: str = "outputs/visualizations"):
        """
        Initialize visualization orchestrator
        
        Args:
            output_dir: Root output directory for all visualizations
        """
        self.output_dir = output_dir
        self.results = {}
    
    def generate_all(self, df: pd.DataFrame, schema: Dict, 
                     dataset_name: str = "Dataset") -> Dict[str, any]:
        """
        Generate all visualizations for a dataset
        
        Args:
            df: DataFrame to visualize
            schema: Schema information (column types)
            dataset_name: Name for output organization
            
        Returns:
            Dictionary with all visualization paths organized by type
        """
        
        # Create timestamped output directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = Path(self.output_dir) / dataset_name / timestamp
        run_dir.mkdir(parents=True, exist_ok=True)
        
        # Get column groupings
        viz_cols = get_visualization_columns(schema)
        numeric_cols = viz_cols["numeric"]
        categorical_cols = viz_cols["categorical"]
        
        results = {
            "timestamp": timestamp,
            "output_dir": str(run_dir),
            "dataset_name": dataset_name,
            "histograms": [],
            "boxplots": [],
            "violin_plots": [],
            "barplots": [],
            "correlation_heatmap": None,
            "missing_heatmap": None,
            "pairplot": None,
            "summary_statistics": None,
            "total_plots_generated": 0
        }
        
        # ===== Numeric Visualizations =====
        if numeric_cols:
            # Limit to top 5 for performance
            top_numeric = numeric_cols[:5]
            
            for col in top_numeric:
                # Histogram
                hist = plot_numeric_histogram(df, col, str(run_dir))
                if hist:
                    results["histograms"].append(hist)
                    results["total_plots_generated"] += 1
                
                # Boxplot
                box = plot_numeric_boxplot(df, col, str(run_dir))
                if box:
                    results["boxplots"].append(box)
                    results["total_plots_generated"] += 1
                
                # Violin plot
                violin = plot_numeric_violin(df, col, str(run_dir))
                if violin:
                    results["violin_plots"].append(violin)
                    results["total_plots_generated"] += 1
        
        # ===== Categorical Visualizations =====
        if categorical_cols:
            # Limit to top 5 for performance
            top_categorical = categorical_cols[:5]
            
            for col in top_categorical:
                bar = plot_categorical_barplot(df, col, str(run_dir))
                if bar:
                    results["barplots"].append(bar)
                    results["total_plots_generated"] += 1
        
        # ===== Correlation Analysis =====
        if len(numeric_cols) >= 2:
            heatmap = plot_correlation_heatmap(df, numeric_cols, str(run_dir))
            if heatmap:
                results["correlation_heatmap"] = heatmap
                results["total_plots_generated"] += 1
        
        # ===== Missing Data Pattern =====
        missing = plot_missing_heatmap(df, str(run_dir))
        if missing:
            results["missing_heatmap"] = missing
            results["total_plots_generated"] += 1
        
        # ===== Pairplot (for small numeric subsets) =====
        small_numeric = numeric_cols[:4] if len(numeric_cols) > 0 else []
        if 2 <= len(small_numeric) <= 4:
            pairplot = plot_pairplot(df, small_numeric, str(run_dir))
            if pairplot:
                results["pairplot"] = pairplot
                results["total_plots_generated"] += 1
        
        # ===== Summary Statistics =====
        if numeric_cols:
            stats = plot_summary_statistics(df, numeric_cols, str(run_dir))
            if stats:
                results["summary_statistics"] = stats
                results["total_plots_generated"] += 1
        
        self.results = results
        return results
    
    def print_summary(self):
        """Print summary of generated visualizations"""
        
        if not self.results:
            print("No visualizations generated yet.")
            return
        
        results = self.results
        
        print(f"\n{'='*70}")
        print("VISUALIZATION SUMMARY")
        print(f"{'='*70}")
        print(f"\nDataset: {results['dataset_name']}")
        print(f"Output Directory: {results['output_dir']}")
        print(f"Total Plots Generated: {results['total_plots_generated']}")
        
        print(f"\n{'Plot Type':<25} {'Count':<10} {'Files'}")
        print("-"*70)
        
        categories = [
            ("Histograms", results["histograms"]),
            ("Boxplots", results["boxplots"]),
            ("Violin Plots", results["violin_plots"]),
            ("Barplots", results["barplots"]),
        ]
        
        for cat_name, cat_files in categories:
            if cat_files:
                print(f"{cat_name:<25} {len(cat_files):<10} ✓")
        
        if results["correlation_heatmap"]:
            print(f"{'Correlation Heatmap':<25} {1:<10} ✓")
        
        if results["missing_heatmap"]:
            print(f"{'Missing Data Pattern':<25} {1:<10} ✓")
        
        if results["pairplot"]:
            print(f"{'Pairplot':<25} {1:<10} ✓")
        
        if results["summary_statistics"]:
            print(f"{'Summary Statistics':<25} {1:<10} ✓")
        
        print(f"{'='*70}\n")
    
    def get_report_markdown(self) -> str:
        """Generate markdown report for visualizations"""
        
        if not self.results:
            return "## Visualizations\n\nNo visualizations generated.\n"
        
        results = self.results
        
        md = f"""## Visualizations

**Generated**: {results['timestamp']}
**Total Plots**: {results['total_plots_generated']}
**Output Directory**: `{results['output_dir']}`

### Core Visualizations

"""
        
        if results["histograms"]:
            md += f"**Distributions (Histograms with KDE)**: {len(results['histograms'])} plots\n"
        
        if results["boxplots"]:
            md += f"**Outlier Detection (Boxplots)**: {len(results['boxplots'])} plots\n"
        
        if results["violin_plots"]:
            md += f"**Distribution Shape (Violin Plots)**: {len(results['violin_plots'])} plots\n"
        
        if results["barplots"]:
            md += f"**Category Distributions (Barplots)**: {len(results['barplots'])} plots\n"
        
        if results["correlation_heatmap"]:
            md += f"\n**Correlation Matrix**: Generated correlation analysis\n"
        
        if results["missing_heatmap"]:
            md += f"**Missing Data Patterns**: Identified missing data structure\n"
        
        if results["pairplot"]:
            md += f"**Pairplot**: Relationships between numeric columns\n"
        
        if results["summary_statistics"]:
            md += f"**Summary Statistics**: Visual summary of key metrics\n"
        
        return md


def generate_visualizations(df: pd.DataFrame, schema: Dict, 
                           dataset_name: str = "Dataset",
                           output_dir: str = "outputs/visualizations") -> Dict:
    """
    Convenience function to generate visualizations
    
    Args:
        df: DataFrame to visualize
        schema: Schema information
        dataset_name: Name for output organization
        output_dir: Root visualization output directory
        
    Returns:
        Dictionary with all visualization paths
    """
    
    orchestrator = VisualizationOrchestrator(output_dir)
    results = orchestrator.generate_all(df, schema, dataset_name)
    
    return results
