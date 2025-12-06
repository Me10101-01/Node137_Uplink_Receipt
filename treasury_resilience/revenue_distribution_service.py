# treasury_resilience/revenue_distribution_service.py
"""
Revenue distribution service with integrated chaos testing.

This is a skeleton; wire your real Sequence / NavyFed adapters where marked.
"""

import asyncio
import logging
import os
from typing import Dict, List

from .chaos_injector import (
    ChaosEvent,
    FinancialChaosEngine,
)

logger = logging.getLogger(__name__)


class RevenueDistributionService:
    """
    Handles revenue splits such as:
      - 93% → StrategicKhaos operations
      - 7%  → ValorYield Engine (501(c)(3))
    with optional chaos testing to validate resilience.
    """

    def __init__(self) -> None:
        chaos_prob = float(os.getenv("CHAOS_PROBABILITY", "0.10"))
        self.chaos_engine = FinancialChaosEngine(chaos_probability=chaos_prob)

        # Example: inject real adapters here
        self._charity_adapter = self._mock_adapter  # replace
        self._ops_adapter = self._mock_adapter      # replace

    # ------------------ Public API ------------------

    async def process_batch(self, revenue_events: List[Dict]) -> None:
        """
        Entry point; takes a batch of revenue events (e.g., from NATS)
        and executes distributions with chaos instrumentation.
        """
        for event in revenue_events:
            await self._execute_distributions(event)

    # ------------------ Core logic ------------------

    async def _execute_distributions(self, event: Dict) -> None:
        """
        Execute distributions WITH chaos instrumentation and recovery tracking.
        """
        amount = float(event["amount"])
        source_id = event.get("source_id", "unknown")

        charity_amount = round(amount * 0.07, 2)
        ops_amount = round(amount - charity_amount, 2)

        logger.info(
            "Processing revenue event source=%s total=%.2f ops=%.2f charity=%.2f",
            source_id, amount, ops_amount, charity_amount,
        )

        # MAYBE inject chaos before attempting any real transfer
        should_fail, chaos_event = await self.chaos_engine.maybe_inject_chaos(
            "charitable_distribution"
        )

        if should_fail and chaos_event:
            await self._handle_chaos_event(chaos_event)

        # attempt the "real" operations (here still mocked)
        try:
            await self._ops_adapter(ops_amount, event)
            await self._charity_adapter(charity_amount, event)

            if should_fail:
                self.chaos_engine.stats.successful_recoveries += 1
                logger.info("✅ CHAOS RECOVERY SUCCESSFUL for source=%s", source_id)

        except Exception as exc:  # noqa: BLE001
            logger.exception("❌ Distribution failed for source=%s: %s", source_id, exc)
            if should_fail:
                self.chaos_engine.stats.failed_recoveries += 1
            # re-raise or send to dead-letter queue, depending on policy
            raise

    async def _handle_chaos_event(self, event: ChaosEvent) -> None:
        """
        Route chaos events to appropriate simulation functions.
        """
        if event == ChaosEvent.BANK_FREEZE:
            await self.chaos_engine.simulate_bank_freeze(duration_seconds=30)

        elif event == ChaosEvent.ACH_FAILURE:
            result = await self.chaos_engine.simulate_ach_failure()
            logger.warning("ACH failure simulation result: %s", result)
            # e.g. wait, then proceed as a "retry"
            await asyncio.sleep(5)

        elif event == ChaosEvent.NATS_OUTAGE:
            await self.chaos_engine.simulate_nats_outage(duration_seconds=10)

        elif event == ChaosEvent.NETWORK_PARTITION:
            await self.chaos_engine.simulate_network_partition(duration_seconds=10)

        elif event == ChaosEvent.REGULATORY_HOLD:
            await self.chaos_engine.simulate_regulatory_hold(duration_seconds=5)

    # ------------------ Mock adapter (replace with real) ------------------

    @staticmethod
    async def _mock_adapter(amount: float, context: Dict) -> None:
        """
        Placeholder for real bank/Sequence adapter.
        Replace with an interface that talks to sandboxed APIs.
        """
        await asyncio.sleep(0.1)
        logger.info(
            "💸 MOCK TRANSFER executed amount=%.2f meta=%s",
            amount,
            {k: v for k, v in context.items() if k != "sensitive"},
        )
