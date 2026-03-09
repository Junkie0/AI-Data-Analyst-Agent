"""
Enhanced Visualization Orchestrator - Phase 3 Integration

Generates all visualizations automatically and integrates with pipeline.
Supports: histograms, boxplots, barplots, heatmaps, violin plots, distribution plots
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# =========================================================================
# Theme Configuration
# =========================================================================

class VizTheme:
    """Visualization theme and styling"""
    
    PRIMARY_COLOR = "#2ecc71"      # Green
    SECONDARY_COLOR = "#3498db"    # Blue
    ACCENT_COLOR = "#f39c12"       # Orange
    WARNING_COLOR = "#e74c3c"      # Red
    NEUTRAL_COLOR = "#95a5a6"      # Gray
    
    @staticmethod
    def setup():
        """Apply theme settings"""
        sns.set_theme(style="whitegrid")
        sns.set_palette([VizTheme.PRIMARY_COLOR, VizTheme.SECONDARY_COLOR, VizTheme.ACCENT_COLOR])
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10


VizTheme.setup()


# =========================================================================
# Utility Functions
# =========================================================================

def ensure_output_dir(output_dir: str) -> Path:
    """Create output directory if it doesn't exist"""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_visualization_columns(schema: Dict) -> Dict[str, List[str]]:
    """Extract column names by type from schema"""
    summary = schema.get("summary", schema)
    
    return {
        "numeric": summary.get("numeric", []) + summary.get("ordinal", []),
        "categorical": summary.get("categorical", []) + summary.get("binary", []),
        "datetime": summary.get("datetime", []),
        "identifier": summary.get("identifier", []),
        "constant": summary.get("constant", [])
    }


# =========================================================================
# Enhanced Numeric Visualizations
# =========================================================================

def plot_numeric_histogram(df: pd.DataFrame, column: str, output_dir: str) -> Optional[str]:
    """Enhanced histogram with distribution curve"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        data = df[column].dropna()
        if len(data) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.histplot(
            data,
            kde=True,
            color=VizTheme.PRIMARY_COLOR,
            edgecolor="black",
            alpha=0.7,
            ax=ax
        )
        
        ax.set_title(f"{column} - Distribution", fontsize=14, weight="bold", pad=20)
        ax.set_xlabel(column, fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        stats_text = f"Mean: {data.mean():.2f}\nStd: {data.std():.2f}\nSkew: {data.skew():.2f}"
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                fontsize=9, family='monospace')
        
        plt.tight_layout()
        
        file_path = output_path / f"{column}_histogram.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create histogram for {column}: {e}")
        return None


def plot_numeric_boxplot(df: pd.DataFrame, column: str, output_dir: str) -> Optional[str]:
    """Enhanced boxplot for outlier detection"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        data = df[column].dropna()
        if len(data) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.boxplot(
            y=data,
            color=VizTheme.SECONDARY_COLOR,
            width=0.5,
            linewidth=2,
            ax=ax
        )
        
        # Add swarm plot for small datasets
        if len(data) < 500:
            sns.swarmplot(y=data, color=VizTheme.WARNING_COLOR, alpha=0.5, size=3, ax=ax)
        
        ax.set_title(f"{column} - Boxplot (Outlier Detection)", fontsize=14, weight="bold", pad=20)
        ax.set_ylabel(column, fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add statistics
        q1, q2, q3 = data.quantile([0.25, 0.5, 0.75])
        stats_text = f"Q1: {q1:.2f}\nMedian: {q2:.2f}\nQ3: {q3:.2f}\nIQR: {q3-q1:.2f}"
        ax.text(1.15, 0.5, stats_text, transform=ax.transAxes,
                verticalalignment='center', fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        plt.tight_layout()
        
        file_path = output_path / f"{column}_boxplot.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create boxplot for {column}: {e}")
        return None


def plot_numeric_violin(df: pd.DataFrame, column: str, output_dir: str) -> Optional[str]:
    """Violin plot for distribution shape"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        data = df[column].dropna()
        if len(data) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.violinplot(y=data, color=VizTheme.ACCENT_COLOR, ax=ax)
        
        ax.set_title(f"{column} - Distribution Shape", fontsize=14, weight="bold", pad=20)
        ax.set_ylabel(column, fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        file_path = output_path / f"{column}_violin.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create violin plot for {column}: {e}")
        return None


# =========================================================================
# Enhanced Categorical Visualizations
# =========================================================================

def plot_categorical_barplot(df: pd.DataFrame, column: str, output_dir: str, top_n: int = 10) -> Optional[str]:
    """Enhanced barplot for categorical data"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        value_counts = df[column].value_counts().head(top_n)
        
        if len(value_counts) == 0:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.barh(range(len(value_counts)), value_counts.values, color=VizTheme.PRIMARY_COLOR, edgecolor='black')
        ax.set_yticks(range(len(value_counts)))
        ax.set_yticklabels([str(x)[:30] for x in value_counts.index])
        
        ax.set_title(f"{column} - Top {top_n} Categories", fontsize=14, weight="bold", pad=20)
        ax.set_xlabel("Count", fontsize=11)
        ax.set_ylabel(column, fontsize=11)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value labels on bars
        for i, (bar, val) in enumerate(zip(bars, value_counts.values)):
            ax.text(val, i, f" {val} ({val/len(df)*100:.1f}%)", va='center', fontsize=9)
        
        plt.tight_layout()
        
        file_path = output_path / f"{column}_barplot.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create barplot for {column}: {e}")
        return None


