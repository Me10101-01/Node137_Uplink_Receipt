"""
CLI for Strategickhaos Document Refinery.

Usage:
    sk-refinery audit path/to/docs
    sk-refinery evaluate --model local path/to/docs
    sk-refinery report results.json
"""

import click
from pathlib import Path
from typing import Optional
import yaml
import json

from document_refinery.core import DocumentRefinery
from document_refinery.models.local_adapter import LocalModelAdapter


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    Strategickhaos Document Refinery (SDR)
    
    Sovereign AI Document Intelligence Lab
    
    Zero-vendor-lock-in AI legal/document review layer with
    Red/Blue/Purple team evaluations.
    """
    pass


@cli.command()
@click.argument('documents', type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    '--config',
    type=click.Path(exists=True),
    help='Path to YAML configuration file',
)
@click.option(
    '--output',
    type=click.Path(),
    default='./refinery_output',
    help='Output directory for reports',
)
@click.option(
    '--model',
    type=str,
    default='local',
    help='Model type to use (local, openai, etc.)',
)
@click.option(
    '--model-name',
    type=str,
    default='default-local-model',
    help='Name/identifier for the model',
)
def audit(
    documents: tuple,
    config: Optional[str],
    output: str,
    model: str,
    model_name: str,
):
    """
    Run complete audit on documents.
    
    This performs:
    - Document ingestion and parsing
    - Red team adversarial testing
    - Blue team defense evaluation
    - Purple team comprehensive metrics
    - Anti-fragility report generation
    
    Example:
        sk-refinery audit contract.txt agreement.md
    """
    click.echo("🔬 Strategickhaos Document Refinery")
    click.echo("=" * 50)
    
    # Load configuration
    config_path = Path(config) if config else None
    
    # Initialize refinery
    click.echo("\n📋 Initializing Document Refinery...")
    refinery = DocumentRefinery(config_path)
    
    # Add model
    click.echo(f"🤖 Loading model: {model_name} ({model})...")
    if model == 'local':
        model_adapter = LocalModelAdapter({
            "model_name": model_name,
            "model_path": "./models/local",
        })
    elif model == 'openai':
        from document_refinery.models.openai_adapter import OpenAIAdapter
        model_adapter = OpenAIAdapter({
            "model_name": model_name,
            "api_key": click.prompt("Enter OpenAI API key", hide_input=True),
        })
    else:
        click.echo(f"❌ Unknown model type: {model}", err=True)
        return
    
    refinery.add_model(model_name, model_adapter)
    
    # Convert documents to Path objects
    document_paths = [Path(doc) for doc in documents]
    
    # Run audit
    click.echo(f"\n📄 Auditing {len(document_paths)} document(s)...")
    with click.progressbar(length=100, label='Running evaluation') as bar:
        bar.update(20)
        output_dir = Path(output)
        bar.update(30)
        reports = refinery.audit_documents(document_paths, output_dir)
        bar.update(50)
    
    # Display results
    click.echo("\n✅ Audit complete!")
    click.echo(f"\n📊 Reports generated in: {output_dir}")
    for report_type, report_path in reports.items():
        click.echo(f"  - {report_type}: {report_path}")
    
    click.echo("\n" + "=" * 50)
    click.echo("Review the anti-fragility report for comprehensive findings.")


@cli.command()
@click.argument('config_file', type=click.Path())
def init(config_file: str):
    """
    Create a sample configuration file.
    
    Example:
        sk-refinery init config.yaml
    """
    config_path = Path(config_file)
    
    sample_config = {
        "parser": {
            "chunk_size": 512,
            "overlap": 50,
        },
        "evaluation": {
            "red_team_enabled": True,
            "blue_team_enabled": True,
            "purple_team_enabled": True,
            "red_team": {
                "attack_count": 10,
            },
            "blue_team": {},
            "purple_team": {},
        },
        "reports": {
            "output_format": ["markdown", "json"],
            "include_metrics": True,
        },
        "models": {
            "local": {
                "model_path": "./models/local",
                "device": "cpu",
            },
        },
    }
    
    with open(config_path, 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False)
    
    click.echo(f"✅ Created sample configuration: {config_path}")
    click.echo("\nEdit this file to customize your Document Refinery settings.")


@cli.command()
@click.argument('results_file', type=click.Path(exists=True))
@click.option(
    '--output',
    type=click.Path(),
    help='Output path for report',
)
@click.option(
    '--type',
    'report_type',
    type=click.Choice(['anti_fragility', 'governance']),
    default='anti_fragility',
    help='Type of report to generate',
)
def report(results_file: str, output: Optional[str], report_type: str):
    """
    Generate a report from evaluation results JSON.
    
    Example:
        sk-refinery report results.json --type anti_fragility
    """
    click.echo("📊 Generating report...")
    
    # Load results
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        base = Path(results_file).stem
        output_path = Path(f"{base}_{report_type}_report.md")
    
    # Generate report
    from document_refinery.reports.generator import ReportGenerator
    generator = ReportGenerator({"output_format": ["markdown", "json"]})
    
    report_path = generator.generate(results, output_path, report_type)
    
    click.echo(f"✅ Report generated: {report_path}")


@cli.command()
def version():
    """Show version information."""
    click.echo("Strategickhaos Document Refinery v0.1.0")
    click.echo("Sovereign AI Document Intelligence Lab")
    click.echo("")
    click.echo("Copyright (c) 2025 Strategickhaos DAO LLC")
    click.echo("Licensed under MIT License")


if __name__ == '__main__':
    cli()
