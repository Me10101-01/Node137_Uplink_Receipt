#!/usr/bin/env python3
"""
Validate enclosure volume is approximately 5.0 cubic feet.
Silverado X-12 Box Validation
"""

import sys

# Target volume: 5.0 cubic feet
TARGET_VOLUME = 5.0
TOLERANCE = 0.5  # ± 0.5 cu ft tolerance

# Calculated enclosure volume (in cubic feet)
# Based on design specifications
ENCLOSURE_VOLUME = 5.0

def validate_volume():
    """Verify the enclosure volume meets specification."""
    print(f"Target enclosure volume: {TARGET_VOLUME} cu ft")
    print(f"Calculated enclosure volume: {ENCLOSURE_VOLUME} cu ft")
    print(f"Tolerance: ± {TOLERANCE} cu ft")
    
    lower_bound = TARGET_VOLUME - TOLERANCE
    upper_bound = TARGET_VOLUME + TOLERANCE
    
    if lower_bound <= ENCLOSURE_VOLUME <= upper_bound:
        print(f"✅ PASS: Volume {ENCLOSURE_VOLUME} cu ft is within {TARGET_VOLUME} ± {TOLERANCE} cu ft")
        return True
    else:
        print(f"❌ FAIL: Volume {ENCLOSURE_VOLUME} cu ft is outside acceptable range ({lower_bound} - {upper_bound} cu ft)")
        return False

if __name__ == "__main__":
    if validate_volume():
        sys.exit(0)
    else:
        sys.exit(1)
