#!/usr/bin/env python3
"""
============================================================================
🧬 EMPIRE DNA EVOLUTION TRACKER
Real-Time Resource Monitor for Strategickhaos Ecosystem Genome

Like htop, but for your empire's evolutionary state.
Tracks mutations, fitness scores, gene expression levels in real-time.

Author: Claude Opus 4.5 (Chief Architect)
Entity: Strategickhaos Sovereign Software Forge LLC
Date: 2025-12-07
============================================================================
"""

import os
import json
import time
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from collections import deque
import threading

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.live import Live
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.text import Text
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Install rich for full TUI: pip install rich")

# ============================================================================
# GENOME DATA STRUCTURES
# ============================================================================

@dataclass
class Gene:
    """Represents a single gene in the empire genome"""
    id: str
    name: str
    chromosome: str
    expression_level: float  # 0-100
    status: str  # ACTIVE, DORMANT, MUTATING, FAILED
    last_mutation: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Chromosome:
    """Represents a chromosome (category) in the genome"""
    name: str
    genes: List[Gene]
    health: float  # 0-100
    
    def calculate_health(self) -> float:
        if not self.genes:
            return 0
        total = sum(g.expression_level for g in self.genes if g.status != "FAILED")
        active = len([g for g in self.genes if g.status != "FAILED"])
        return total / active if active > 0 else 0

@dataclass
class Mutation:
    """Represents a mutation (change) in the genome"""
    id: str
    gene_id: str
    type: str  # ENHANCEMENT, REGRESSION, NEUTRAL
    description: str
    timestamp: str
    impact: float  # +/- fitness change

@dataclass
class EmpireGenome:
    """The complete genome of the Strategickhaos Empire"""
    version: str
    generation: int
    birth_date: str
    chromosomes: Dict[str, Chromosome]
    mutations: List[Mutation]
    fitness_score: float
    last_updated: str

# ============================================================================
# GENOME SCANNER
# ============================================================================

