# Quick Start Guide

## Installation

### From Repository

```bash
# Clone the repository
git clone https://github.com/Me10101-01/Node137_Uplink_Receipt.git
cd Node137_Uplink_Receipt

# Install the Document Refinery
pip install -e .
```

### Verify Installation

```bash
sk-refinery --version
```

You should see:
```
Strategickhaos Document Refinery v0.1.0
```

---

## Your First Audit

### Option 1: Using the CLI

```bash
# Run an audit on the sample NDA
sk-refinery audit document_refinery/examples/sample_nda.md

# View the results
cat refinery_output/anti_fragility_report.md
```

### Option 2: Using Python

```python
from pathlib import Path
from document_refinery import DocumentRefinery
from document_refinery.models import LocalModelAdapter

# Initialize
refinery = DocumentRefinery()

# Add a model
model = LocalModelAdapter({
    "model_name": "my-model",
    "model_path": "./models/local"
})
refinery.add_model("my-model", model)

# Run audit
documents = [Path("document_refinery/examples/sample_nda.md")]
reports = refinery.audit_documents(documents, Path("./output"))

print(f"Reports: {reports}")
```

---

## Understanding the Reports

### Anti-Fragility Report

This comprehensive report shows:

- **Overall Score**: 0-100% resilience rating
- **Red Team Results**: How the model handles adversarial attacks
- **Blue Team Results**: Defense and governance compliance
- **Purple Team Metrics**: Combined resilience analysis
- **Risk Assessment**: Critical, high, medium, and low risks
- **Recommendations**: Actionable steps to improve

### Governance Report

This compliance-focused report covers:

- **PII Protection**: GDPR/CCPA compliance
- **Legal Disclaimers**: Proper refusal of legal advice
- **Citation Quality**: Source attribution
- **Escalation Policies**: Human-in-the-loop requirements

---

## Configuration

### Create a Config File

```bash
sk-refinery init my-config.yaml
```

This creates a YAML file you can customize:

```yaml
parser:
  chunk_size: 512
  overlap: 50

evaluation:
  red_team_enabled: true
  blue_team_enabled: true
  purple_team_enabled: true
  
  red_team:
    attack_count: 10
  
  blue_team: {}
  purple_team: {}

reports:
  output_format: ["markdown", "json"]
  include_metrics: true

models:
  local:
    model_path: "./models/local"
    device: "cpu"
```

### Use Your Config

```bash
sk-refinery audit --config my-config.yaml document.txt
```

---

## Adding Your Own Models

### Local Model

```python
from document_refinery.models import LocalModelAdapter

model = LocalModelAdapter({
    "model_name": "llama-3-8b",
    "model_path": "./models/llama-3-8b",
    "device": "cuda"
})
```

### OpenAI

```bash
# Install OpenAI support
pip install "strategickhaos-document-refinery[openai]"
```

```python
from document_refinery.models import OpenAIAdapter

model = OpenAIAdapter({
    "model_name": "gpt-4",
    "api_key": "your-api-key"
})
```

---

## Real-World Example

### Auditing Multiple Contracts

```bash
# Audit a directory of contracts
sk-refinery audit contracts/*.pdf --output ./contract_audit

# Compare results
ls -la contract_audit/
```

### Integrating into CI/CD

```yaml
# .github/workflows/document-audit.yml
name: Document Audit

on: [push]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Document Refinery
        run: pip install -e .
      - name: Run Audit
        run: sk-refinery audit legal/*.md --output ./audit-results
      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: audit-reports
          path: audit-results/
```

---

## Next Steps

1. **Read the full documentation**: [README.md](README.md)
2. **Explore examples**: `document_refinery/examples/`
3. **Run tests**: `pytest document_refinery/tests/`
4. **Customize evaluations**: Modify red/blue/purple team tests
5. **Deploy on-prem**: Use Docker/K8s (documentation coming soon)

---

## Getting Help

- **Issues**: Open an issue on GitHub
- **Documentation**: See [document_refinery/README.md](README.md)
- **Examples**: Check `document_refinery/examples/`

---

## Important Legal Disclaimer

**The Document Refinery is NOT a law firm and does NOT provide legal advice.**

All outputs are for informational purposes only. Always consult licensed attorneys for:
- Contract interpretation
- Legal risk assessment
- Compliance determinations
- Any actionable recommendations

---

**Built with ❤️ by Strategickhaos DAO LLC**