# =========================================================================
# Correlation Visualizations
# =========================================================================

def plot_correlation_heatmap(df: pd.DataFrame, numeric_cols: List[str], output_dir: str) -> Optional[str]:
    """Correlation heatmap for numeric columns"""
    
    try:
        if len(numeric_cols) < 2:
            return None
        
        output_path = ensure_output_dir(output_dir)
        
        corr_data = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(max(10, len(numeric_cols)), max(8, len(numeric_cols)-1)))
        
        sns.heatmap(
            corr_data,
            annot=True,
            fmt='.2f',
            cmap='RdYlGn',
            center=0,
            vmin=-1, vmax=1,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        
        ax.set_title("Correlation Matrix - Numeric Columns", fontsize=14, weight="bold", pad=20)
        plt.tight_layout()
        
        file_path = output_path / "correlation_heatmap.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create correlation heatmap: {e}")
        return None


def plot_missing_heatmap(df: pd.DataFrame, output_dir: str) -> Optional[str]:
    """Heatmap showing missing data patterns"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        missing = df.isnull().astype(int)
        
        if missing.sum().sum() == 0:
            return None  # No missing data
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        sns.heatmap(
            missing,
            cbar=True,
            cmap=['#2ecc71', '#e74c3c'],
            yticklabels=False,
            xticklabels=True,
            ax=ax
        )
        
        ax.set_title("Missing Data Pattern", fontsize=14, weight="bold", pad=20)
        ax.set_xlabel("Columns", fontsize=11)
        ax.set_ylabel("Rows", fontsize=11)
        
        plt.tight_layout()
        
        file_path = output_path / "missing_data_heatmap.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create missing data heatmap: {e}")
        return None


# =========================================================================
# Advanced Visualizations
# =========================================================================

def plot_pairplot(df: pd.DataFrame, numeric_cols: List[str], output_dir: str) -> Optional[str]:
    """Pairplot for relationships between numeric columns"""
    
    try:
        if len(numeric_cols) < 2 or len(numeric_cols) > 5:
            return None
        
        output_path = ensure_output_dir(output_dir)
        
        pairplot = sns.pairplot(
            df[numeric_cols].dropna(),
            diag_kind='kde',
            plot_kws={'alpha': 0.6, 's': 20}
        )
        
        pairplot.fig.suptitle("Pairplot - Numeric Relationships", fontsize=14, weight="bold", y=1.001)
        
        file_path = output_path / "pairplot.png"
        pairplot.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create pairplot: {e}")
        return None


# =========================================================================
# Summary Statistics Visualization
# =========================================================================

def plot_summary_statistics(df: pd.DataFrame, numeric_cols: List[str], output_dir: str) -> Optional[str]:
    """Summary statistics visualization"""
    
    try:
        if len(numeric_cols) == 0:
            return None
        
        output_path = ensure_output_dir(output_dir)
        
        # Get summary stats
        stats_df = df[numeric_cols].describe().T
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Mean
        axes[0, 0].barh(stats_df.index, stats_df['mean'], color=VizTheme.PRIMARY_COLOR)
        axes[0, 0].set_title('Mean Values', weight='bold')
        axes[0, 0].set_xlabel('Value')
        
        # Std Dev
        axes[0, 1].barh(stats_df.index, stats_df['std'], color=VizTheme.SECONDARY_COLOR)
        axes[0, 1].set_title('Standard Deviation', weight='bold')
        axes[0, 1].set_xlabel('Value')
        
        # Min
        axes[1, 0].barh(stats_df.index, stats_df['min'], color=VizTheme.ACCENT_COLOR)
        axes[1, 0].set_title('Minimum Values', weight='bold')
        axes[1, 0].set_xlabel('Value')
        
        # Max
        axes[1, 1].barh(stats_df.index, stats_df['max'], color=VizTheme.WARNING_COLOR)
        axes[1, 1].set_title('Maximum Values', weight='bold')
        axes[1, 1].set_xlabel('Value')
        
        plt.suptitle('Summary Statistics', fontsize=14, weight='bold', y=1.00)
        plt.tight_layout()
        
        file_path = output_path / "summary_statistics.png"
        plt.savefig(file_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create summary statistics plot: {e}")
        return None