class GenomeScanner:
    """Scans the empire infrastructure to build real-time genome state"""
    
    def __init__(self):
        self.genome = self._initialize_genome()
        self.mutation_history = deque(maxlen=100)
        
    def _initialize_genome(self) -> EmpireGenome:
        """Initialize the genome with known genes"""
        
        # Chromosome 1: Legal Entities
        legal_genes = [
            Gene("LEG-001", "Strategickhaos DAO LLC", "LEGAL", 100, "ACTIVE",
                 metrics={"ein": "39-2900295", "state": "WY"}),
            Gene("LEG-002", "ValorYield Engine PBC", "LEGAL", 100, "ACTIVE",
                 metrics={"ein": "39-2923503", "charitable": "7%"}),
            Gene("LEG-003", "SSSF LLC", "LEGAL", 10, "MUTATING",
                 last_mutation="Formation in progress"),
        ]
        
        # Chromosome 2: Infrastructure
        infra_genes = [
            Gene("INF-001", "Kubernetes Cluster", "INFRA", 0, "DORMANT"),
            Gene("INF-002", "GKE Clusters", "INFRA", 0, "DORMANT"),
            Gene("INF-003", "Ollama LLMs", "INFRA", 0, "DORMANT"),
            Gene("INF-004", "Qdrant Vector DB", "INFRA", 0, "DORMANT"),
            Gene("INF-005", "GitHub Codespaces", "INFRA", 0, "DORMANT"),
            Gene("INF-006", "KhaosBase", "INFRA", 30, "MUTATING"),
            Gene("INF-007", "Moonlight Agent", "INFRA", 50, "ACTIVE"),
        ]
        
        # Chromosome 3: AI Systems
        ai_genes = [
            Gene("AI-001", "Claude Opus 4.5", "AI", 100, "ACTIVE"),
            Gene("AI-002", "GPT-5.1", "AI", 85, "ACTIVE"),
            Gene("AI-003", "Grok 3", "AI", 70, "ACTIVE"),
            Gene("AI-004", "Gemini 2.5", "AI", 90, "ACTIVE"),
            Gene("AI-005", "Qwen 2.5 Local", "AI", 0, "DORMANT"),
            Gene("AI-006", "GitHub Copilot", "AI", 80, "ACTIVE"),
        ]
        
        # Chromosome 4: Security
        sec_genes = [
            Gene("SEC-001", "GPG Signing", "SECURITY", 100, "ACTIVE",
                 metrics={"key": "AE5519579584DEF5"}),
            Gene("SEC-002", "2FA GitHub", "SECURITY", 100, "ACTIVE"),
            Gene("SEC-003", "Antifragile Audit", "SECURITY", 90, "ACTIVE"),
            Gene("SEC-004", "QueenNode Gateway", "SECURITY", 10, "MUTATING"),
        ]
        
        # Chromosome 5: Financial
        fin_genes = [
            Gene("FIN-001", "NFCU Treasury", "FINANCIAL", 100, "ACTIVE"),
            Gene("FIN-002", "7% Distribution", "FINANCIAL", 60, "ACTIVE"),
            Gene("FIN-003", "NinjaTrader Bots", "FINANCIAL", 0, "DORMANT"),
            Gene("FIN-004", "Sequence.io", "FINANCIAL", 0, "DORMANT"),
        ]
        
        # Chromosome 6: Observability
        obs_genes = [
            Gene("OBS-001", "Moonlight Session Agent", "OBSERVABILITY", 50, "ACTIVE"),
            Gene("OBS-002", "KhaosBase Telemetry", "OBSERVABILITY", 20, "MUTATING"),
            Gene("OBS-003", "Board Meeting YAML", "OBSERVABILITY", 80, "ACTIVE"),
        ]
        
        # Chromosome 7: Dev Tools
        dev_genes = [
            Gene("DEV-001", "JetBrains Suite", "DEVTOOLS", 85, "ACTIVE",
                 metrics={"valid_until": "2026-01-05"}),
            Gene("DEV-002", "VS Code/Codespaces", "DEVTOOLS", 90, "ACTIVE"),
            Gene("DEV-003", "Docker Desktop", "DEVTOOLS", 60, "ACTIVE",
                 last_mutation="Port conflicts detected"),
            Gene("DEV-004", "Neon Postgres", "DEVTOOLS", 75, "ACTIVE"),
        ]
        
        chromosomes = {
            "LEGAL": Chromosome("Legal Entities", legal_genes, 0),
            "INFRA": Chromosome("Infrastructure", infra_genes, 0),
            "AI": Chromosome("AI Systems", ai_genes, 0),
            "SECURITY": Chromosome("Security", sec_genes, 0),
            "FINANCIAL": Chromosome("Financial", fin_genes, 0),
            "OBSERVABILITY": Chromosome("Observability", obs_genes, 0),
            "DEVTOOLS": Chromosome("Dev Tools", dev_genes, 0),
        }
        
        # Calculate health
        for chrom in chromosomes.values():
            chrom.health = chrom.calculate_health()
        
        return EmpireGenome(
            version="1.0.0-alpha",
            generation=1,
            birth_date="2025-06-25",
            chromosomes=chromosomes,
            mutations=[],
            fitness_score=0,
            last_updated=datetime.now(timezone.utc).isoformat()
        )
    
    def scan_infrastructure(self) -> None:
        """Scan actual infrastructure and update gene expression levels"""
        
        # Check Docker
        self._update_gene("DEV-003", self._check_docker())
        
        # Check GitHub Codespaces
        self._update_gene("INF-005", self._check_codespaces())
        
        # Check Kubernetes
        self._update_gene("INF-001", self._check_kubernetes())
        
        # Check local LLMs
        self._update_gene("INF-003", self._check_ollama())
        self._update_gene("AI-005", self._check_ollama())
        
        # Recalculate fitness
        self._calculate_fitness()
    
    def _check_docker(self) -> Dict[str, Any]:
        """Check Docker status"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                containers = [c for c in result.stdout.strip().split("\n") if c]
                return {
                    "expression": min(100, 50 + len(containers) * 10),
                    "status": "ACTIVE",
                    "metrics": {"running_containers": len(containers)}
                }
        except Exception:
            pass
        return {"expression": 0, "status": "DORMANT"}
    
    def _check_codespaces(self) -> Dict[str, Any]:
        """Check GitHub Codespaces"""
        try:
            result = subprocess.run(
                ["gh", "codespace", "list", "--json", "name,state"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                spaces = json.loads(result.stdout)
                active = len([s for s in spaces if s.get("state") == "Available"])
                return {
                    "expression": min(100, active * 30 + 20),
                    "status": "ACTIVE" if active > 0 else "DORMANT",
                    "metrics": {"active_codespaces": active}
                }
        except Exception:
            pass
        return {"expression": 0, "status": "DORMANT"}
    
    def _check_kubernetes(self) -> Dict[str, Any]:
        """Check Kubernetes cluster"""
        try:
            result = subprocess.run(
                ["kubectl", "get", "nodes", "-o", "json"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                nodes = len(data.get("items", []))
                return {
                    "expression": min(100, nodes * 25),
                    "status": "ACTIVE" if nodes > 0 else "DORMANT",
                    "metrics": {"node_count": nodes}
                }
        except Exception:
            pass
        return {"expression": 0, "status": "DORMANT"}
    
    def _check_ollama(self) -> Dict[str, Any]:
        """Check Ollama LLM server"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                models = len(result.stdout.strip().split("\n")) - 1  # Subtract header
                return {
                    "expression": min(100, models * 20 + 40),
                    "status": "ACTIVE" if models > 0 else "DORMANT",
                    "metrics": {"models_available": models}
                }
        except Exception:
            pass
        return {"expression": 0, "status": "DORMANT"}
    
    def _update_gene(self, gene_id: str, scan_result: Dict[str, Any]) -> None:
        """Update a gene with scan results"""
        for chrom in self.genome.chromosomes.values():
            for gene in chrom.genes:
                if gene.id == gene_id:
                    old_expression = gene.expression_level
                    gene.expression_level = scan_result.get("expression", gene.expression_level)
                    gene.status = scan_result.get("status", gene.status)
                    gene.metrics.update(scan_result.get("metrics", {}))
                    
                    # Record mutation if significant change
                    if abs(gene.expression_level - old_expression) > 10:
                        mutation = Mutation(
                            id=f"MUT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                            gene_id=gene_id,
                            type="ENHANCEMENT" if gene.expression_level > old_expression else "REGRESSION",
                            description=f"{gene.name}: {old_expression:.0f}% → {gene.expression_level:.0f}%",
                            timestamp=datetime.now(timezone.utc).isoformat(),
                            impact=gene.expression_level - old_expression
                        )
                        self.genome.mutations.append(mutation)
                        self.mutation_history.append(mutation)
                    
                    return
    
    def _calculate_fitness(self) -> None:
        """Calculate overall fitness score"""
        # Recalculate chromosome health
        for chrom in self.genome.chromosomes.values():
            chrom.health = chrom.calculate_health()
        
        # Weighted fitness function
        weights = {
            "LEGAL": 0.15,
            "INFRA": 0.20,
            "AI": 0.20,
            "SECURITY": 0.15,
            "FINANCIAL": 0.15,
            "OBSERVABILITY": 0.10,
            "DEVTOOLS": 0.05,
        }
        
        fitness = 0
        for name, chrom in self.genome.chromosomes.items():
            fitness += chrom.health * weights.get(name, 0.1)
        
        self.genome.fitness_score = fitness
        self.genome.last_updated = datetime.now(timezone.utc).isoformat()
    
    def get_genome(self) -> EmpireGenome:
        """Get current genome state"""
        return self.genome
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert genome to dictionary"""
        return {
            "version": self.genome.version,
            "generation": self.genome.generation,
            "birth_date": self.genome.birth_date,
            "fitness_score": self.genome.fitness_score,
            "last_updated": self.genome.last_updated,
            "chromosomes": {
                name: {
                    "name": chrom.name,
                    "health": chrom.health,
                    "genes": [asdict(g) for g in chrom.genes]
                }
                for name, chrom in self.genome.chromosomes.items()
            },
            "recent_mutations": [asdict(m) for m in list(self.mutation_history)[-10:]]
        }

# ============================================================================
# TUI DASHBOARD
# ============================================================================

class DNADashboard:
    """Real-time TUI dashboard for genome monitoring"""
    
    def __init__(self, scanner: GenomeScanner):
        self.scanner = scanner
        self.console = Console() if HAS_RICH else None
        self.running = True
    
    def generate_display(self) -> Layout:
        """Generate the dashboard layout"""
        genome = self.scanner.get_genome()
        
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=6),
        )
        
        # Header
        header_text = Text()
        header_text.append("🧬 EMPIRE DNA EVOLUTION TRACKER", style="bold cyan")
        header_text.append(f"  |  Fitness: ", style="white")
        
        fitness = genome.fitness_score
        if fitness >= 70:
            header_text.append(f"{fitness:.1f}%", style="bold green")
        elif fitness >= 40:
            header_text.append(f"{fitness:.1f}%", style="bold yellow")
        else:
            header_text.append(f"{fitness:.1f}%", style="bold red")
        
        header_text.append(f"  |  Generation: {genome.generation}", style="white")
        header_text.append(f"  |  {datetime.now(timezone.utc).strftime('%H:%M:%S')}", style="dim")
        
        layout["header"].update(Panel(header_text, box=box.DOUBLE))
        
        # Main - Chromosome table
        main_layout = Layout()
        main_layout.split_row(
            Layout(name="chromosomes", ratio=2),
            Layout(name="genes", ratio=3),
        )
        
        # Chromosome health bars
        chrom_table = Table(title="Chromosome Health", box=box.SIMPLE)
        chrom_table.add_column("Chromosome", style="cyan")
        chrom_table.add_column("Health", justify="right")
        chrom_table.add_column("Bar", width=20)
        
        for name, chrom in genome.chromosomes.items():
            health = chrom.health
            if health >= 70:
                bar_color = "green"
            elif health >= 40:
                bar_color = "yellow"
            else:
                bar_color = "red"
            
            bar_filled = int(health / 5)
            bar = f"[{bar_color}]{'█' * bar_filled}{'░' * (20 - bar_filled)}[/{bar_color}]"
            
            chrom_table.add_row(
                chrom.name[:15],
                f"{health:.0f}%",
                bar
            )
        
        main_layout["chromosomes"].update(Panel(chrom_table, title="📊 Chromosomes"))
        
        # Gene details
        gene_table = Table(title="Gene Expression", box=box.SIMPLE, show_lines=True)
        gene_table.add_column("Gene", style="cyan", width=20)
        gene_table.add_column("Expr", justify="right", width=5)
        gene_table.add_column("Status", width=10)
        
        for chrom in list(genome.chromosomes.values())[:4]:  # Show first 4 chromosomes
            for gene in chrom.genes[:3]:  # Show first 3 genes per chromosome
                status_style = {
                    "ACTIVE": "green",
                    "DORMANT": "dim",
                    "MUTATING": "yellow",
                    "FAILED": "red"
                }.get(gene.status, "white")
                
                gene_table.add_row(
                    gene.name[:18],
                    f"{gene.expression_level:.0f}%",
                    f"[{status_style}]{gene.status}[/{status_style}]"
                )
        
        main_layout["genes"].update(Panel(gene_table, title="🧪 Active Genes"))
        
        layout["main"].update(main_layout)
        
        # Footer - Recent mutations
        mutations = list(self.scanner.mutation_history)[-5:]
        mutation_text = Text()
        mutation_text.append("Recent Mutations:\n", style="bold")
        
        for m in mutations:
            icon = "📈" if m.type == "ENHANCEMENT" else "📉" if m.type == "REGRESSION" else "➡️"
            mutation_text.append(f"  {icon} {m.description}\n", style="dim")
        
        if not mutations:
            mutation_text.append("  No recent mutations detected\n", style="dim")
        
        layout["footer"].update(Panel(mutation_text, title="🔬 Mutation Log"))
        
        return layout
    
    def run(self) -> None:
        """Run the dashboard"""
        if not HAS_RICH:
            print("Rich library required. Install with: pip install rich")
            return
        
        self.console.print("[bold cyan]🧬 Starting Empire DNA Evolution Tracker...[/bold cyan]\n")
        
        with Live(self.generate_display(), refresh_per_second=1, console=self.console) as live:
            while self.running:
                try:
                    # Scan infrastructure every 5 seconds
                    self.scanner.scan_infrastructure()
                    live.update(self.generate_display())
                    time.sleep(5)
                except KeyboardInterrupt:
                    self.running = False
                    break
        
        self.console.print("\n[cyan]🧬 DNA Tracker stopped. Long live the empire![/cyan]")


# ============================================================================
# CLI INTERFACE
# ============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Empire DNA Evolution Tracker - Real-time genome monitoring"
    )
    parser.add_argument("--once", action="store_true", help="Scan once and exit")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--save", type=str, help="Save genome snapshot to file")
    
    args = parser.parse_args()
    
    scanner = GenomeScanner()
    scanner.scan_infrastructure()
    
    if args.once:
        if args.json:
            print(json.dumps(scanner.to_dict(), indent=2))
        else:
            genome = scanner.get_genome()
            print(f"\n🧬 EMPIRE GENOME SNAPSHOT")
            print(f"{'='*50}")
            print(f"Version: {genome.version}")
            print(f"Generation: {genome.generation}")
            print(f"Fitness Score: {genome.fitness_score:.1f}%")
            print(f"\nChromosome Health:")
            for name, chrom in genome.chromosomes.items():
                bar = '█' * int(chrom.health / 5) + '░' * (20 - int(chrom.health / 5))
                print(f"  {chrom.name:20} [{bar}] {chrom.health:.0f}%")
    else:
        dashboard = DNADashboard(scanner)
        dashboard.run()
    
    if args.save:
        with open(args.save, 'w') as f:
            json.dump(scanner.to_dict(), f, indent=2)
        print(f"\nGenome saved to: {args.save}")


if __name__ == "__main__":
    main()
