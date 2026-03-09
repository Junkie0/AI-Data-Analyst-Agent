# AI Data Analyst Agent

> Automated Exploratory Data Analysis Engine with Adaptive Insights Generation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🎯 Overview

A deterministic, end-to-end data analysis engine that takes raw datasets and produces:

- **Phase 1-2**: Automatic data ingestion + schema inference
- **Phase 3**: Comprehensive exploratory data analysis
- **Phase 3.5**: Professional visualizations (20+ plot types)
- **Phase 4**: Adaptive insight generation (14 insight types)
- **Phase 5**: Natural language reports (5-section narrative)

No machine learning models, no LLMs—just pure statistical analysis with intelligent thresholds.

## ✨ Features

### 📊 Data Processing

- **Robust CSV/Excel Loading** - Automatic encoding detection (UTF-8, Latin-1, etc.)
- **Schema Inference** - 8-type classification (numeric, categorical, datetime, binary, ordinal, identifier, constant, string)
- **Automatic Validation** - Data quality checks built-in

### 📈 Analysis & Insights

- **EDA Engine** - Numeric summaries (mean, std, min, max, skewness, kurtosis)
- **14 Insight Types**:
  - Distribution analysis (skewness, kurtosis)
  - Correlation detection (Pearson)
  - Categorical imbalance (entropy-based)
  - Missing data patterns
  - Cardinality issues
  - Outlier detection
  - Duplicate analysis
  - Quality metrics
- **Adaptive Thresholds** - Adjusts to dataset characteristics

### 🎨 Visualizations (8 Function Types)

- **Histograms** + KDE with statistics overlay
- **Boxplots** + outlier swarm plots
- **Violin Plots** - Distribution shape analysis
- **Barplots** - Categorical frequencies with percentages
- **Correlation Heatmap** - Diverging RdYlGn colormap
- **Pairplots** - Relationship exploration
- **Missing Data Heatmap** - Pattern detection
- **Summary Statistics** - 4-panel overview

### 📄 Reporting

- **Executive Summary** - Dataset shape, quality score, key metrics
- **Key Findings** - High-priority insights ranked by severity
- **Data Quality Assessment** - Issues and recommendations
- **Recommendations** - Top 5 actionable items
- **Detailed Analysis** - Complete insight breakdown

### 🔧 Production Features

- **CLI Tool** - `ai-analyst` command with 4 modes
- **Batch Processing** - Recursive directory analysis
- **Config System** - YAML-based adaptive thresholds
- **Clean Architecture** - Modular 5-phase pipeline
- **Error Handling** - UTF-8 safe, robust exception handling

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Junkie0/ai-data-analyst-agent.git
cd ai-data-analyst-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .
```

### Usage

#### Option 1: Command Line

```bash
# Single file analysis
ai-analyst analyze data/sample.csv --verbose --print-report

# Batch processing
ai-analyst batch data/datasets/ --recursive

# Quick validation
ai-analyst validate data/file.csv

# Show version
ai-analyst version
```

#### Option 2: Python API

```python
from src.core.pipeline import AnalysisPipeline

# Run analysis
pipeline = AnalysisPipeline()
results = pipeline.run('data/sample.csv', dataset_name='My Dataset')

# Access results
print(f"Insights: {results['insights']['count']}")
print(f"Visualizations: {results['visualizations']['total_plots_generated']}")
print(f"Report: {results['report']}")
```

## 📊 Example Output

### Superstore Dataset Test (9,994 rows × 21 columns)

```
✓ Phase 1-2: Ingestion & Schema Inference
✓ Phase 3: EDA (4 numeric, 9 categorical columns)
✓ Phase 3.5: Visualization (20 PNG files generated)
✓ Phase 4: Insights (16 insights: 6 HIGH, 10 MEDIUM)
✓ Phase 5: Reports (5-section natural language report)

Execution Time: 34.3 seconds
Output: outputs/analysis/superstore_clean/20260308_234702/
```

### Visualizations Generated

- 4 × Histograms (with KDE + statistics)
- 4 × Boxplots (with outlier detection)
- 4 × Violin plots (distribution shape)
- 5 × Barplots (categorical analysis)
- 1 × Correlation heatmap
- 1 × Pairplot
- 1 × Summary statistics

### Key Insights Found

```
⚡ HIGH PRIORITY ISSUES:
  1. Skewed Distribution: Sales (skewness: 12.97)
  2. Heavy Tails: Sales (kurtosis: 305.16)
  3. Skewed Distribution: Quantity
  4. Skewed Distribution: Discount
  5. Skewed Distribution: Profit
  6. Heavy Tails: Profit

ℹ️ MEDIUM PRIORITY ISSUES:
  → High Cardinality: Row ID, Order ID, Sales
  → Imbalanced Categories: Ship Mode, Segment, Category
  → Constant Column: Country
