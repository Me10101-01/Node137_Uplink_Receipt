"""
Core orchestration for Document Refinery.

This module provides the main DocumentRefinery class that coordinates:
- Document ingestion and structuring
- Model evaluation harness
- Red/Blue/Purple team evaluations
- Report generation
"""

from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml
from datetime import datetime

from document_refinery.ingestion.parser import DocumentParser
from document_refinery.models.adapter import ModelAdapter
from document_refinery.evaluation.harness import EvaluationHarness
from document_refinery.reports.generator import ReportGenerator


class DocumentRefinery:
    """
    Main orchestrator for the Strategickhaos Document Refinery.
    
    Provides a unified interface for:
    1. Document intake & structuring
    2. Model evaluation across multiple backends
    3. Red/Blue/Purple team testing
    4. Anti-fragility report generation
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the Document Refinery.
        
        Args:
            config_path: Path to YAML configuration file. If None, uses defaults.
        """
        self.config = self._load_config(config_path)
        self.parser = DocumentParser(self.config.get("parser", {}))
        self.models: Dict[str, ModelAdapter] = {}
        self.harness = EvaluationHarness(self.config.get("evaluation", {}))
        self.report_generator = ReportGenerator(self.config.get("reports", {}))
        
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Load configuration from YAML file or return defaults."""
        if config_path and config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "parser": {
                "chunk_size": 512,
                "overlap": 50,
            },
            "evaluation": {
                "red_team_enabled": True,
                "blue_team_enabled": True,
                "purple_team_enabled": True,
            },
            "reports": {
                "output_format": ["markdown", "json"],
                "include_metrics": True,
            },
        }
    
    def add_model(self, name: str, adapter: ModelAdapter) -> None:
        """
        Register a model for evaluation.
        
        Args:
            name: Identifier for the model
            adapter: ModelAdapter instance configured for this model
        """
        self.models[name] = adapter
    
    def ingest_documents(self, document_paths: List[Path]) -> Dict[str, Any]:
        """
        Ingest and parse documents.
        
        Args:
            document_paths: List of paths to documents to process
            
        Returns:
            Dictionary containing parsed document structures
        """
        parsed_docs = {}
        for path in document_paths:
            parsed_docs[str(path)] = self.parser.parse(path)
        return parsed_docs
    
    def evaluate(self, documents: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run comprehensive evaluation on documents across all models.
        
        Args:
            documents: Parsed document structures
            
        Returns:
            Evaluation results including red/blue/purple team findings
        """
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "models": {},
            "documents": list(documents.keys()),
        }
        
        for model_name, model_adapter in self.models.items():
            model_results = self.harness.evaluate_model(
                model_adapter,
                documents,
            )
            results["models"][model_name] = model_results
        
        return results
    
    def generate_report(
        self,
        evaluation_results: Dict[str, Any],
        output_path: Path,
        report_type: str = "anti_fragility",
    ) -> Path:
        """
        Generate comprehensive report from evaluation results.
        
        Args:
            evaluation_results: Results from evaluate()
            output_path: Where to save the report
            report_type: Type of report (anti_fragility, governance, etc.)
            
        Returns:
            Path to generated report
        """
        return self.report_generator.generate(
            evaluation_results,
            output_path,
            report_type,
        )
    
    def audit_documents(
        self,
        document_paths: List[Path],
        output_dir: Path,
    ) -> Dict[str, Path]:
        """
        Complete end-to-end audit pipeline.
        
        Args:
            document_paths: Documents to audit
            output_dir: Directory for output reports
            
        Returns:
            Dictionary mapping report types to their file paths
        """
        # Ingest documents
        documents = self.ingest_documents(document_paths)
        
        # Run evaluation
        results = self.evaluate(documents)
        
        # Generate reports
        output_dir.mkdir(parents=True, exist_ok=True)
        reports = {}
        
        for report_type in ["anti_fragility", "governance"]:
            report_path = output_dir / f"{report_type}_report.md"
            generated_path = self.generate_report(results, report_path, report_type)
            reports[report_type] = generated_path
        
        return reports
