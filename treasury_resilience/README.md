# Treasury Resilience - Financial Chaos Engineering

**StrategicKhaos DAO LLC Anti-Fragility Testing Framework**

This package implements a controlled chaos engineering system for testing financial distribution resilience, specifically designed for the StrategicKhaos DAO LLC revenue split model:

- **93%** → StrategicKhaos operations
- **7%** → ValorYield Engine (501(c)(3) charitable distribution)

## 🎯 Purpose

The Financial Chaos Engine proves system resilience by simulating real-world failure scenarios in a controlled, **sandbox-only environment**. This generates legally-compliant anti-fragility reports suitable for inclusion in the StrategicKhaos Legal Proof Dossier.

## 🔥 Chaos Events Simulated

1. **Bank Freeze** - Simulates banking API unavailability (30s default)
2. **ACH Failure** - Simulates payment rejection with retry eligibility
3. **NATS Outage** - Simulates message bus unavailability (10s default)
4. **Network Partition** - Simulates inter-service communication failure (10s default)
5. **Regulatory Hold** - Simulates compliance delay without blocking (5s default)

## 📦 Installation

```bash
# Navigate to repository root
cd /path/to/Node137_Uplink_Receipt

# No external dependencies required - uses Python stdlib only
# Python 3.8+ required for async/await and dataclasses
```

## 🚀 Quick Start

### Basic Usage

```bash
# Run with default settings (50 iterations, 10% chaos probability)
python3 -m treasury_resilience.run_chaos_once

# Run with custom settings
python3 -m treasury_resilience.run_chaos_once --iterations 100 --chaos-prob 0.15

# Help
python3 -m treasury_resilience.run_chaos_once --help
```

### Expected Output

```
2025-12-06 22:08:44 - INFO - 🚀 Starting StrategicKhaos Financial Chaos Engine
2025-12-06 22:08:44 - INFO -    Iterations: 10
2025-12-06 22:08:44 - INFO -    Chaos Probability: 0.50
2025-12-06 22:08:44 - INFO - Processing revenue event source=test_source_0 total=653.16
2025-12-06 22:08:44 - WARNING - 🔥 CHAOS INJECTED: bank_freeze_simulation during charitable_distribution
2025-12-06 22:08:44 - INFO - 💥 SIMULATING BANK FREEZE for 30s
...
2025-12-06 22:10:06 - INFO - ✅ CHAOS RECOVERY SUCCESSFUL for source=test_source_9
```

The tool will generate a markdown report:

```
📄 Report saved to: chaos_report_<timestamp>.md
```

## 📊 Anti-Fragility Report

After each run, the system generates a legal-grade report containing:

- **Total Operations** executed
- **Chaos Events Injected** (count and breakdown)
- **Successful/Failed Recoveries**
- **System Uptime During Chaos** (percentage)
- **Event Summary** by type
- **Legal/Compliance Notes** for dossier inclusion

### Sample Report

```markdown
# ANTI-FRAGILITY STRESS TEST REPORT
## StrategicKhaos DAO LLC + ValorYield Engine

**Generated:** 2025-12-06T22:10:06.431780+00:00  
**Total Operations:** 10  
**Chaos Events Injected:** 5  
**Successful Recoveries:** 5  
**Failed Recoveries:** 0  
**System Uptime During Chaos:** 100.00%

## Chaos Event Summary
- Bank freeze simulations: 2
- ACH failure simulations: 1
- NATS outage simulations: 1
- Network partition simulations: 0
- Regulatory hold simulations: 1
```

## 🔧 Programmatic Usage

### Python API

```python
import asyncio
from treasury_resilience import (
    FinancialChaosEngine,
    RevenueDistributionService,
    generate_antifragility_report,
)

async def main():
    # Create service with chaos testing enabled
    service = RevenueDistributionService()
    
    # Process revenue events
    events = [
        {"amount": 1000.00, "source_id": "tx_001"},
        {"amount": 500.00, "source_id": "tx_002"},
    ]
    
    await service.process_batch(events)
    
    # Generate report
    report = generate_antifragility_report(service.chaos_engine)
    print(report)

asyncio.run(main())
```

### Environment Variables

```bash
# Set chaos probability (0.0 - 1.0)
export CHAOS_PROBABILITY=0.15

# Run chaos test
python3 -m treasury_resilience.run_chaos_once
```

## 🔐 Security & Compliance

### ⚠️ CRITICAL SAFETY REQUIREMENTS

1. **SANDBOX ONLY**: This module MUST ONLY be connected to sandbox/mock banking adapters
2. **NO PRODUCTION USE**: Do not wire to real banking endpoints without explicit counsel approval
3. **Mock Adapters**: Default implementation uses `_mock_adapter` - replace with sandboxed APIs only

### Current Implementation

The `RevenueDistributionService` uses mock adapters by default:

```python
# Example: inject real adapters here
self._charity_adapter = self._mock_adapter  # replace
self._ops_adapter = self._mock_adapter      # replace
```

**DO NOT** replace these with production adapters until:
- ✅ Full testing completed in sandbox environment
- ✅ Legal counsel review and approval
- ✅ Compliance verification complete