```

## 🏗️ Architecture

### 5-Phase Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│ DATA INGESTION LAYER (Phase 1-2)                            │
├─────────────────────────────────────────────────────────────┤
│ • DataLoader: CSV/Excel loading with encoding detection     │
│ • Schema Inference: 8-type classification                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ ANALYSIS ENGINE (Phase 3)                                   │
├─────────────────────────────────────────────────────────────┤
│ • Numeric Summary: stats, skewness, kurtosis               │
│ • Categorical Summary: unique values, top categories        │
│ • Correlation Analysis: Pearson correlations               │
│ • Duplicate Detection: exact duplicates                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ VISUALIZATION ENGINE (Phase 3.5)                            │
├─────────────────────────────────────────────────────────────┤
│ • VisualizationOrchestrator: Manages all 8 plot types      │
│ • Enhanced Plots: Statistics, colors, formatting            │
│ • Output: 20+ professional PNG files per dataset            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ INSIGHT ENGINE (Phase 4)                                    │
├─────────────────────────────────────────────────────────────┤
│ • InsightEngine: 14 insight detection methods               │
│ • Adaptive Thresholds: Based on data characteristics        │
│ • Severity Assignment: Critical → High → Medium → Low       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ REPORTING ENGINE (Phase 5)                                  │
├─────────────────────────────────────────────────────────────┤
│ • ReportWriter: Natural language generation                 │
│ • 5-Section Reports: Executive summary, findings, etc.      │
│ • JSON + TXT output: Structured data + readable reports     │
└─────────────────────────────────────────────────────────────┘
```

### Module Structure

```
ai_data_analyst/
├── cli.py                 # Click-based CLI interface
├── __init__.py

src/
├── core/
│   └── pipeline.py        # Main orchestration
├── ingestion/
│   └── loader.py          # CSV/Excel loading
├── schema/
│   └── inference2.py      # Type inference
├── eda/
│   └── basic_eda.py       # Statistical analysis
├── insights/
│   ├── insight_engine.py  # Insight generation
│   └── insight_types.py   # 14 insight definitions
├── reporting/
│   ├── report_writer.py   # Report generation
│   └── __init__.py
├── visualization/
│   ├── plots.py           # 8 visualization functions
│   ├── orchestrator.py    # Visualization manager
│   └── __init__.py

config/
├── default.yaml           # Configuration template
└── loader.py              # Config loading

tests/
├── test_*.py              # Unit tests
└── demo.py                # Integration demo
```

## 📋 Configuration

Edit `config/default.yaml` to customize:

```yaml
# Pipeline Phases
phases:
  ingestion: true
  schema: true
  eda: true
  visualization: true
  insights: true
  reporting: true

# Visualization Settings
viz_output_dir: outputs/visualizations

# Insight Thresholds (Adaptive)
thresholds:
  skewness_high: 1.0
  kurtosis_high: 3.0
  correlation_strong: 0.7
  cardinality_ratio: 0.9
  missing_ratio: 0.5
```

## 📦 Dependencies

### Core Dependencies

- **pandas** ≥ 1.3.0 - Data manipulation
- **scipy** ≥ 1.7.0 - Statistical analysis
- **numpy** ≥ 1.20.0 - Numerical computing
- **matplotlib** ≥ 3.4.0 - Visualization base
- **seaborn** ≥ 0.11.0 - Enhanced statistical plots
- **click** ≥ 8.0.0 - CLI framework
- **openpyxl** ≥ 3.7.0 - Excel support

### Development Dependencies (Optional)

```bash
pip install -e ".[dev]"  # pytest, black, flake8, mypy
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Run specific test
pytest tests/test_complete_pipeline.py -v
```

## 📊 Performance Benchmark

| Dataset             | Rows    | Columns | Time | Visualizations | Insights |
| ------------------- | ------- | ------- | ---- | -------------- | -------- |
| Consumer Complaints | 555,957 | 18      | 45s  | 22             | 10       |
| HR Attrition        | 1,470   | 35      | 8s   | 18             | 38       |
| Superstore          | 9,994   | 21      | 34s  | 20             | 16       |
| Rideshare           | 1,000   | 12      | 6s   | 15             | 14       |

## 🔒 Security & Privacy

- ✓ No data transmission (runs locally)
- ✓ No API calls (fully self-contained)
- ✓ No persistent storage of data (outputs only)
- ✓ UTF-8 safe for all character encodings
- ✓ Error handling with graceful degradation

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact & Support

For issues, questions, or suggestions:

- Open an Issue on GitHub
- Check existing documentation in `PHASE*.md` files
- Review `all_the_changes_i_did.txt` for technical details

## 🎓 Learning Resources

- **PHASE1_SUMMARY.md** - Phases 1-3 architecture
- **PHASE5_ARCHITECTURE_SUMMARY.md** - Production system design
- **all_the_changes_i_did.txt** - Complete technical changelog

## 🚀 Roadmap

- [ ] Real-time dashboard UI (Streamlit)
- [ ] Advanced ML-based anomaly detection
- [ ] Custom insight plugins system
- [ ] Data quality scoring enhancements
- [ ] Integration with BI tools (Tableau, Power BI)
- [ ] Cloud deployment (AWS, GCP, Azure)

## 🏆 Key Achievements

✓ Complete 5-phase automated analysis engine
✓ 20+ professional visualizations per dataset
✓ Adaptive insight generation (14 types)
✓ Production-grade CLI + packaging
✓ Tested on 4+ diverse datasets
✓ <45 seconds per analysis (even large datasets)
✓ 100% deterministic (no randomness)
✓ UTF-8 safe across platforms

---

**Built with ❤️ for data professionals**
