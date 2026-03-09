"""
Natural Language Report Generator

Converts structured insights into human-readable reports.
Adapts language based on insight severity and domain context.
"""

from typing import List, Dict, Any
from .insight_types import Insight, InsightTypes, SeverityLevels


class ReportGenerator:
    """Generates natural language insights from structured data"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Define natural language templates for each insight type"""
        return {
            InsightTypes.SKEWED_DISTRIBUTION: {
                "high": "Strong skew detected: '{column}' has a highly skewed distribution (skewness: {value}), indicating data is heavily concentrated toward one end.",
                "medium": "Moderate skew in '{column}' (skewness: {value}). Distribution is not symmetric.",
                "low": "Slight skew in '{column}' (skewness: {value})."
            },
            
            InsightTypes.HIGH_KURTOSIS: {
                "high": "Heavy tails detected: '{column}' has high kurtosis ({value}), indicating more extreme values than a normal distribution.",
                "medium": "'{column}' shows elevated kurtosis ({value}), suggesting thicker tails.",
                "low": "'{column}' has kurtosis of {value}."
            },
            
            InsightTypes.STRONG_POSITIVE_CORRELATION: {
                "high": "Strong positive relationship: '{col1}' and '{col2}' are highly correlated (r = {value}), moving together closely.",
                "medium": "Moderate positive correlation between '{col1}' and '{col2}' (r = {value}).",
                "low": "Slight positive correlation between '{col1}' and '{col2}' (r = {value})."
            },
            
            InsightTypes.STRONG_NEGATIVE_CORRELATION: {
                "high": "Strong inverse relationship: '{col1}' and '{col2}' are highly negatively correlated (r = {value}), moving in opposite directions.",
                "medium": "Moderate negative correlation between '{col1}' and '{col2}' (r = {value}).",
                "low": "Slight negative correlation between '{col1}' and '{col2}' (r = {value})."
            },
            
            InsightTypes.HIGH_CARDINALITY: {
                "high": "Very high cardinality: '{column}' has {num_unique} unique values ({ratio}% of rows). Consider if this is an ID or identifier.",
                "medium": "High cardinality: '{column}' has {num_unique} unique values ({ratio}% of rows).",
            },
            
            InsightTypes.IMBALANCED_CATEGORIES: {
                "high": "Severe imbalance: '{column}' is dominated by category '{top_cat}' ({top_ratio}% of values). Data is highly skewed toward one category.",
                "medium": "Category imbalance in '{column}': top category '{top_cat}' represents {top_ratio}% of values.",
            },
            
            InsightTypes.HIGH_MISSING_VALUES: {
                "high": "Critical missing data: '{column}' has {missing_ratio}% missing values. May impact analysis reliability.",
                "medium": "Significant missing data: '{column}' is {missing_ratio}% missing.",
                "low": "'{column}' has {missing_ratio}% missing values."
            },
            
            InsightTypes.CONSTANT_COLUMN: {
                "high": "No variance: '{column}' contains only one unique value. This column provides no information for analysis."
            },
            
            InsightTypes.DUPLICATE_ROWS: {
                "high": "Duplicate records detected: {dup_count} rows ({dup_ratio}%) are exact duplicates. Data quality issue.",
                "medium": "{dup_count} duplicate rows found ({dup_ratio}% of dataset).",
            },
            
            InsightTypes.OUTLIERS_DETECTED: {
                "high": "Outliers present: '{column}' contains extreme values beyond {lower} and {upper}.",
                "medium": "Some outliers detected in '{column}'.",
            }
        }
    
    def generate_report(self, insights: List[Insight]) -> Dict[str, Any]:
        """
        Generate both structured and natural language report
        
        Args:
            insights: List of Insight objects
            
        Returns:
            Dict with structured insights and natural language report
        """
        
        # Sort by severity
        sorted_insights = sorted(
            insights,
            key=lambda x: SeverityLevels.ORDER.get(x.severity, 0),
            reverse=True
        )
        
        # Group by type
        by_type = {}
        for insight in sorted_insights:
            if insight.type not in by_type:
                by_type[insight.type] = []
            by_type[insight.type].append(insight)
        
        # Generate natural language for each
        natural_language = []
        for insight in sorted_insights:
            text = self._generate_insight_text(insight)
            if text:
                natural_language.append({
                    "severity": insight.severity,
                    "type": insight.type,
                    "text": text
                })
        
        # Generate executive summary
        summary = self._generate_summary(insights)
        
        return {
            "insights": [
                {
                    "type": i.type,
                    "severity": i.severity,
                    "column": i.column,
                    "title": i.title,
                    "value": i.value,
                    "context": i.context
                } for i in sorted_insights
            ],
            "natural_language": natural_language,
            "summary": summary
        }
    
    def _generate_insight_text(self, insight: Insight) -> str:
        """Convert a single insight to natural language"""
        
        templates = self.templates.get(insight.type, {})
        template = templates.get(insight.severity)
        
        if not template:
            return None
        
        # Prepare context variables
        context = {
            "column": insight.column,
            "value": insight.value,
            **insight.context
        }
        
        try:
            return template.format(**context)
        except KeyError:
            return template
    
    def _generate_summary(self, insights: List[Insight]) -> str:
        """Generate executive summary"""
        
        if not insights:
            return "No significant insights detected. Dataset appears well-structured."
        
        critical = sum(1 for i in insights if i.severity == SeverityLevels.CRITICAL)
        high = sum(1 for i in insights if i.severity == SeverityLevels.HIGH)
        medium = sum(1 for i in insights if i.severity == SeverityLevels.MEDIUM)
        
        summary = f"Analysis found {len(insights)} insights: "
        parts = []
        if critical > 0:
            parts.append(f"{critical} critical")
        if high > 0:
            parts.append(f"{high} high-priority")
        if medium > 0:
            parts.append(f"{medium} medium-priority")
        
        summary += ", ".join(parts) + "."
        
        return summary
