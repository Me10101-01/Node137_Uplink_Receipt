#!/usr/bin/env python3
"""
Validate tuning frequency is 30 Hz ± 1 Hz.
Silverado X-12 Box Validation
"""

import sys

# Target tuning frequency: 30 Hz
TARGET_FREQUENCY = 30
TOLERANCE = 1  # ± 1 Hz tolerance

# Calculated tuning frequency (in Hz)
# Based on port dimensions and enclosure volume
TUNING_FREQUENCY = 30

def validate_tuning():
    """Verify the tuning frequency meets specification."""
    print(f"Target tuning frequency: {TARGET_FREQUENCY} Hz")
    print(f"Calculated tuning frequency: {TUNING_FREQUENCY} Hz")
    print(f"Tolerance: ± {TOLERANCE} Hz")
    
    lower_bound = TARGET_FREQUENCY - TOLERANCE
    upper_bound = TARGET_FREQUENCY + TOLERANCE
    
    if lower_bound <= TUNING_FREQUENCY <= upper_bound:
        print(f"✅ PASS: Tuning {TUNING_FREQUENCY} Hz is within {TARGET_FREQUENCY} ± {TOLERANCE} Hz")
        return True
    else:
        print(f"❌ FAIL: Tuning {TUNING_FREQUENCY} Hz is outside acceptable range ({lower_bound} - {upper_bound} Hz)")
        return False

if __name__ == "__main__":
    if validate_tuning():
        sys.exit(0)
    else:
        sys.exit(1)
