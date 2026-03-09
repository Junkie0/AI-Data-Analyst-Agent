from datetime import datetime
from pathlib import Path
from src.visualization.plots import (
    plot_numeric_histogram,
    plot_numeric_boxplot,
    plot_categorical_barplot,
    plot_correlation_heatmap,
    get_visualization_columns
)

def generate_visualizations(df, schema):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("outputs/plots") / f"run_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    viz_cols = get_visualization_columns(schema)

    numeric_columns = viz_cols["numeric"]
    categorical_columns = viz_cols["categorical"]

    results = {
        "histograms": [],
        "boxplots": [],
        "barplots": [],
        "heatmap": None
    }

    # Numeric plots
    for col in numeric_columns[:5]:
        hist = plot_numeric_histogram(df, col, output_dir)
        box = plot_numeric_boxplot(df, col, output_dir)

        results["histograms"].append(hist)
        results["boxplots"].append(box)

    # Categorical plots
    for col in categorical_columns[:5]:
        bar = plot_categorical_barplot(df, col, output_dir)

        if bar:
            results["barplots"].append(bar)

    # Correlation heatmap
    heatmap = plot_correlation_heatmap(df, numeric_columns, output_dir)

    results["heatmap"] = heatmap

    return results