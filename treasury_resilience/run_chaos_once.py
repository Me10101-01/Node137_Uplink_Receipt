#!/usr/bin/env python3
# treasury_resilience/run_chaos_once.py
"""
CLI tool for running chaos tests against the revenue distribution system.

Usage:
    python -m treasury_resilience.run_chaos_once --iterations 100
    python -m treasury_resilience.run_chaos_once --chaos-prob 0.15 --iterations 50
"""

import argparse
import asyncio
import logging
import sys
import time
from typing import Dict, List

from .chaos_injector import FinancialChaosEngine
from .resilience_report_generator import generate_antifragility_report
from .revenue_distribution_service import RevenueDistributionService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def generate_fake_revenue_events(count: int) -> List[Dict]:
    """Generate fake revenue events for testing."""
    import random
    events = []
    for i in range(count):
        events.append({
            "amount": round(random.uniform(10.0, 1000.0), 2),
            "source_id": f"test_source_{i}",
            "timestamp": "2025-12-06T22:00:00Z",
        })
    return events


async def run_chaos_test(iterations: int, chaos_probability: float) -> None:
    """Run a chaos test session."""
    logger.info("🚀 Starting StrategicKhaos Financial Chaos Engine")
    logger.info("   Iterations: %d", iterations)
    logger.info("   Chaos Probability: %.2f", chaos_probability)
    logger.info("=" * 60)

    # Create service with chaos testing enabled
    import os
    os.environ["CHAOS_PROBABILITY"] = str(chaos_probability)
    service = RevenueDistributionService()

    # Generate test events
    events = generate_fake_revenue_events(iterations)

    # Run the batch processing
    try:
        await service.process_batch(events)
    except Exception as exc:
        logger.error("Batch processing encountered errors: %s", exc)

    # Generate report
    logger.info("=" * 60)
    logger.info("🔍 Generating Anti-Fragility Report")
    logger.info("=" * 60)

    report = generate_antifragility_report(service.chaos_engine)
    print("\n" + report)

    # Save report to file
    report_filename = f"chaos_report_{time.time():.0f}.md"
    with open(report_filename, "w") as f:
        f.write(report)
    logger.info("📄 Report saved to: %s", report_filename)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="StrategicKhaos Financial Chaos Engine - Resilience Testing CLI"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=50,
        help="Number of revenue events to process (default: 50)",
    )
    parser.add_argument(
        "--chaos-prob",
        type=float,
        default=0.10,
        help="Probability of chaos injection (0.0-1.0, default: 0.10)",
    )

    args = parser.parse_args()

    # Validate chaos probability
    if not (0.0 <= args.chaos_prob <= 1.0):
        logger.error("❌ chaos-prob must be between 0.0 and 1.0")
        return 1

    # Run the chaos test
    try:
        asyncio.run(run_chaos_test(args.iterations, args.chaos_prob))
        logger.info("✅ Chaos test session completed successfully")
        return 0
    except KeyboardInterrupt:
        logger.info("⚠️  Chaos test interrupted by user")
        return 130
    except Exception as exc:
        logger.exception("❌ Chaos test failed: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