## 🏗️ Architecture

### Module Structure

```
treasury_resilience/
├── __init__.py                          # Package exports
├── chaos_injector.py                    # Core chaos engine
├── revenue_distribution_service.py      # Distribution logic with chaos integration
├── resilience_report_generator.py       # Anti-fragility report generation
└── run_chaos_once.py                    # CLI tool
```

### Key Classes

**`FinancialChaosEngine`**
- Manages chaos injection probability
- Tracks statistics (total ops, chaos events, recoveries)
- Provides simulation methods for each chaos event type

**`RevenueDistributionService`**
- Implements 93/7 revenue split
- Integrates chaos testing
- Handles recovery from simulated failures

**`generate_antifragility_report()`**
- Generates legal-grade compliance reports
- Includes cryptographic hash-ready timestamps
- Suitable for Legal Proof Dossier inclusion

## ☸️ Kubernetes Deployment

For scheduled chaos testing in Kubernetes:

```yaml
# k8s/chaos-engine-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: strategickhaos-chaos-engine
  namespace: treasury
spec:
  schedule: "0 * * * *"  # hourly
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: Never
          containers:
            - name: chaos-runner
              image: ghcr.io/your-org/treasury-resilience:latest
              env:
                - name: CHAOS_PROBABILITY
                  value: "0.15"
              command: ["python", "-m", "treasury_resilience.run_chaos_once"]
```

Deploy with:

```bash
kubectl apply -f k8s/chaos-engine-cronjob.yaml
```

## 📝 Legal Proof Dossier Integration

### Step 1: Run Chaos Tests

```bash
python3 -m treasury_resilience.run_chaos_once --iterations 200 --chaos-prob 0.10
```

### Step 2: Collect Report

The generated `chaos_report_<timestamp>.md` file contains all necessary data.

### Step 3: Hash Report

```bash
# Generate cryptographic hash (BLAKE3 or SHA256)
blake3sum chaos_report_<timestamp>.md > chaos_report_hash.txt
# or
sha256sum chaos_report_<timestamp>.md > chaos_report_hash.txt
```

### Step 4: Archive

Store the following in your Legal Proof Dossier:

1. **Annex A**: Chaos Stress Test Report (the .md file)
2. **Annex B**: Selected Chaos Event Logs (optional excerpts)
3. **Annex C**: Cryptographic Hashes + Integrity Notes

This proves:
> "We don't just log. We prove we survive chaos."

## 🎨 Customization

### Adding New Chaos Events

Edit `chaos_injector.py`:

```python
class ChaosEvent(str, Enum):
    BANK_FREEZE = "bank_freeze_simulation"
    ACH_FAILURE = "ach_failure_simulation"
    # Add your new event:
    PAYMENT_PROCESSOR_TIMEOUT = "payment_processor_timeout"
```

Then add the simulation method:

```python
async def simulate_payment_processor_timeout(self, duration_seconds: int = 15) -> None:
    """Simulate payment processor timeout."""
    logger.info("💥 SIMULATING PAYMENT PROCESSOR TIMEOUT for %ss", duration_seconds)
    await asyncio.sleep(duration_seconds)
    logger.info("✅ Payment processor timeout simulation ended")
```

### Adjusting Chaos Probability

Control chaos frequency:

```python
# Low chaos (10%)
engine = FinancialChaosEngine(chaos_probability=0.10)

# Medium chaos (25%)
engine = FinancialChaosEngine(chaos_probability=0.25)

# High chaos (50%)
engine = FinancialChaosEngine(chaos_probability=0.50)
```

## 🧪 Testing

```bash
# Quick test (low iterations)
python3 -m treasury_resilience.run_chaos_once --iterations 5 --chaos-prob 0.5

# Standard test
python3 -m treasury_resilience.run_chaos_once --iterations 50 --chaos-prob 0.10

# Comprehensive test
python3 -m treasury_resilience.run_chaos_once --iterations 200 --chaos-prob 0.15
```

## 📚 Additional Resources

- [Chaos Engineering Principles](https://principlesofchaos.org/)
- [Anti-Fragility Concept](https://en.wikipedia.org/wiki/Antifragile_(book))
- StrategicKhaos DAO Legal Proof Dossier (internal)
- ValorYield Engine 501(c)(3) Compliance Documentation (internal)

## 🤝 Contributing

This is a sovereign StrategicKhaos DAO LLC project. For questions or contributions:

1. Open an issue in the Node137_Uplink_Receipt repository
2. Tag with `treasury-resilience` label
3. Reference this README in your proposal

## 📜 License

See [LICENSE](../LICENSE) in repository root.

## ⚡ Version History

- **v1.0.0** (2025-12-06): Initial implementation
  - Core chaos engine with 5 event types
  - Revenue distribution service integration
  - Anti-fragility report generation
  - CLI tool and Kubernetes CronJob example

---

**Built with sovereignty by StrategicKhaos DAO LLC**  
**Node 137 • Ratio Ex Nihilo • Financial Anti-Fragility**
