# treasury_resilience/chaos_injector.py
"""
Financial Chaos Engineering Module
Simulates failures to prove system resilience.

IMPORTANT:
- This module must ONLY be wired to sandbox/mock banking adapters
  until everything is fully tested and cleared by counsel.
"""

import asyncio
import logging
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ChaosEvent(str, Enum):
    BANK_FREEZE = "bank_freeze_simulation"
    ACH_FAILURE = "ach_failure_simulation"
    NATS_OUTAGE = "nats_outage_simulation"
    NETWORK_PARTITION = "network_partition_simulation"
    REGULATORY_HOLD = "regulatory_hold_simulation"


@dataclass
class ChaosRecord:
    timestamp: str
    operation: str
    chaos_event: str
    simulated: bool = True
    metadata: Dict = field(default_factory=dict)


@dataclass
class ChaosStats:
    total_operations: int = 0
    chaos_events: int = 0
    successful_recoveries: int = 0
    failed_recoveries: int = 0


class FinancialChaosEngine:
    """
    Injects controlled failures into the financial distribution system.

    All events are SIMULATED and should be handled by higher-level
    services without touching real banking endpoints directly.
    """

    def __init__(self, chaos_probability: float = 0.1):
        if not (0.0 <= chaos_probability <= 1.0):
            raise ValueError("chaos_probability must be between 0 and 1")

        self.chaos_probability = chaos_probability
        self.chaos_log: List[ChaosRecord] = []
        self.stats = ChaosStats()

    async def maybe_inject_chaos(self, operation_type: str) -> Tuple[bool, Optional[ChaosEvent]]:
        """
        Randomly decide whether to inject chaos for an operation.
        Returns (should_fail, chaos_event).
        """
        self.stats.total_operations += 1

        if random.random() < self.chaos_probability:
            event: ChaosEvent = random.choice(list(ChaosEvent))
            record = ChaosRecord(
                timestamp=datetime.now(timezone.utc).isoformat(),
                operation=operation_type,
                chaos_event=event.value,
            )
            self.chaos_log.append(record)
            self.stats.chaos_events += 1
            logger.warning("🔥 CHAOS INJECTED: %s during %s", event.value, operation_type)
            return True, event

        return False, None

    # --- Individual simulation helpers ---------------------------------

    async def simulate_bank_freeze(self, duration_seconds: int = 30) -> None:
        """Simulate bank API being unavailable."""
        logger.info("💥 SIMULATING BANK FREEZE for %ss", duration_seconds)
        await asyncio.sleep(duration_seconds)
        logger.info("✅ Bank freeze simulation ended; proceeding to recovery path")

    async def simulate_ach_failure(self) -> Dict:
        """Simulate an ACH transfer rejection."""
        logger.info("💥 SIMULATING ACH FAILURE")
        return {
            "status": "failed",
            "error_code": "SIMULATED_ACH_FAILURE",
            "retry_eligible": True,
        }

    async def simulate_nats_outage(self, duration_seconds: int = 10) -> None:
        """Simulate the message bus being temporarily unavailable."""
        logger.info("💥 SIMULATING NATS OUTAGE for %ss", duration_seconds)
        await asyncio.sleep(duration_seconds)
        logger.info("✅ NATS outage simulation ended")

    async def simulate_network_partition(self, duration_seconds: int = 10) -> None:
        """Simulate a network partition between services."""
        logger.info("💥 SIMULATING NETWORK PARTITION for %ss", duration_seconds)
        await asyncio.sleep(duration_seconds)
        logger.info("✅ Network partition simulation ended")

    async def simulate_regulatory_hold(self, duration_seconds: int = 5) -> None:
        """Simulate a regulatory hold that delays, but does not block, processing."""
        logger.info("💥 SIMULATING REGULATORY HOLD for %ss", duration_seconds)
        await asyncio.sleep(duration_seconds)
        logger.info("✅ Regulatory hold simulation ended")
