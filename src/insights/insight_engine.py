"""
Core Insight Generation Engine

Processes EDA outputs and generates adaptive insights.
Uses statistical measures to determine insight severity dynamically.
"""

import math
from typing import List, Dict, Tuple, Any
import pandas as pd
from .insight_types import (
    Insight, InsightTypes, SeverityLevels, 
    ADAPTIVE_THRESHOLDS
)
from .report_generator import ReportGenerator


class InsightEngine:
    """Main engine for generating insights from EDA results"""
    
    def __init__(self, df: pd.DataFrame = None, schema: Dict = None):
        """
        Initialize the insight engine
        
        Args:
            df: Original dataframe (optional, used for additional analysis)
            schema: Schema dictionary (optional)
        """
        self.df = df
        self.schema = schema or {}
        self.reporter = ReportGenerator()
    
    def generate_insights(self, eda_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point: Generate all insights from EDA outputs
        
        Args:
            eda_results: Dictionary containing all EDA outputs
            
        Returns:
            Dictionary with insights, natural language report, and metadata
        """
        
        insights = []
        
        # Extract insights by category
        insights.extend(self._extract_distribution_insights(eda_results))
        insights.extend(self._extract_correlation_insights(eda_results))
        insights.extend(self._extract_categorical_insights(eda_results))
        insights.extend(self._extract_missing_data_insights(eda_results))
        insights.extend(self._extract_quality_insights(eda_results))
        
        # Generate report
        report = self.reporter.generate_report(insights)
        
        return {
            "insights": report["insights"],
            "natural_language": report["natural_language"],
            "summary": report["summary"],
            "count": len(insights),
            "metadata": {
                "by_severity": self._count_by_severity(insights),
                "by_type": self._count_by_type(insights)
            }
        }
    
    # =========================================================================
    # DISTRIBUTION INSIGHTS
    # =========================================================================
    
    def _extract_distribution_insights(self, eda_results: Dict) -> List[Insight]:
        """Extract insights from numeric distributions"""
        
        insights = []
        numeric_summary = eda_results.get("numeric_summary", {})
        
        for col, stats in numeric_summary.items():
            
            # Skewness insight
            skewness = stats.get("skewness", 0)
            if abs(skewness) > ADAPTIVE_THRESHOLDS["skewness_high"]:
                severity = SeverityLevels.HIGH
                context = {"value": skewness}
            elif abs(skewness) > ADAPTIVE_THRESHOLDS["skewness_moderate"]:
                severity = SeverityLevels.MEDIUM
                context = {"value": skewness}
            else:
                severity = None
                context = {}
            
            if severity:
                insights.append(Insight(
                    type=InsightTypes.SKEWED_DISTRIBUTION,
                    severity=severity,
                    column=col,
                    title=f"Skewed Distribution: {col}",
                    description=f"Column '{col}' shows skewness of {skewness}",
                    value=skewness,
                    context=context
                ))
            
            # Kurtosis insight
            kurtosis = stats.get("kurtosis", 0)
            if kurtosis > ADAPTIVE_THRESHOLDS["kurtosis_high"]:
                severity = SeverityLevels.HIGH
                context = {"value": kurtosis}
            elif kurtosis > ADAPTIVE_THRESHOLDS["kurtosis_moderate"]:
                severity = SeverityLevels.MEDIUM
                context = {"value": kurtosis}
            else:
                severity = None
                context = {}
            
            if severity:
                insights.append(Insight(
                    type=InsightTypes.HIGH_KURTOSIS,
                    severity=severity,
                    column=col,
                    title=f"Heavy Tails: {col}",
                    description=f"Column '{col}' shows kurtosis of {kurtosis}",
                    value=kurtosis,
                    context=context
                ))
        
        return insights
    
    # =========================================================================
    # CORRELATION INSIGHTS
    # =========================================================================
    
    def _extract_correlation_insights(self, eda_results: Dict) -> List[Insight]:
        """Extract insights from correlations"""
        
        insights = []
        strong_corrs = eda_results.get("strong_correlations", {})
        
        for (col1, col2), corr_value in strong_corrs.items():
            
            # Determine severity by correlation strength
            abs_corr = abs(corr_value)
            
            if abs_corr >= ADAPTIVE_THRESHOLDS["correlation_very_strong"]:
                severity = SeverityLevels.HIGH
            elif abs_corr >= ADAPTIVE_THRESHOLDS["correlation_strong"]:
                severity = SeverityLevels.MEDIUM
            else:
                severity = SeverityLevels.LOW
            
            # Determine type
            if corr_value > 0:
                insight_type = InsightTypes.STRONG_POSITIVE_CORRELATION
            else:
                insight_type = InsightTypes.STRONG_NEGATIVE_CORRELATION
            
            insights.append(Insight(
                type=insight_type,
                severity=severity,
                column=f"{col1} × {col2}",
                title=f"Correlation: {col1} & {col2}",
                description=f"Correlation between '{col1}' and '{col2}': {corr_value}",
                value=corr_value,
                context={
                    "col1": col1,
                    "col2": col2,
                    "value": round(corr_value, 3)
                }
            ))
        
        return insights
    
    # =========================================================================
    # CATEGORICAL INSIGHTS
    # =========================================================================
    
    def _extract_categorical_insights(self, eda_results: Dict) -> List[Insight]:
        """Extract insights from categorical data"""
        
        insights = []
        
        # High cardinality - extract from cardinality_report
        cardinality = eda_results.get("cardinality_report", {})
        
        for col, card_info in cardinality.items():
            
            if isinstance(card_info, dict) and card_info.get("high_cardinality"):
                unique_ratio = card_info.get("unique_ratio", 0)
                num_unique = card_info.get("unique_count", 0)
                
                insights.append(Insight(
                    type=InsightTypes.HIGH_CARDINALITY,
                    severity=SeverityLevels.MEDIUM,
                    column=col,
                    title=f"High Cardinality: {col}",
                    description=f"Column '{col}' has {num_unique} unique values",
                    value=unique_ratio,
                    context={
                        "num_unique": num_unique,
                        "ratio": round(unique_ratio * 100, 1)
                    }
                ))
        
        # Categorical imbalance
        categorical_summary = eda_results.get("categorical_summary", {})
        for col, cat_info in categorical_summary.items():
            
            top_values = cat_info.get("top_values", {})
            if not top_values:
                continue
            
            # Get top category ratio
            total = sum(top_values.values())
            if total == 0:
                continue
            
            top_val, top_count = list(top_values.items())[0]
            top_ratio = (top_count / total) * 100
            
            # Detect imbalance (if top category > 50% and there are multiple categories)
            num_categories = cat_info.get("unique_values", 0)
            if top_ratio > 50 and num_categories > 2:
                
                # Calculate entropy to measure imbalance
                entropy = self._calculate_entropy(top_values)
                
                severity = SeverityLevels.HIGH if entropy < 0.3 else SeverityLevels.MEDIUM
                
                insights.append(Insight(
                    type=InsightTypes.IMBALANCED_CATEGORIES,
                    severity=severity,
                    column=col,
                    title=f"Imbalanced Categories: {col}",
                    description=f"Category '{top_val}' dominates {col}",
                    value=entropy,
                    context={
                        "top_cat": str(top_val),
                        "top_ratio": round(top_ratio, 1),
                        "num_categories": num_categories
                    }
                ))
        
        return insights
    
    # =========================================================================
    # MISSING DATA INSIGHTS
    # =========================================================================
    
    def _extract_missing_data_insights(self, eda_results: Dict) -> List[Insight]:
        """Extract insights from missing data patterns"""
        
        insights = []
        
        numeric_summary = eda_results.get("numeric_summary", {})
        categorical_summary = eda_results.get("categorical_summary", {})
        
        all_cols = {**numeric_summary, **categorical_summary}
        
        for col, stats in all_cols.items():
            missing_ratio = stats.get("missing_ratio", 0)
            
            if missing_ratio > ADAPTIVE_THRESHOLDS["high_missing_ratio"]:
                severity = SeverityLevels.HIGH
            elif missing_ratio > ADAPTIVE_THRESHOLDS["moderate_missing_ratio"]:
                severity = SeverityLevels.MEDIUM
            else:
                continue
            
            insights.append(Insight(
                type=InsightTypes.HIGH_MISSING_VALUES,
                severity=severity,
                column=col,
                title=f"Missing Data: {col}",
                description=f"Column '{col}' has {missing_ratio*100}% missing values",
                value=missing_ratio,
                context={
                    "missing_ratio": round(missing_ratio * 100, 1)
                }
            ))
        
        return insights
    
    # =========================================================================
    # DATA QUALITY INSIGHTS
    # =========================================================================
    
    def _extract_quality_insights(self, eda_results: Dict) -> List[Insight]:
        """Extract data quality insights"""
        
        insights = []
        
        # Constant columns
        schema = eda_results.get("summary", {})
        if isinstance(schema, dict):
            constant_cols = schema.get("constant", [])
            for col in constant_cols:
                insights.append(Insight(
                    type=InsightTypes.CONSTANT_COLUMN,
                    severity=SeverityLevels.MEDIUM,
                    column=col,
                    title=f"Constant Column: {col}",
                    description=f"Column '{col}' has no variance",
                    value=None,
                    context={}
                ))
        
        # Duplicate rows
        dup_summary = eda_results.get("duplicate_summary", {})
        if isinstance(dup_summary, dict):
            dup_ratio = dup_summary.get("duplicate_ratio", 0)
            dup_count = dup_summary.get("duplicate_rows", 0)
            
            if dup_ratio > 0:
                severity = SeverityLevels.HIGH if dup_ratio > 0.05 else SeverityLevels.MEDIUM
                
                insights.append(Insight(
                    type=InsightTypes.DUPLICATE_ROWS,
                    severity=severity,
                    column="*",
                    title="Duplicate Rows Detected",
                    description=f"Dataset contains {dup_count} duplicate rows",
                    value=dup_ratio,
                    context={
                        "dup_count": dup_count,
                        "dup_ratio": round(dup_ratio * 100, 1)
                    }
                ))
        
        return insights
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _calculate_entropy(self, value_counts: Dict[str, int]) -> float:
        """
        Calculate normalized entropy (0 to 1)
        Higher entropy = more balanced
        Lower entropy = more imbalanced
        """
        
        if not value_counts:
            return 0
        
        total = sum(value_counts.values())
        if total == 0:
            return 0
        
        # Calculate Shannon entropy
        entropy = 0
        for count in value_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        
        # Normalize by max possible entropy
        max_entropy = math.log2(len(value_counts))
        if max_entropy == 0:
            return 0
        
        normalized_entropy = entropy / max_entropy
        return round(normalized_entropy, 3)
    
    def _count_by_severity(self, insights: List[Insight]) -> Dict[str, int]:
        """Count insights by severity level"""
        
        counts = {level: 0 for level in [SeverityLevels.CRITICAL, SeverityLevels.HIGH, 
                                         SeverityLevels.MEDIUM, SeverityLevels.LOW]}
        
        for insight in insights:
            counts[insight.severity] += 1
        
        return counts
    
    def _count_by_type(self, insights: List[Insight]) -> Dict[str, int]:
        """Count insights by type"""
        
        counts = {}
        for insight in insights:
            counts[insight.type] = counts.get(insight.type, 0) + 1
        
        return counts
