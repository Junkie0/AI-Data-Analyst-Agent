"""
Insight Type Definitions

Structured definitions for different types of insights
that can be automatically generated from EDA data.
"""

from typing import Any, Dict, List
from dataclasses import dataclass


@dataclass
class Insight:
    """Base insight structure"""
    type: str
    severity: str  # low, medium, high
    column: str
    title: str
    description: str
    value: Any
    context: Dict[str, Any]


class InsightTypes:
    """Insight type constants and validators"""
    
    # Distribution insights
    SKEWED_DISTRIBUTION = "skewed_distribution"
    HIGH_KURTOSIS = "high_kurtosis"
    BIMODAL_DISTRIBUTION = "bimodal_distribution"
    
    # Correlation insights
    STRONG_POSITIVE_CORRELATION = "strong_positive_correlation"
    STRONG_NEGATIVE_CORRELATION = "strong_negative_correlation"
    
    # Categorical insights
    HIGH_CARDINALITY = "high_cardinality"
    IMBALANCED_CATEGORIES = "imbalanced_categories"
    LOW_CARDINALITY = "low_cardinality"
    
    # Missing data insights
    HIGH_MISSING_VALUES = "high_missing_values"
    MISSING_PATTERN = "missing_pattern"
    
    # Data quality insights
    CONSTANT_COLUMN = "constant_column"
    DUPLICATE_ROWS = "duplicate_rows"
    
    # Statistical insights
    OUTLIERS_DETECTED = "outliers_detected"
    UNUSUAL_RANGE = "unusual_range"
    
    ALL_TYPES = {
        SKEWED_DISTRIBUTION,
        HIGH_KURTOSIS,
        BIMODAL_DISTRIBUTION,
        STRONG_POSITIVE_CORRELATION,
        STRONG_NEGATIVE_CORRELATION,
        HIGH_CARDINALITY,
        IMBALANCED_CATEGORIES,
        LOW_CARDINALITY,
        HIGH_MISSING_VALUES,
        MISSING_PATTERN,
        CONSTANT_COLUMN,
        DUPLICATE_ROWS,
        OUTLIERS_DETECTED,
        UNUSUAL_RANGE
    }


class SeverityLevels:
    """Severity level definitions"""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    # Severity order for sorting
    ORDER = {CRITICAL: 4, HIGH: 3, MEDIUM: 2, LOW: 1}


# Thresholds for adaptive insight generation
ADAPTIVE_THRESHOLDS = {
    # Skewness: |skew| > 1 is considered highly skewed
    "skewness_high": 1.0,
    "skewness_moderate": 0.5,
    
    # Kurtosis: Fisher's definition, excess kurtosis > 3 is heavy-tailed
    "kurtosis_high": 3.0,
    "kurtosis_moderate": 1.0,
    
    # Cardinality: unique_ratio thresholds
    "high_cardinality_ratio": 0.95,
    "low_cardinality_ratio": 0.05,
    
    # Missing data: ratio threshold
    "high_missing_ratio": 0.3,
    "moderate_missing_ratio": 0.1,
    
    # Category imbalance: entropy-based
    "imbalance_threshold": 0.5,  # normalized entropy
    
    # Correlation
    "correlation_very_strong": 0.85,
    "correlation_strong": 0.7,
    "correlation_moderate": 0.5,
}
