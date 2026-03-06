# 🧠 AI Data Analyst Agent

A deterministic, modular **data analysis engine** that performs automated **data validation, structured EDA, and visualization** before introducing AI-based reasoning.

This project is being built **phase-by-phase** to simulate a **production-grade data analysis system** similar to internal analytics tools used by data teams.

---

# 📌 Project Goal

Upload any dataset →

The system automatically performs:

- Data validation
- Schema inference
- Structured EDA
- Data quality diagnostics
- Correlation analysis
- Automated visualization generation
- *(Upcoming)* AI-powered insight explanations
- *(Upcoming)* Natural language reports

---

# ✅ Phase 1 – Data Ingestion & Validation (Completed)

### Data Loading

- CSV / Excel loading with robust error handling
- Encoding fallback handling
- Empty dataset detection

### Data Validation

- Schema inspection
- Row and column counts
- Data type inspection
- Missing value analysis
- Column uniqueness analysis

### Data Quality Checks

- High missing value detection
- Constant column detection
- ID-like column detection
- String-date detection

### Tested On

- Superstore dataset
- HR Attrition dataset
- Consumer Complaints dataset

---

# ✅ Phase 2 – Core EDA Engine (Completed)

Implemented deterministic **Exploratory Data Analysis engine**.

### Schema Inference

Automatic column classification:

- Identifier
- Numeric
- Binary
- Ordinal
- Categorical
- Datetime
- Constant

Includes:

- Confidence scoring
- Ambiguity detection
- Column-level reasoning

---

### Numeric Analysis

For numeric columns:

- Mean
- Standard deviation
- Minimum / Maximum
- Quartiles
- Missing ratio

---

### Categorical Analysis

For categorical features:

- Cardinality detection
- Top value frequency
- High-cardinality detection

---

### Dataset Diagnostics

- Duplicate row detection
- Cardinality report
- Missing value analysis

---

### Correlation Analysis

- Pearson correlation matrix
- Numeric-only correlation analysis
- Strong correlation detection using threshold filtering

Example strong correlations detected:

```

('Eminem', 'K_Lamar'): 0.733
('Nirvana', 'Linkin_Park'): 0.72

```

All computations are **deterministic and reproducible**.

No transformations or AI reasoning are applied yet.

---

# ✅ Phase 3 – Visualization Engine (Completed)

Automated visualization generation based on inferred schema.

### Supported Visualizations

**Numeric Columns**

- Histogram (distribution analysis)
- Boxplot (outlier detection)

**Categorical Columns**

- Barplots for top categories

**Dataset-Level Analysis**

- Correlation heatmap

---

### Visualization Features

- Automatic plot selection based on schema
- Clean visual styling
- Organized output directory generation
- Schema-driven column filtering

Generated plots are automatically saved in:

```

outputs/plots/run_timestamp/

```

Example visual outputs include:

- Distribution plots
- Outlier detection plots
- Correlation heatmaps

---

# 📁 Project Structure

```

AI-Data-Analyst-Agent
│
├── data
│   └── sample
│
├── outputs
│   └── plots
│
├── src
│   ├── ingestion
│   │   └── loader.py
│   │
│   ├── schema
│   │   ├── inference.py (testing phase)
│   │   └── inference2.py
│   │
│   ├── validation
│   │   ├── schema.py
│   │   └── quality_checks.py
│   │
│   ├── eda
│   │   └── basic_eda.py
│   │
│   └── visualization
│       ├── auto_viz.py
│       └── plots.py
│
├── tests
│   ├── test_schema_v2.py
│   ├── test_basic_eda_manual.py
│   ├── test_quality_checks_manual.py
│   └── test_visualization_manual.py
│
├── README.md
└── PHASE1_SUMMARY.md

```

---

# 🔜 Upcoming Phases

### Phase 4 — Insight Generation Engine

Automatically convert EDA outputs into **human-readable insights**.

Example:

```

Strong correlation detected between Eminem and Kendrick Lamar (r = 0.73),
suggesting overlapping hip-hop listener audiences.

```

---

### Phase 5 — Natural Language Report Generator

Generate structured reports such as:

```

Dataset Overview
Key Findings
Data Quality Issues
Correlation Insights
Distribution Observations

```

---

### Phase 6 — Queryable Data Analyst Agent

Users will be able to ask:

```

Which features are highly correlated?
Which columns contain missing values?
Which variables have strong outliers?

```

---

# 🎯 Project Vision

The final system will function as an **AI-powered Data Analyst Agent** capable of:

- Understanding datasets automatically
- Performing structured EDA
- Generating visualizations
- Producing human-readable insights
- Answering analytical questions about the dataset

---

# 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Seaborn
- Matplotlib

---

# 📊 Current Status

| Phase | Status |
|------|------|
| Phase 1 – Ingestion & Validation | ✅ Completed |
| Phase 2 – Core EDA Engine | ✅ Completed |
| Phase 3 – Visualization Engine | ✅ Completed |
| Phase 4 – Insight Generator | 🔜 Upcoming |
| Phase 5 – Report Generator | 🔜 Upcoming |

---

# 📌 Author

**Anurag Potdar**

Building systems that combine **data engineering, analytics, and AI reasoning**.
