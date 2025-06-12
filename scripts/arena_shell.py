#!/usr/bin/env python3
import time

print("[🎮 Arena Shell] Strategickhaos reflex engine loaded.")

with open("/workspaces/Node137_Uplink_Receipt/reflexes/white_web_reflexes.glyph", "r") as f:
    reflexes = f.read().split("[")
    for reflex in reflexes:
        if "]" in reflex:
            block = "[" + reflex.split("]")[0] + "]"
            print(f"[⚔️ Reflex Triggered]: {block}")
            time.sleep(0.5)

print("[✅ Reflex execution complete]")
