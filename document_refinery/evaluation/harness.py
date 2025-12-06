"""
Evaluation harness for running comprehensive model tests.

Coordinates Red/Blue/Purple team evaluations across all models.
"""

from typing import Dict, List, Any
from document_refinery.models.adapter import ModelAdapter
from document_refinery.evaluation.red_team import RedTeam
from document_refinery.evaluation.blue_team import BlueTeam
from document_refinery.evaluation.purple_team import PurpleTeam


class EvaluationHarness:
    """
    Main evaluation harness that orchestrates all testing.
    
    Runs:
    - Red team adversarial tests
    - Blue team defense checks
    - Purple team comprehensive metrics
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize evaluation harness.
        
        Args:
            config: Configuration for evaluation teams
        """
        self.config = config
        self.red_team = RedTeam(config.get("red_team", {}))
        self.blue_team = BlueTeam(config.get("blue_team", {}))
        self.purple_team = PurpleTeam(config.get("purple_team", {}))
    
    def evaluate_model(
        self,
        model: ModelAdapter,
        documents: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run comprehensive evaluation on a model.
        
        Args:
            model: Model adapter to evaluate
            documents: Parsed documents to test with
            
        Returns:
            Evaluation results with red/blue/purple findings
        """
        results = {
            "model_info": model.get_model_info(),
            "red_team": {},
            "blue_team": {},
            "purple_team": {},
        }
        
        # Red team: adversarial testing
        if self.config.get("red_team_enabled", True):
            results["red_team"] = self.red_team.run_attacks(model, documents)
        
        # Blue team: defense evaluation
        if self.config.get("blue_team_enabled", True):
            results["blue_team"] = self.blue_team.evaluate_defenses(model, documents)
        
        # Purple team: combined metrics
        if self.config.get("purple_team_enabled", True):
            results["purple_team"] = self.purple_team.run_evaluation(
                model,
                documents,
                results["red_team"],
                results["blue_team"],
            )
        
        return results
