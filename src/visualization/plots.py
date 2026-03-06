import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------
# Theme Configuration (Green-Yellow Style)
# ---------------------------------------------------

sns.set_theme(style="whitegrid")

GREEN = "#2ecc71"
DARK_GREEN = "#27ae60"
YELLOW = "#f1c40f"
LIGHT_YELLOW = "#f9e79f"

sns.set_palette([GREEN, YELLOW])


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
):

    output_path = ensure_output_dir(output_dir)

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df[column].dropna(),
        kde=True,
        color=GREEN,
        edgecolor="black",
        alpha=0.8
    )

    plt.title(f"{column} Distribution", fontsize=14, weight="bold")
    plt.xlabel(column, fontsize=11)
    plt.ylabel("Frequency", fontsize=11)

    plt.tight_layout()

    file_path = output_path / f"{column}_histogram.png"

    plt.savefig(file_path)
    plt.close()

    return str(file_path)


# ---------------------------------------------------
# Numeric Boxplot
# ---------------------------------------------------

def plot_numeric_boxplot(
        df: pd.DataFrame,
        column: str,
        output_dir: str = "outputs/plots"
):

    output_path = ensure_output_dir(output_dir)

    plt.figure(figsize=(6, 4))

    sns.boxplot(
        x=df[column].dropna(),
        color=YELLOW,
        fliersize=4,
        linewidth=1.2
    )

    plt.title(f"{column} Outlier Detection", fontsize=14, weight="bold")
    plt.xlabel(column, fontsize=11)

    plt.tight_layout()

    file_path = output_path / f"{column}_boxplot.png"

    plt.savefig(file_path)
    plt.close()

    return str(file_path)


# ---------------------------------------------------
# Categorical Bar Plot
# ---------------------------------------------------

def plot_categorical_barplot(
        df: pd.DataFrame,
        column: str,
        output_dir: str = "outputs/plots",
        top_n: int = 10
):

    output_path = ensure_output_dir(output_dir)

    value_counts = df[column].value_counts(dropna=False).head(top_n)

    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=value_counts.values,
        y=value_counts.index,
        color=GREEN
    )

    plt.title(f"Top {top_n} Categories of {column}", fontsize=14, weight="bold")
    plt.xlabel("Count", fontsize=11)
    plt.ylabel(column, fontsize=11)

    plt.tight_layout()

    file_path = output_path / f"{column}_barplot.png"

    plt.savefig(file_path, bbox_inches="tight")
    plt.close()

    return str(file_path)


# ---------------------------------------------------
# Correlation Heatmap
# ---------------------------------------------------

def plot_correlation_heatmap(
        df: pd.DataFrame,
        numeric_cols,
        output_dir: str = "outputs/plots"
):

    if len(numeric_cols) < 2:
        return None

    output_path = ensure_output_dir(output_dir)

    corr = df[numeric_cols].corr()

    plt.figure(figsize=(10, 8))

    sns.heatmap(
        corr,
        cmap="YlGn",
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        linecolor="white"
    )

    plt.title("Correlation Heatmap", fontsize=15, weight="bold")

    plt.tight_layout()

    file_path = output_path / "correlation_heatmap.png"

    plt.savefig(file_path, bbox_inches="tight")
    plt.close()

    return str(file_path)