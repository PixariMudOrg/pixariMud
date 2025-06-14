#!/usr/bin/env python3
"""
Quick NPC test script to verify NPC system is working.

This creates a simple test scenario with one NPC of each type
and runs basic interaction tests.
"""

import sys
from test_framework import EvenniaTestFramework


def main():
    """Run basic NPC tests."""
    framework = EvenniaTestFramework()
    
    print("Testing NPC System...")
    print("-" * 40)
    
    if not framework.test_connection():
        print("ERROR: Cannot connect to Evennia server")
        return 1
        
    try:
        # Quick test sequence
        commands = [
            # Create a test room with NPCs
            ("@dig NPC Test Room", 2, "Creating test room"),
            ("@tel NPC Test Room", 2, "Moving to test room"),
            
            # Spawn one of each NPC type
            ("@spawn SCANNER_BOT", 2, "Creating scanner bot"),
            ("@spawn WHISPER_BOT", 2, "Creating whisper bot"),
            ("@spawn FACTION_GUARD", 2, "Creating faction guard"),
            ("@spawn MERCHANT_NPC", 2, "Creating merchant"),
            
            # Basic interaction tests
            ("look", 2, "Examining room with NPCs"),
            ("say Hello everyone!", 3, "Testing speech reaction"),
            ("whisper guide = hello", 3, "Testing whisper command"),
            ("setfaction tech_consortium", 2, "Setting faction"),
            
            # Check each NPC
            ("look scanner", 2, "Examining scanner bot"),
            ("look guide", 2, "Examining whisper bot"),
            ("look guard", 2, "Examining faction guard"),
            ("look merchant", 2, "Examining merchant"),
            
            # Cleanup
            ("@destroy scanner", 1, "Cleaning up scanner"),
            ("@destroy guide", 1, "Cleaning up guide"),
            ("@destroy guard", 1, "Cleaning up guard"),
            ("@destroy merchant", 1, "Cleaning up merchant"),
            ("@tel Limbo", 1, "Returning to Limbo"),
            ("@destroy NPC Test Room", 1, "Cleaning up test room"),
        ]
        
        success = framework.run_command_sequence(commands, "NPC System Test")
        
        if success:
            print("\n✓ NPC System Test PASSED")
            print("  - NPCs created successfully")
            print("  - Commands (whisper, setfaction) working")
            print("  - Basic interactions functioning")
        else:
            print("\n✗ NPC System Test FAILED")
            
    except Exception as e:
        print(f"\nERROR during test: {e}")
        return 1
    finally:
        framework.disconnect()
        
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())