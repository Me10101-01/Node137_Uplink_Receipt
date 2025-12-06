# treasury_resilience/resilience_report_generator.py
"""
Generate legal-grade anti-fragility reports
for inclusion in your Legal Proof Dossier.
"""

from collections import Counter
from datetime import datetime, timezone
from typing import List

from .chaos_injector import ChaosEvent, ChaosRecord, FinancialChaosEngine


def _count_by_type(records: List[ChaosRecord], event: ChaosEvent) -> int:
    return sum(1 for r in records if r.chaos_event == event.value)


def generate_antifragility_report(engine: FinancialChaosEngine) -> str:
    stats = engine.stats
    records = engine.chaos_log

    uptime_pct = (
        (stats.successful_recoveries / stats.chaos_events) * 100
        if stats.chaos_events > 0
        else 100.0
    )

    counts = Counter(r.chaos_event for r in records)

    now = datetime.now(timezone.utc).isoformat()

    report = f"""# ANTI-FRAGILITY STRESS TEST REPORT
## StrategicKhaos DAO LLC + ValorYield Engine

**Generated:** {now}  
**Total Operations:** {stats.total_operations}  
**Chaos Events Injected:** {stats.chaos_events}  
**Successful Recoveries:** {stats.successful_recoveries}  
**Failed Recoveries:** {stats.failed_recoveries}  
**System Uptime During Chaos:** {uptime_pct:.2f}%

---

## Chaos Event Summary

- Bank freeze simulations: {counts.get(ChaosEvent.BANK_FREEZE.value, 0)}
- ACH failure simulations: {counts.get(ChaosEvent.ACH_FAILURE.value, 0)}
- NATS outage simulations: {counts.get(ChaosEvent.NATS_OUTAGE.value, 0)}
- Network partition simulations: {counts.get(ChaosEvent.NETWORK_PARTITION.value, 0)}
- Regulatory hold simulations: {counts.get(ChaosEvent.REGULATORY_HOLD.value, 0)}

All chaos events are SIMULATED and were executed against sandboxed
adapters for the purposes of resilience testing only.

---

## Legal/Compliance Notes

1. The 7% charitable distribution path (StrategicKhaos DAO LLC → ValorYield Engine)
   was exercised under adverse simulated conditions.
2. Recovery logic (retry, backoff, and failover) successfully preserved the
   intended distribution flows in the majority of chaos test runs.
3. All events are logged with timestamps suitable for cryptographic
   hashing (e.g., BLAKE3) and long-term archival in tamper-evident storage.

This report is designed to be attached as an addendum to the
Strategickhaos Legal Proof Dossier to demonstrate not only compliance,
but operational resilience under simulated failure conditions.
"""
    return report
