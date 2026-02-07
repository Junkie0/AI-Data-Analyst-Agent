# Phase 1 – Data Ingestion & Validation

## Implemented Checks

1. High Missing Columns
   - Flags columns with missing ratio above a configurable threshold (default 50%)
   - Useful for identifying unusable or optional fields

2. Constant Columns
   - Detects columns with a single unique value
   - Example: Country, Over18

3. ID-like Columns
   - Uses unique-value ratio heuristic
   - Correctly flags true identifiers
   - Known limitation: high-cardinality numeric columns may be falsely flagged

4. String Date Columns
   - Detects date-like columns stored as object
   - Uses coercion ratio heuristic

## Datasets Tested
- Superstore (transactional)
- HR Attrition (categorical-heavy)
- Consumer Complaints (messy, text-heavy)

## Known Limitations
- ID-like detection needs semantic refinement
- Date detection currently attempts parsing on all object columns
- CSV mixed-type warnings intentionally preserved for later analysis
