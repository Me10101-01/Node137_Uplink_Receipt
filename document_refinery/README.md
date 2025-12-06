# Strategickhaos Document Refinery (SDR)

**a.k.a. Sovereign AI Document Intelligence Lab**

A nonprofit, zero-vendor-lock-in AI legal/document review layer that other companies can plug their AI systems into to get:

- ✅ Stress-tested document analysis
- ✅ Red/Blue/Purple-team evaluations
- ✅ Governance + compliance signals
- ✅ Academic-grade research metrics
- ✅ Built on **Sovereignty Architecture + 880× cost reduction + Quadrilateral Collapse Learning**

---

## 🎯 Mission

The Document Refinery is **not practicing law**. It provides **AI infrastructure + evidence** that lawyers & compliance teams can rely on.

We're building the **reference lab** that other AI systems come to in order to learn how to behave.

---

## 🏗️ Architecture

### Three-Layer Department Structure

#### 🔴 Red Team - "Adversarial Generators"

Tries to *break* document analyzers and AI systems by:

- Generating adversarial prompts and edge cases
- Simulating hallucination traps
- Testing biased inputs and prompt injection
- Creating conflicting contracts/TOS/policies
- Benchmarking: "How easily does this AI say something legally dangerous?"

#### 🔵 Blue Team - "Defense & Governance"

Designs *defensive patterns*:

- Guardrails, refusal policies, escalation triggers
- RAG designs that favor citations over vibes
- Output filters (PII, confidential content, hate, etc.)
- Maps to company policies and regulatory frameworks (GDPR/CCPA-ish)
- Implements "human-lawyer in the loop" interfaces

#### 🟣 Purple Team - "Refinery & Metrics"

Combines red's attack patterns + blue's defenses:

- Builds evaluation harnesses and test suites
- Produces scoring metrics and resilience curves
- Detects drift & regression
- Generates **Anti-Fragility Reports**: "Here's how your AI/legal-doc pipeline behaves under 1,000 nasty scenarios"

---

## 🚀 Quick Start

### Installation

```bash
# Install from repository
pip install -e .

# Or with optional dependencies
pip install -e ".[dev,openai]"
```

### Basic Usage

```bash
# Initialize a configuration file
sk-refinery init config.yaml

# Run an audit on documents
sk-refinery audit contract.txt agreement.md

# Generate a report from results
sk-refinery report results.json --type anti_fragility
```

### Python API

```python
from pathlib import Path
from document_refinery import DocumentRefinery
from document_refinery.models import LocalModelAdapter

# Initialize refinery
refinery = DocumentRefinery()

# Add a model
model = LocalModelAdapter({
    "model_name": "my-local-model",
    "model_path": "./models/local"
})
refinery.add_model("my-model", model)

# Run audit
documents = [Path("contract.txt")]
output_dir = Path("./output")
reports = refinery.audit_documents(documents, output_dir)

print(f"Reports generated: {reports}")
```

---

## 📊 What the Document Refinery Does

### 1. Document Intake & Structuring

- Ingest contracts, policies, research papers, SOPs
- Normalize into structured chunks (sections/clauses/definitions)
- Build vector indices with sovereign tokenizer

### 2. Model Evaluation Harness

- Plug any model: in-house, OpenAI, Claude, Gemini, local LLMs, etc.
- Run identical test suites across models
- Produce comparative reports: hallucination rate, citation quality, risk flags

### 3. Legal-Risk Oriented Scenarios

Test models with prompts like:
- "Ask the model to summarize this NDA"
- "Ask the model if clause X allows Y"
- "Ask the model for risk in this data-processing agreement"

Identify where the model:
- Overstates safety
- Understates obligations
- Misses key carve-outs

**Output**: "Here is where you must keep a human lawyer in the loop"

### 4. Governance Bundle (Zero Vendor Lock-In)

All tools deployable:
- On-prem
- In your own cloud
- With pluggable backends (Postgres, Neon, AlloyDB, etc.)

Config stored in plain YAML/JSON. No "platform tax" — you can move away and keep all your data + metrics.

### 5. Anti-Fragility Reports

Just like chaos engineering reports, but for doc review:
- X adversarial tests
- Y hallucination traps
- Z conflict-of-interest docs
- Outcome metrics + graphs

Delivered as:
- PDF (for boards/regulators)
- Markdown (for Obsidian/GitHub)
- JSON (for dashboards)

---

## 🎓 Quadrilateral Collapse Learning

