# 🧠 AI Data Analyst Agent

A deterministic, modular data analysis engine that performs structured EDA before introducing AI-based reasoning.

This project is being built phase-by-phase to simulate a production-grade data analysis system.

---

## 📌 Project Goal

Upload any dataset →  
System performs:

- Data validation
- Structured EDA
- Quality diagnostics
- Correlation analysis
- (Upcoming) Visualization engine
- (Upcoming) AI-powered insight explanations

---

# ✅ Phase 1 – Data Ingestion & Validation (Completed)

Implemented:

- CSV / Excel loading with error handling
- Schema inspection (rows, columns, dtype, nulls, uniqueness)
- Data quality checks:
  - High missing value detection
  - Constant column detection
  - ID-like column detection
  - String-date detection

Tested on:
- Superstore dataset
- HR Attrition dataset
- Consumer Complaints dataset

---

# ✅ Phase 2 – Core EDA Engine (Completed)

Implemented:

- Column type separation (numeric vs categorical)
- Numeric summary statistics
- Categorical summary (top values + cardinality)
- High-cardinality detection
- Duplicate row detection
- Numeric-only correlation analysis with threshold filtering

All computations are deterministic and reproducible.

No transformations or AI reasoning yet.

---

# 📁 Project Structure

