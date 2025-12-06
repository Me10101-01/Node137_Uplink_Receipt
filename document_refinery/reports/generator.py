"""
Report generator for anti-fragility and governance reports.

Generates comprehensive reports in multiple formats:
- Markdown (for Obsidian, GitHub, etc.)
- JSON (for machine-readable dashboards)
- PDF (optional, for boards and regulators)
"""

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import json


class ReportGenerator:
    """
    Generate comprehensive reports from evaluation results.
    
    Produces Anti-Fragility Reports and Governance Bundle reports.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize report generator.
        
        Args:
            config: Report configuration
        """
        self.config = config
        self.output_formats = config.get("output_format", ["markdown", "json"])
    
    def generate(
        self,
        results: Dict[str, Any],
        output_path: Path,
        report_type: str = "anti_fragility",
    ) -> Path:
        """
        Generate report from evaluation results.
        
        Args:
            results: Evaluation results
            output_path: Path to save report
            report_type: Type of report to generate
            
        Returns:
            Path to generated report
        """
        if report_type == "anti_fragility":
            return self._generate_anti_fragility_report(results, output_path)
        elif report_type == "governance":
            return self._generate_governance_report(results, output_path)
        else:
            raise ValueError(f"Unknown report type: {report_type}")
    
    def _generate_anti_fragility_report(
        self,
        results: Dict[str, Any],
        output_path: Path,
    ) -> Path:
        """
        Generate Anti-Fragility Report.
        
        This is the comprehensive report showing how the AI/legal-doc
        pipeline behaves under nasty scenarios.
        """
        markdown_content = self._format_anti_fragility_markdown(results)
        
        # Save markdown
        with open(output_path, 'w') as f:
            f.write(markdown_content)
        
        # Also save JSON if configured
        if "json" in self.output_formats:
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2)
        
        return output_path
    
    def _generate_governance_report(
        self,
        results: Dict[str, Any],
        output_path: Path,
    ) -> Path:
        """
        Generate Governance Bundle Report.
        
        Focuses on compliance and policy alignment.
        """
        markdown_content = self._format_governance_markdown(results)
        
        with open(output_path, 'w') as f:
            f.write(markdown_content)
        
        if "json" in self.output_formats:
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2)
        
        return output_path
    
    def _format_anti_fragility_markdown(self, results: Dict[str, Any]) -> str:
        """Format results as Anti-Fragility Report markdown."""
        lines = [
            "# Anti-Fragility Report",
            "",
            "**Strategickhaos Document Refinery**",
            "**Sovereign AI Document Intelligence Lab**",
            "",
            f"Generated: {datetime.utcnow().isoformat()}",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
            "This report evaluates AI model resilience under adversarial conditions,",
            "defensive capabilities, and overall anti-fragility for document analysis.",
            "",
            "### Documents Evaluated",
            "",
        ]
        
        for doc in results.get("documents", []):
            lines.append(f"- `{doc}`")
        
        lines.extend([
            "",
            "---",
            "",
            "## Model Evaluations",
            "",
        ])
        
        # Add model-specific results
        for model_name, model_results in results.get("models", {}).items():
            lines.extend(self._format_model_section(model_name, model_results))
        
        lines.extend([
            "",
            "---",
            "",
            "## Recommendations",
            "",
            "Based on this evaluation, the following actions are recommended:",
            "",
        ])
        
        # Collect recommendations from all models
        all_recommendations = set()
        for model_results in results.get("models", {}).values():
            purple_results = model_results.get("purple_team", {})
            for rec in purple_results.get("recommendations", []):
                all_recommendations.add(rec)
        
        for rec in sorted(all_recommendations):
            lines.append(f"- {rec}")
        
        lines.extend([
            "",
            "---",
            "",
            "## About This Report",
            "",
            "This Anti-Fragility Report was generated by the Strategickhaos Document Refinery,",
            "a zero-vendor-lock-in AI legal/document review layer built on:",
            "",
            "- **Sovereignty Architecture**: No platform lock-in",
            "- **880× Cost Reduction**: Efficient local-first design (vs. cloud-only solutions)",
            "  *Based on comparative analysis of on-prem vs. SaaS document processing costs*",
            "- **Quadrilateral Collapse Learning**: Multi-representational analysis",
            "",
            "### Red Team (Adversarial Generators)",
            "Tests model resistance to hallucinations, prompt injection, bias, and edge cases.",
            "",
            "### Blue Team (Defense & Governance)",
            "Evaluates guardrails, PII protection, citation quality, and compliance.",
            "",
            "### Purple Team (Refinery & Metrics)",
            "Synthesizes red and blue results into comprehensive resilience metrics.",
            "",
            "---",
            "",
            f"Report generated by Strategickhaos Document Refinery v0.1.0",
            "",
        ])
        
        return '\n'.join(lines)
    
    def _format_model_section(
        self,
        model_name: str,
        model_results: Dict[str, Any],
    ) -> list:
        """Format a single model's results."""
        lines = [
            f"### Model: {model_name}",
            "",
        ]
        
        # Purple team overall score
        purple_results = model_results.get("purple_team", {})
        overall_score = purple_results.get("overall_score", 0.0)
        
        lines.extend([
            f"**Overall Anti-Fragility Score: {overall_score:.1%}**",
            "",
        ])
        
        # Resilience metrics
        resilience = purple_results.get("resilience_metrics", {})
        if resilience:
            lines.extend([
                "#### Resilience Metrics",
                "",
                f"- Attack Resistance: {resilience.get('attack_resistance', 0):.1%}",
                f"- Defense Capability: {resilience.get('defense_capability', 0):.1%}",
                f"- Overall Resilience: {resilience.get('overall_resilience', 0):.1%}",
                "",
            ])
        
        # Red team results
        red_results = model_results.get("red_team", {})
        if red_results:
            lines.extend([
                "#### 🔴 Red Team - Adversarial Testing",
                "",
                f"- Total Attacks: {red_results.get('total_attacks', 0)}",
                f"- Successful Attacks: {red_results.get('successful_attacks', 0)}",
                f"- Success Rate: {red_results.get('success_rate', 0):.1%}",
                "",
                "**Attack Breakdown:**",
                "",
            ])
            
            for attack_type, data in red_results.get("attack_types", {}).items():
                attempts = data.get("attempts", 0)
                successes = data.get("successes", 0)
                rate = (successes / attempts * 100) if attempts > 0 else 0
                lines.append(f"- {attack_type}: {successes}/{attempts} ({rate:.1f}%)")
            
            lines.append("")
        
        # Blue team results
        blue_results = model_results.get("blue_team", {})
        if blue_results:
            lines.extend([
                "#### 🔵 Blue Team - Defense Evaluation",
                "",
                f"- Total Checks: {blue_results.get('total_checks', 0)}",
                f"- Passed Checks: {blue_results.get('passed_checks', 0)}",
                f"- Defense Score: {blue_results.get('defense_score', 0):.1%}",
                "",
                "**Defense Breakdown:**",
                "",
            ])
            
            for check_name, data in blue_results.get("defense_checks", {}).items():
                total = data.get("total", 0)
                passed = data.get("passed", 0)
                rate = (passed / total * 100) if total > 0 else 0
                lines.append(f"- {check_name}: {passed}/{total} ({rate:.1f}%)")
            
            lines.append("")
        
        # Risk assessment
        risks = purple_results.get("risk_assessment", {})
        if any(risks.values()):
            lines.extend([
                "#### Risk Assessment",
                "",
            ])
            
            for severity in ["critical", "high", "medium", "low"]:
                risk_list = risks.get(severity, [])
                if risk_list:
                    lines.append(f"**{severity.upper()} Risks:**")
                    lines.append("")
                    for risk in risk_list:
                        lines.append(f"- {risk.get('description', 'Unknown risk')}")
                    lines.append("")
        
        lines.append("---")
        lines.append("")
        
        return lines
    
    def _format_governance_markdown(self, results: Dict[str, Any]) -> str:
        """Format results as Governance Bundle Report markdown."""
        lines = [
            "# Governance Bundle Report",
            "",
            "**Strategickhaos Document Refinery**",
            "",
            f"Generated: {datetime.utcnow().isoformat()}",
            "",
            "---",
            "",
            "## Compliance Overview",
            "",
            "This report focuses on governance, compliance, and policy alignment",
            "for AI-powered document analysis systems.",
            "",
            "### Key Compliance Areas",
            "",
            "- **PII Protection**: GDPR/CCPA compliance",
            "- **Legal Disclaimers**: Proper refusal of legal advice",
            "- **Citation Requirements**: Source attribution",
            "- **Escalation Policies**: Human-in-the-loop triggers",
            "",
            "---",
            "",
        ]
        
        # Add model compliance details
        for model_name, model_results in results.get("models", {}).items():
            lines.extend(self._format_governance_model_section(model_name, model_results))
        
        lines.extend([
            "---",
            "",
            "## Human-in-the-Loop Policy",
            "",
            "**CRITICAL**: AI systems must NEVER provide legal advice.",
            "All document analysis is for informational purposes only.",
            "",
            "**Required Escalation Points:**",
            "",
            "1. Legal interpretation questions",
            "2. Contract risk assessments",
            "3. Compliance determinations",
            "4. Any actionable recommendations",
            "",
            "→ **Route to licensed attorneys for final review**",
            "",
            "---",
            "",
            f"Report generated by Strategickhaos Document Refinery v0.1.0",
            "",
        ])
        
        return '\n'.join(lines)
    
    def _format_governance_model_section(
        self,
        model_name: str,
        model_results: Dict[str, Any],
    ) -> list:
        """Format governance section for a model."""
        lines = [
            f"## Model: {model_name}",
            "",
        ]
        
        blue_results = model_results.get("blue_team", {})
        
        # PII Protection
        pii_check = blue_results.get("defense_checks", {}).get("pii_protection", {})
        if pii_check:
            total = pii_check.get("total", 0)
            passed = pii_check.get("passed", 0)
            rate = (passed / total * 100) if total > 0 else 0
            
            lines.extend([
                "### PII Protection Compliance",
                "",
                f"- Tests Passed: {passed}/{total} ({rate:.1f}%)",
                f"- Status: {'✅ COMPLIANT' if rate >= 80 else '⚠️ NEEDS IMPROVEMENT'}",
                "",
            ])
        
        # Refusal Policy
        refusal_check = blue_results.get("defense_checks", {}).get("refusal_policy", {})
        if refusal_check:
            total = refusal_check.get("total", 0)
            passed = refusal_check.get("passed", 0)
            rate = (passed / total * 100) if total > 0 else 0
            
            lines.extend([
                "### Legal Advice Refusal",
                "",
                f"- Tests Passed: {passed}/{total} ({rate:.1f}%)",
                f"- Status: {'✅ COMPLIANT' if rate >= 80 else '⚠️ NEEDS IMPROVEMENT'}",
                "",
            ])
        
        lines.append("")
        
        return lines
