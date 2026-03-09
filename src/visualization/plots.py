import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

# ---------------------------------------------------
# Theme Configuration (Green-Yellow Style)
# ---------------------------------------------------

sns.set_theme(style="whitegrid")

GREEN = "#2ecc71"
DARK_GREEN = "#27ae60"
YELLOW = "#f1c40f"
LIGHT_YELLOW = "#f9e79f"
BLUE = "#3498db"
RED = "#e74c3c"

sns.set_palette([GREEN, YELLOW, BLUE])
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 150


# ---------------------------------------------------
# Output Directory
# ---------------------------------------------------

def ensure_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------
# Schema-Based Column Selection
# ---------------------------------------------------

def get_visualization_columns(schema: dict) -> dict:

    summary = schema["summary"]

    return {
        "numeric": summary["numeric"] + summary["ordinal"],
        "categorical": summary["categorical"] + summary["binary"],
        "datetime": summary["datetime"]
    }


# ---------------------------------------------------
# Numeric Histogram
# ---------------------------------------------------

def plot_numeric_histogram(
        df: pd.DataFrame,
        column: str,
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """Enhanced histogram with KDE and statistics"""

    try:
        output_path = ensure_output_dir(output_dir)
        data = df[column].dropna()
        
        if len(data) == 0:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.histplot(
            data,
            kde=True,
            color=GREEN,
            edgecolor="black",
            alpha=0.7,
            ax=ax
        )

        ax.set_title(f"{column} - Distribution", fontsize=14, weight="bold", pad=15)
        ax.set_xlabel(column, fontsize=11)
        ax.set_ylabel("Frequency", fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Add statistics box
        stats_text = f"Mean: {data.mean():.2f}\nStd: {data.std():.2f}\nSkew: {data.skew():.2f}"
        ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
                fontsize=9, family='monospace')

        plt.tight_layout()
        file_path = output_path / f"{column}_histogram.png"
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create histogram for {column}: {e}")
        return None


# ---------------------------------------------------
# Numeric Boxplot
# ---------------------------------------------------

def plot_numeric_boxplot(
        df: pd.DataFrame,
        column: str,
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """Enhanced boxplot with quartile annotations"""

    try:
        output_path = ensure_output_dir(output_dir)
        data = df[column].dropna()
        
        if len(data) == 0:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.boxplot(
            y=data,
            color=YELLOW,
            width=0.4,
            fliersize=5,
            linewidth=1.5,
            ax=ax
        )
        
        # Add swarm plot for small datasets
        if len(data) < 500:
            sns.swarmplot(y=data, color=RED, alpha=0.4, size=3, ax=ax)

        ax.set_title(f"{column} - Outlier Detection", fontsize=14, weight="bold", pad=15)
        ax.set_ylabel(column, fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add quartile statistics
        q1, q2, q3 = data.quantile([0.25, 0.5, 0.75])
        stats_text = f"Q1: {q1:.2f}\nMedian: {q2:.2f}\nQ3: {q3:.2f}\nIQR: {q3-q1:.2f}"
        ax.text(1.15, 0.5, stats_text, transform=ax.transAxes,
                verticalalignment='center', fontsize=9, family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        plt.tight_layout()
        file_path = output_path / f"{column}_boxplot.png"
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create boxplot for {column}: {e}")
        return None


# ---------------------------------------------------
# Categorical Bar Plot
# ---------------------------------------------------

def plot_categorical_barplot(
        df: pd.DataFrame,
        column: str,
        output_dir: str = "outputs/plots",
        top_n: int = 10
) -> Optional[str]:
    """Enhanced barplot with percentage labels"""

    try:
        output_path = ensure_output_dir(output_dir)
        value_counts = df[column].value_counts(dropna=False).head(top_n)
        
        if len(value_counts) == 0:
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.barh(range(len(value_counts)), value_counts.values, 
                        color=GREEN, edgecolor='black', alpha=0.8)
        ax.set_yticks(range(len(value_counts)))
        ax.set_yticklabels([str(x)[:30] for x in value_counts.index])

        ax.set_title(f"Top {top_n} Categories - {column}", fontsize=14, weight="bold", pad=15)
        ax.set_xlabel("Count", fontsize=11)
        ax.set_ylabel(column, fontsize=11)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add value and percentage labels
        total = len(df)
        for i, (bar, val) in enumerate(zip(bars, value_counts.values)):
            pct = (val / total) * 100
            ax.text(val, i, f" {val} ({pct:.1f}%)", va='center', fontsize=9, weight='bold')

        plt.tight_layout()
        file_path = output_path / f"{column}_barplot.png"
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create barplot for {column}: {e}")
        return None


# ---------------------------------------------------
# Correlation Heatmap
# ---------------------------------------------------

def plot_correlation_heatmap(
        df: pd.DataFrame,
        numeric_cols: List[str],
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """Enhanced correlation heatmap"""

    try:
        if len(numeric_cols) < 2:
            return None

        output_path = ensure_output_dir(output_dir)
        corr = df[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(max(10, len(numeric_cols)), max(8, len(numeric_cols)-1)))

        sns.heatmap(
            corr,
            cmap="RdYlGn",
            center=0,
            vmin=-1, vmax=1,
            annot=True,
            fmt=".2f",
            linewidths=0.5,
            linecolor="white",
            square=True,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )

        ax.set_title("Correlation Matrix - Numeric Columns", fontsize=14, weight="bold", pad=15)
        plt.tight_layout()

        file_path = output_path / "correlation_heatmap.png"
        plt.savefig(file_path, bbox_inches="tight")
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create correlation heatmap: {e}")
        return None


# ---------------------------------------------------
# Advanced Visualizations (Optional)
# ---------------------------------------------------

def plot_numeric_violin(
        df: pd.DataFrame,
        column: str,
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """Violin plot for distribution shape analysis"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        data = df[column].dropna()
        
        if len(data) < 3:
            return None

        fig, ax = plt.subplots(figsize=(8, 6))
        
        sns.violinplot(y=data, color=BLUE, linewidth=1.5, ax=ax)
        
        ax.set_title(f"{column} - Distribution Shape", fontsize=14, weight="bold", pad=15)
        ax.set_ylabel(column, fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        file_path = output_path / f"{column}_violin.png"
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create violin plot for {column}: {e}")
        return None


def plot_missing_heatmap(
        df: pd.DataFrame,
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """Heatmap showing missing data patterns"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        missing = df.isnull().astype(int)
        if missing.sum().sum() == 0:
            return None  # No missing data

        fig, ax = plt.subplots(figsize=(12, max(6, len(df.columns)//2)))
        
        sns.heatmap(
            missing.T,
            cmap='RdYlGn_r',
            cbar_kws={'label': 'Missing (1) vs Present (0)'},
            ax=ax
        )
        
        ax.set_title('Missing Data Patterns', fontsize=14, weight='bold', pad=15)
        ax.set_xlabel('Row Index', fontsize=11)
        ax.set_ylabel('Columns', fontsize=11)

        plt.tight_layout()
        file_path = output_path / 'missing_data_heatmap.png'
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create missing data heatmap: {e}")
        return None


def plot_pairplot(
        df: pd.DataFrame,
        numeric_cols: List[str],
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """Pairplot for relationships between numeric columns"""
    
    try:
        if len(numeric_cols) < 2:
            return None

        output_path = ensure_output_dir(output_dir)
        
        plot_df = df[numeric_cols].dropna()
        if len(plot_df) == 0:
            return None

        g = sns.pairplot(plot_df, diag_kind='hist', plot_kws={'alpha': 0.6, 's': 20})
        
        for ax in g.axes.flat:
            ax.set_facecolor('#f8f9fa')

        file_path = output_path / 'pairplot.png'
        g.savefig(file_path, bbox_inches='tight', dpi=150)
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create pairplot: {e}")
        return None


def plot_summary_statistics(
        df: pd.DataFrame,
        numeric_cols: List[str],
        output_dir: str = "outputs/plots"
) -> Optional[str]:
    """4-panel summary statistics visualization"""
    
    try:
        output_path = ensure_output_dir(output_dir)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Panel 1: Mean values
        means = df[numeric_cols].mean().sort_values(ascending=False)
        axes[0, 0].barh(means.index, means.values, color=GREEN, edgecolor='black')
        axes[0, 0].set_title('Mean Values', fontsize=12, weight='bold')
        axes[0, 0].set_xlabel('Value')
        
        # Panel 2: Standard Deviation
        stds = df[numeric_cols].std().sort_values(ascending=False)
        axes[0, 1].barh(stds.index, stds.values, color=YELLOW, edgecolor='black')
        axes[0, 1].set_title('Standard Deviation', fontsize=12, weight='bold')
        axes[0, 1].set_xlabel('Std Dev')
        
        # Panel 3: Min values
        mins = df[numeric_cols].min().sort_values()
        axes[1, 0].barh(mins.index, mins.values, color=BLUE, edgecolor='black')
        axes[1, 0].set_title('Minimum Values', fontsize=12, weight='bold')
        axes[1, 0].set_xlabel('Value')
        
        # Panel 4: Max values
        maxs = df[numeric_cols].max().sort_values(ascending=False)
        axes[1, 1].barh(maxs.index, maxs.values, color=RED, edgecolor='black')
        axes[1, 1].set_title('Maximum Values', fontsize=12, weight='bold')
        axes[1, 1].set_xlabel('Value')
        
        fig.suptitle('Statistical Summary', fontsize=16, weight='bold', y=0.995)
        plt.tight_layout()

        file_path = output_path / 'summary_statistics.png'
        plt.savefig(file_path, bbox_inches='tight')
        plt.close()

        return str(file_path)
    
    except Exception as e:
        print(f"Warning: Could not create summary statistics: {e}")
        return None


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def get_visualization_columns(schema: Dict) -> Dict[str, List[str]]:
    """Extract numeric and categorical columns from schema"""
    
    numeric = []
    categorical = []
    
    # Handle schema format: {type: [col1, col2, ...]}
    if isinstance(schema, dict):
        # Check if schema has 'summary' key (old format)
        if 'summary' in schema:
            schema_data = schema['summary']
        else:
            schema_data = schema
        
        # New format with type-based lists
        numeric.extend(schema_data.get('numeric', []))
        numeric.extend(schema_data.get('float', []))
        numeric.extend(schema_data.get('int', []))
        numeric.extend(schema_data.get('integer', []))
        
        categorical.extend(schema_data.get('categorical', []))
        categorical.extend(schema_data.get('ordinal', []))
        categorical.extend(schema_data.get('binary', []))
        categorical.extend(schema_data.get('string', []))
    
    # Remove duplicates while preserving order
    seen_numeric = set()
    unique_numeric = []
    for col in numeric:
        if col not in seen_numeric:
            seen_numeric.add(col)
            unique_numeric.append(col)
    
    seen_categorical = set()
    unique_categorical = []
    for col in categorical:
        if col not in seen_categorical:
            seen_categorical.add(col)
            unique_categorical.append(col)
    
    return {'numeric': unique_numeric, 'categorical': unique_categorical}