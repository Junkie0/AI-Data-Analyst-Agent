"""
Phase 4: Insight Generation Engine

Automatically generates structured insights from EDA outputs.
Provides both machine-readable and natural language formats.
"""

from .insight_engine import InsightEngine
from .report_generator import ReportGenerator

__all__ = ["InsightEngine", "ReportGenerator"]
