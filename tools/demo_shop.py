#!/usr/bin/env python3
"""
Shop System Demo Script

This script demonstrates the shop and trading system features in pixariMud.
It shows buying items, using consumables, and the economic system.
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.test_framework import EvenniaTestFramework


def run_shop_demo():
    """Run the complete shop system demonstration."""
    framework = EvenniaTestFramework()
    
    print("\n" + "="*60)
    print("PIXARIMUD SHOP SYSTEM DEMONSTRATION")
    print("="*60)
    
    # Connect to the game
    print("\n[1] Connecting to game server...")
    success, output = framework.connect_and_login("testplayer", "testpass123")
    if not success:
        print(f"Failed to connect: {output}")
        return
    
    print("\n[2] Setting up shop demo area...")
    commands = [
        "@batchcommand world/shop_demo_setup.ev",
    ]
    
    for cmd in commands:
        print(f"   Executing: {cmd}")
        framework.send_command(cmd)
        time.sleep(2)  # Give batch command time to complete
    
    print("\n[3] Testing character gold and stats...")
    demo_commands = [
        ("stats", "Display character statistics including gold"),
        ("gold", "Check current gold amount"),
    ]
    
    for cmd, description in demo_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[4] Testing shop interaction...")
    shop_commands = [
        ("look", "Examine the marketplace"),
        ("shop", "Open the shop interface with equipment merchant"),
        ("1", "Inspect iron sword"),
        ("buy", "Purchase iron sword"),
        ("back", "Return to shop menu"),
        ("quit", "Exit shop"),
    ]
    
    for cmd, description in shop_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[5] Testing inventory and gold after purchase...")
    post_purchase_commands = [
        ("inventory", "Check inventory for purchased item"),
        ("gold", "Check remaining gold"),
        ("look iron sword", "Examine the purchased sword"),
    ]
    
    for cmd, description in post_purchase_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[6] Testing potion merchant...")
    potion_commands = [
        ("look potion seller", "Examine the potion merchant"),
        ("shop potion", "Open shop with potion seller"),
        ("1", "Inspect health potion"),
        ("buy", "Purchase health potion"),
        ("back", "Return to shop menu"),
        ("2", "Inspect teleport scroll"),
        ("buy", "Purchase teleport scroll"),
        ("quit", "Exit shop"),
    ]
    
    for cmd, description in potion_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[7] Testing consumable items...")
    # First, let's take some damage
    damage_commands = [
        ("north", "Go to training arena"),
        ("hit dummy", "Take combat action (gain XP)"),
        ("hit worn", "Attack worn dummy multiple times"),
        ("hit worn", "Continue attacking"),
        ("hit worn", "More damage"),
        ("suicide", "Test death mechanics to lose health"),
        ("stats", "Check health after respawn"),
    ]
    
    for cmd, description in damage_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    # Now test healing
    heal_commands = [
        ("drink potion", "Use health potion"),
        ("stats", "Check health after healing"),
    ]
    
    for cmd, description in heal_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[8] Testing teleport scroll...")
    teleport_commands = [
        ("south", "Return to marketplace"),
        ("setrespawn", "Set respawn point here"),
        ("north", "Go to arena"),
        ("read scroll", "Use teleport scroll to return"),
        ("look", "Verify we're back at marketplace"),
    ]
    
    for cmd, description in teleport_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[9] Testing selling items back to merchant...")
    sell_commands = [
        ("shop", "Open shop interface"),
        ("sell", "Enter sell menu"),
        ("1", "Sell the iron sword back"),
        ("back", "Return to main shop"),
        ("quit", "Exit shop"),
        ("gold", "Check gold after selling"),
        ("inventory", "Verify sword was sold"),
    ]
    
    for cmd, description in sell_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(1)
    
    print("\n[10] Testing gold rewards from combat...")
    combat_reward_commands = [
        ("north", "Go to training arena"),
        ("stats", "Check current gold"),
    ]
    
    # Hit the worn dummy until it's destroyed
    for i in range(10):
        combat_reward_commands.append(("hit worn", f"Attack worn dummy ({i+1}/10)"))
    
    combat_reward_commands.extend([
        ("gold", "Check gold after destroying dummy"),
        ("stats", "Final statistics check"),
    ])
    
    for cmd, description in combat_reward_commands:
        print(f"\n   {description}:")
        print(f"   > {cmd}")
        output = framework.send_command(cmd)
        print(f"   {output}")
        time.sleep(0.5)
    
    print("\n" + "="*60)
    print("SHOP SYSTEM DEMO COMPLETED!")
    print("="*60)
    print("\nKey features demonstrated:")
    print("- Shop interface with browse/buy/sell functionality")
    print("- Multiple merchant types with different inventories")
    print("- Gold-based economy system")
    print("- Consumable items (potions, scrolls)")
    print("- Equipment items (weapons, armor, accessories)")
    print("- Gold rewards from defeating enemies")
    print("- Item inspection and inventory management")
    
    # Disconnect
    framework.disconnect()


if __name__ == "__main__":
    run_shop_demo()