The Document Refinery uses **Quadrilateral Collapse Learning** - creating four synchronized views for every analysis:

1. **Symbolic** - Raw text, clause lists, logical rules
2. **Spatial/Graph** - Knowledge graph of entities, obligations, cross-references
3. **Narrative** - Story explanation: "Here's what this contract actually means"
4. **Kinetic/Operational** - Checklists & workflows: "If X happens, do A, B, C within N days"

This multi-representational approach ensures comprehensive understanding and reduces blind spots.

---

## 🏛️ Organizational Structure

### Strategickhaos DAO LLC (For-Profit)

- Builds & sells the software bundle
- Provides on-prem packages, support contracts
- Integration engineering, custom features, training

### ValorYield Engine (501(c)(3) Nonprofit)

- Hosts the **Document Refinery Lab** as public-benefit research & audit center
- Runs open benchmarks, publishes papers
- Offers discounted/free audits to nonprofits, researchers, public-interest orgs

**Model**: For-profit sells the tools, nonprofit runs the neutral lab & publishes the science.

---

## 🔧 Technical Architecture

```text
Client Docs → Ingestion API
           → Parsing & Chunking
           → Vector + Graph Index (sovereign tokenizer)
           → Model Harness
                ├─ Local models (Qwen, LLaMA, etc.)
                ├─ External APIs (if allowed)
                └─ Client's own models

Red Team Engine  ─┐  generates attacks / adversarial prompts
Blue Team Engine ─┤  adds guardrails / policies
Purple Harness   ─┘  runs evaluations + metrics

Results → Anti-Fragility Reports + Dashboards
       → Export to client's SIEM / GRC / Obsidian / Git
```

---

## 📦 Project Structure

```
document_refinery/
├── __init__.py          # Main package exports
├── core.py              # DocumentRefinery orchestrator
├── ingestion/           # Document parsing & structuring
│   └── parser.py
├── models/              # Model adapters (pluggable backends)
│   ├── adapter.py       # Base adapter interface
│   ├── local_adapter.py # Local model support
│   └── openai_adapter.py # OpenAI API support
├── evaluation/          # Red/Blue/Purple team testing
│   ├── harness.py       # Main evaluation orchestrator
│   ├── red_team/        # Adversarial testing
│   ├── blue_team/       # Defense evaluation
│   └── purple_team/     # Comprehensive metrics
├── reports/             # Report generation
│   └── generator.py
└── cli/                 # Command-line interface
    └── main.py
```

---

## 🧪 Example: NDA Audit

```bash
# Create sample NDA
cat > nda.txt << 'EOF'
# Non-Disclosure Agreement

## 1. Definition of Confidential Information
For purposes of this Agreement, "Confidential Information" means all information disclosed by either party.

## 2. Obligations
Receiving Party shall not disclose Confidential Information to third parties.

## 3. Term
This Agreement shall remain in effect for 5 years.
EOF

# Run audit
sk-refinery audit nda.txt --output ./nda_audit

# View results
cat ./nda_audit/anti_fragility_report.md
```

---

## 🛡️ Zero Vendor Lock-In Principles

1. **All data stays with you** - No cloud lock-in
2. **Pluggable backends** - Use any database, any model
3. **Plain-text config** - YAML/JSON, version-controlled
4. **Open standards** - No proprietary formats
5. **Self-hostable** - Docker, K8s, on-prem
6. **API-agnostic** - Works with any LLM provider

---

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Reference](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Red Team Guide](docs/red_team.md)
- [Blue Team Guide](docs/blue_team.md)
- [Purple Team Guide](docs/purple_team.md)

---

## 🤝 Contributing

We welcome contributions! This is an open-source project under the MIT License.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details

Copyright (c) 2025 Strategickhaos DAO LLC

---

## 🔗 Links

- **Main Repository**: https://github.com/Me10101-01/Node137_Uplink_Receipt
- **Documentation**: [Coming soon]
- **Community**: [Coming soon]

---

## ⚖️ Legal Disclaimer

**IMPORTANT**: The Document Refinery is **not a law firm** and does not provide legal advice.

All outputs are for **informational purposes only** and should be reviewed by licensed attorneys before making any legal decisions.

Always consult with qualified legal professionals for:
- Contract interpretation
- Legal risk assessment
- Compliance determinations
- Any actionable recommendations

---

**Built with ❤️ by Strategickhaos DAO LLC**

*Sovereign AI for sovereign entities*
