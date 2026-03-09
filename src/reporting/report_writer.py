"""
Phase 5: Natural Language Report Generation

Converts structured insights into executive narratives and actionable recommendations.
Domain-aware and context-sensitive.
"""

from typing import List, Dict, Any
from src.insights.insight_types import Insight, SeverityLevels, InsightTypes


class ReportWriter:
    """Generates natural language executive reports from insights"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load narrative templates for reports"""
        return {
            "executive_summary": """
EXECUTIVE SUMMARY
─────────────────────────────────────────
Dataset: {dataset_name}
Rows: {num_rows:,} | Columns: {num_cols}
Analysis Date: {analysis_date}

{summary_text}

KEY FINDINGS:
{key_findings}

DATA QUALITY: {quality_score}/10
COMPLETENESS: {completeness_score}%
STATISTICAL HEALTH: {statistical_health}
            """,
            
            "recommendation": """
RECOMMENDATION: {title}
Severity: {severity}
─────────────────────────────────────────
{description}

Action Items:
{actions}
            """,
            
            "section_header": "\n{title}\n{'=' * len(title)}\n",
        }
    
    def generate_full_report(self, 
                            insights: List[Insight],
                            eda_results: Dict[str, Any],
                            dataset_name: str = "Dataset") -> Dict[str, str]:
        """
        Generate complete natural language report
        
        Args:
            insights: List of Insight objects
            eda_results: EDA results dictionary
            dataset_name: Name of the dataset being analyzed
            
        Returns:
            Dictionary with different report sections
        """
        
        if not insights:
            return {
                "executive_summary": "No significant insights detected. Dataset appears standard.",
                "key_findings": "N/A",
                "recommendations": "No immediate actions needed.",
                "data_quality_assessment": "Good - baseline data quality detected."
            }
        
        # Extract key metrics
        num_rows = eda_results.get("duplicate_summary", {}).get("total_rows", "Unknown")
        num_cols = len(eda_results.get("cardinality_report", {}))
        
        # Generate sections
        sections = {
            "executive_summary": self._gen_executive_summary(insights, num_rows, num_cols, dataset_name),
            "key_findings": self._gen_key_findings(insights),
            "data_quality_assessment": self._gen_quality_assessment(insights, eda_results),
            "recommendations": self._gen_recommendations(insights),
            "detailed_analysis": self._gen_detailed_analysis(insights)
        }
        
        return sections
    
    def _gen_executive_summary(self, insights: List[Insight], 
                               num_rows: int, num_cols: int, 
                               dataset_name: str) -> str:
        """Generate executive summary section"""
        
        # Count by severity
        critical = sum(1 for i in insights if i.severity == SeverityLevels.CRITICAL)
        high = sum(1 for i in insights if i.severity == SeverityLevels.HIGH)
        medium = sum(1 for i in insights if i.severity == SeverityLevels.MEDIUM)
        
        if critical > 0:
            summary = f"⚠️ CRITICAL ISSUES DETECTED: {critical} critical, {high} high-priority findings require immediate attention."
        elif high > 0:
            summary = f"⚡ SIGNIFICANT FINDINGS: Analysis reveals {high} high-priority issues affecting data quality or statistical validity."
        elif medium > 0:
            summary = f"ℹ️ MODERATE FINDINGS: {medium} observations worth noting for data interpretation and modeling decisions."
        else:
            summary = "✓ BASELINE: Dataset shows standard characteristics with no major anomalies."
        
        # Quality score
        quality_score = max(0, 10 - (critical * 3 + high * 2 + medium))
        completeness = self._calculate_completeness(insights)
        statistical_health = self._assess_statistical_health(insights)
        
        return f"""
EXECUTIVE SUMMARY
{'─' * 60}
Dataset: {dataset_name}
Shape: {num_rows:,} rows × {num_cols} columns
Total Insights: {len(insights)}

{summary}

KEY METRICS:
  • Data Quality Score: {quality_score}/10
  • Completeness: {completeness}%
  • Statistical Health: {statistical_health}
  • Issues Found: {critical} critical, {high} high, {medium} medium
        """
    
    def _gen_key_findings(self, insights: List[Insight]) -> str:
        """Generate key findings section"""
        
        # Group by type and severity
        findings = {}
        for insight in insights:
            if insight.severity in [SeverityLevels.CRITICAL, SeverityLevels.HIGH]:
                key = insight.type
                if key not in findings:
                    findings[key] = []
                findings[key].append(insight)
        
        if not findings:
            return "No critical or high-priority findings."
        
        text = "\nKEY FINDINGS\n" + "─" * 60 + "\n"
        
        for insight_type, type_insights in findings.items():
            text += f"\n• {self._format_insight_type(insight_type)} ({len(type_insights)} issues)\n"
            for insight in type_insights[:3]:  # Top 3 per type
                text += f"  - {insight.title}\n"
        
        return text
    
    def _gen_quality_assessment(self, insights: List[Insight], 
                               eda_results: Dict[str, Any]) -> str:
        """Generate data quality assessment"""
        
        missing_issues = sum(1 for i in insights if "missing" in i.type.lower())
        duplicate_ratio = eda_results.get("duplicate_summary", {}).get("duplicate_ratio", 0)
        constant_cols = eda_results.get("summary", {}).get("constant", [])
        
        text = "\nDATA QUALITY ASSESSMENT\n" + "─" * 60 + "\n"
        
        if missing_issues > 0:
            text += f"\n⚠️ MISSING DATA: {missing_issues} columns with significant missing values detected.\n"
            text += "   Action: Review missing data mechanism (MCAR, MAR, or MNAR).\n"
        
        if duplicate_ratio > 0.01:
            text += f"\n⚠️ DUPLICATES: {duplicate_ratio*100:.1f}% of rows are duplicated.\n"
            text += "   Action: Deduplicate or verify if duplicates are intentional.\n"
        
        if constant_cols:
            text += f"\n⚠️ CONSTANT COLUMNS: {len(constant_cols)} columns contain only one value.\n"
            text += "   Action: Remove or investigate why columns lack variance.\n"
        
        if missing_issues == 0 and duplicate_ratio < 0.01 and not constant_cols:
            text += "\n✓ No major data quality issues detected.\n"
        
        return text
    
    def _gen_recommendations(self, insights: List[Insight]) -> str:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Group insights into actionable groups
        for insight in insights:
            if insight.severity in [SeverityLevels.CRITICAL, SeverityLevels.HIGH]:
                rec = self._create_recommendation(insight)
                if rec:
                    recommendations.append(rec)
        
        if not recommendations:
            return "\nRECOMMENDATIONS\n" + "─" * 60 + "\nNo immediate actions needed.\n"
        
        text = "\nRECOMMENDATIONS\n" + "─" * 60 + "\n"
        for i, rec in enumerate(recommendations[:5], 1):  # Top 5 recommendations
            text += f"\n[{i}] {rec}\n"
        
        return text
    
    def _gen_detailed_analysis(self, insights: List[Insight]) -> str:
        """Generate detailed technical analysis"""
        
        # Group by insight type
        by_type = {}
        for insight in insights:
            if insight.type not in by_type:
                by_type[insight.type] = []
            by_type[insight.type].append(insight)
        
        text = "\nDETAILED ANALYSIS\n" + "─" * 60 + "\n"
        
        for insight_type, type_insights in by_type.items():
            text += f"\n{self._format_insight_type(insight_type)}:\n"
            for insight in type_insights[:3]:
                text += f"  • {insight.column}: {insight.description}\n"
                if insight.context:
                    text += f"    Context: {insight.context}\n"
        
        return text
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _create_recommendation(self, insight: Insight) -> str:
        """Convert insight to actionable recommendation"""
        
        recommendations = {
            InsightTypes.HIGH_MISSING_VALUES: 
                f"Address missing values in '{insight.column}': "
                f"Consider imputation, deletion, or investigating data collection issues.",
            
            InsightTypes.SKEWED_DISTRIBUTION:
                f"Handle skewness in '{insight.column}': "
                f"Consider log transformation, Box-Cox, or separate modeling for skewed segments.",
            
            InsightTypes.HIGH_CARDINALITY:
                f"Review '{insight.column}': "
                f"High cardinality may indicate ID column or require feature engineering.",
            
            InsightTypes.DUPLICATE_ROWS:
                f"Investigate and handle duplicate rows: "
                f"Deduplication may be necessary before analysis.",
            
            InsightTypes.IMBALANCED_CATEGORIES:
                f"Address category imbalance in '{insight.column}': "
                f"Consider stratified sampling or class weighting for modeling.",
            
            InsightTypes.STRONG_POSITIVE_CORRELATION:
                f"Multicollinearity detected: "
                f"'{insight.context.get('col1')}' and '{insight.context.get('col2')}' are highly correlated. "
                f"Consider feature selection or regularization.",
        }
        
        return recommendations.get(insight.type, f"Review {insight.title}")
    
    def _format_insight_type(self, insight_type: str) -> str:
        """Format insight type name for display"""
        return insight_type.replace("_", " ").title()
    
    def _calculate_completeness(self, insights: List[Insight]) -> int:
        """Estimate data completeness percentage"""
        missing_count = sum(1 for i in insights if "missing" in i.type.lower())
        if missing_count > 3:
            return max(50, 100 - (missing_count * 10))
        return 95
    
    def _assess_statistical_health(self, insights: List[Insight]) -> str:
        """Assess overall statistical health"""
        high_issues = sum(1 for i in insights if i.severity == SeverityLevels.HIGH)
        if high_issues > 5:
            return "⚠️ Poor - Significant statistical issues"
        elif high_issues > 2:
            return "⚠️ Fair - Some statistical concerns"
        else:
            return "✓ Good - Reasonable statistical properties"


# =========================================================================
# Convenience function to generate report from raw data
# =========================================================================

def generate_report(insights: List[Insight], 
                   eda_results: Dict[str, Any],
                   dataset_name: str = "Dataset") -> Dict[str, str]:
    """
    Generate a complete report
    
    Args:
        insights: List of Insight objects from Phase 4
        eda_results: EDA results from Phase 3
        dataset_name: Name of dataset
        
    Returns:
        Dictionary with report sections
    """
    writer = ReportWriter()
    return writer.generate_full_report(insights, eda_results, dataset_name)
