# Scripts Directory

## Empire DNA Evolution Tracker

The Empire DNA Evolution Tracker (`empire_dna_tracker.py`) is a real-time monitoring tool for the StrategicKhaos ecosystem. It provides both a TUI dashboard and command-line interface for tracking the health and evolution of your empire's infrastructure.

### Features

- **Real-time Genome Monitoring**: Track the expression levels of all empire "genes" (components)
- **Chromosome Health Metrics**: Monitor health across 7 chromosomes (Legal, Infrastructure, AI, Security, Financial, Observability, DevTools)
- **Mutation Tracking**: Automatically detect and log significant changes in gene expression
- **Multiple Output Modes**: TUI dashboard, JSON export, or simple text output
- **Infrastructure Scanning**: Auto-detect Docker, Kubernetes, Ollama, and GitHub Codespaces

### Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

Note: The `rich` library is optional. Without it, the script falls back to simple text output.

### Usage

**Interactive TUI Dashboard** (requires `rich`):
```bash
python3 scripts/empire_dna_tracker.py
```

**Single Scan (Text Output)**:
```bash
python3 scripts/empire_dna_tracker.py --once
```

**JSON Output**:
```bash
python3 scripts/empire_dna_tracker.py --once --json
```

**Save Snapshot to File**:
```bash
python3 scripts/empire_dna_tracker.py --once --save genome_snapshot.json
```

### Genome Structure

The empire genome is organized into 7 chromosomes:

1. **LEGAL** (15% weight) - Legal entities (DAO LLC, SSSF LLC, ValorYield PBC)
2. **INFRA** (20% weight) - Infrastructure (Kubernetes, Docker, Codespaces, etc.)
3. **AI** (20% weight) - AI Systems (Claude, GPT, Grok, Gemini, etc.)
4. **SECURITY** (15% weight) - Security measures (GPG, 2FA, audits)
5. **FINANCIAL** (15% weight) - Financial systems (Treasury, distributions)
6. **OBSERVABILITY** (10% weight) - Monitoring and telemetry
7. **DEVTOOLS** (5% weight) - Development tools (IDEs, databases)

### Gene Status Types

- **ACTIVE** - Gene is functioning normally (green)
- **DORMANT** - Gene is inactive but available (dim)
- **MUTATING** - Gene is in transition/development (yellow)
- **FAILED** - Gene has encountered errors (red)

### Fitness Score

The overall fitness score is calculated as a weighted average of chromosome health, ranging from 0-100%. Higher scores indicate a healthier, more robust empire infrastructure.

### Example Output

```
🧬 EMPIRE GENOME SNAPSHOT
==================================================
Version: 1.0.0-alpha
Generation: 1
Fitness Score: 53.0%

Chromosome Health:
  Legal Entities       [██████████████░░░░░░] 70%
  Infrastructure       [██░░░░░░░░░░░░░░░░░░] 11%
  AI Systems           [██████████████░░░░░░] 71%
  Security             [███████████████░░░░░] 75%
  Financial            [████████░░░░░░░░░░░░] 40%
  Observability        [██████████░░░░░░░░░░] 50%
  Dev Tools            [███████████████░░░░░] 75%
```

### Other Scripts

- **arena_shell.py** - Strategickhaos reflex engine loader
- **gpt_echo.sh** - GPT echo utility
- **grok_echo.sh** - Grok echo utility
- **status.sh** - Status check utility
