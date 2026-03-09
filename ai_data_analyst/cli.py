#!/usr/bin/env python3
"""
AI Data Analyst Agent - CLI Tool

Production-ready command-line interface for automated data analysis.

Usage:
    python -m ai_data_analyst.cli analyze data/file.csv
    python -m ai_data_analyst.cli analyze data/file.csv --output-dir results --verbose
    python -m ai_data_analyst.cli batch data/sample/ --recursive
"""

import click
import sys
from pathlib import Path
from typing import Optional
import json

from src.core.pipeline import AnalysisPipeline


@click.group()
@click.version_option()
def cli():
    """AI Data Analyst Agent - Automated Exploratory Data Analysis Engine"""
    pass


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    type=click.Path(),
    default="outputs/analysis",
    help="Output directory for results"
)
@click.option(
    "--dataset-name",
    type=str,
    default=None,
    help="Custom dataset name (defaults to filename)"
)
@click.option(
    "--verbose",
    is_flag=True,
    default=True,
    help="Verbose output"
)
@click.option(
    "--save-json",
    is_flag=True,
    default=True,
    help="Save insights as JSON"
)
@click.option(
    "--save-report",
    is_flag=True,
    default=True,
    help="Save natural language report"
)
@click.option(
    "--print-report",
    is_flag=True,
    default=False,
    help="Print report to console"
)
def analyze(filepath: str,
            output_dir: str,
            dataset_name: Optional[str],
            verbose: bool,
            save_json: bool,
            save_report: bool,
            print_report: bool):
    """
    Analyze a single dataset
    
    Runs the complete pipeline:
    Data Ingestion → Schema → EDA → Insights → Reports
    """
    
    try:
        # Create pipeline
        config = {
            "output_dir": output_dir,
            "save_intermediate": save_json or save_report,
            "verbose": verbose,
        }
        
        pipeline = AnalysisPipeline(config)
        
        # Run analysis
        results = pipeline.run(filepath, dataset_name)
        
        # Print report if requested
        if print_report:
            pipeline.print_report()
        
        # Exit success
        click.secho("\nAnalysis complete!", fg="green")
        sys.exit(0)
    
    except Exception as e:
        click.secho(f"\nError: {str(e)}", fg="red", err=True)
        sys.exit(1)


@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    type=click.Path(),
    default="outputs/batch",
    help="Output directory for batch results"
)
@click.option(
    "--recursive",
    is_flag=True,
    default=False,
    help="Recursively process subdirectories"
)
@click.option(
    "--pattern",
    type=str,
    default="*.csv",
    help="File pattern to match (default: *.csv)"
)
def batch(directory: str, output_dir: str, recursive: bool, pattern: str):
    """
    Batch process multiple datasets
    
    Analyzes all files matching pattern in directory
    """
    
    dir_path = Path(directory)
    
    # Find matching files
    if recursive:
        files = list(dir_path.rglob(pattern))
    else:
        files = list(dir_path.glob(pattern))
    
    if not files:
        click.echo(f"No files matching '{pattern}' found in {directory}")
        sys.exit(1)
    
    click.echo(f"Found {len(files)} file(s) to process\n")
    
    # Process each file
    results_summary = []
    
    for i, filepath in enumerate(files, 1):
        click.echo(f"[{i}/{len(files)}] Processing: {filepath.name}")
        
        try:
            config = {
                "output_dir": output_dir,
                "save_intermediate": True,
                "verbose": False,  # Less verbose for batch
            }
            
            pipeline = AnalysisPipeline(config)
            results = pipeline.run(str(filepath), filepath.stem)
            
            insights_count = results["insights"]["count"]
            high_severity = results["insights"]["metadata"]["by_severity"].get("high", 0)
            
            results_summary.append({
                "file": filepath.name,
                "insights": insights_count,
                "high_severity": high_severity,
                "status": "✓"
            })
            
            click.echo(f"  ✓ {insights_count} insights ({high_severity} high) → {output_dir}")
        
        except Exception as e:
            results_summary.append({
                "file": filepath.name,
                "status": "✗",
                "error": str(e)
            })
            click.echo(f"  ✗ Error: {str(e)}")
    
    # Print summary
    click.echo(f"\n{'='*70}")
    click.echo("BATCH PROCESSING SUMMARY")
    click.echo(f"{'='*70}")
    for result in results_summary:
        if result["status"] == "✓":
            click.echo(f"  {result['file']:30} {result['insights']:3} insights")
        else:
            click.echo(f"  {result['file']:30} ERROR")
    
    click.echo(f"{'='*70}\n")
    sys.exit(0)


@cli.command()
@click.argument("filepath", type=click.Path(exists=True))
def validate(filepath: str):
    """
    Validate dataset without full analysis
    
    Performs schema inference and basic validation only
    """
    
    from src.ingestion.loader import DataLoader
    from src.schema.inference2 import infer_schema
    from src.validation.quality_checks import (
        high_missing_columns,
        constant_columns,
        id_like_columns
    )
    
    try:
        click.echo(f"Validating: {filepath}\n")
        
        # Load
        df = DataLoader.load(filepath)
        click.echo(f"✓ Loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")
        
        # Schema
        schema = infer_schema(df)
        click.echo(f"✓ Schema inferred")
        
        # Checks
        missing = high_missing_columns(df)
        constants = constant_columns(df)
        id_like = id_like_columns(df)
        
        click.echo(f"\nValidation Results:")
        click.echo(f"  High missing: {len(missing['flagged_columns'])} columns")
        click.echo(f"  Constants: {len(constants['constant_columns'])} columns")
        click.echo(f"  ID-like: {len(id_like['id_like_columns'])} columns")
        
        # Issues
        issues = (len(missing['flagged_columns']) + 
                 len(constants['constant_columns']) + 
                 len(id_like['id_like_columns']))
        
        if issues == 0:
            click.echo("\n✓ Dataset looks healthy!")
        else:
            click.echo(f"\n⚠️  Found {issues} potential issues")
        
        sys.exit(0)
    
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def version():
    """Show version information"""
    click.echo("AI Data Analyst Agent v1.0.0")


if __name__ == "__main__":
    cli()
