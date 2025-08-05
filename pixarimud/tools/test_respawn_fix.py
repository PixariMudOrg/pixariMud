#!/usr/bin/env python3
"""
Test script to verify the WornOutDummy respawn mechanism works correctly
after fixing the TICKER_HANDLER callback issue.
"""
import sys
import os
import time

# Add parent directory to path so we can import test_framework
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_framework import EvenniaTestFramework

def test_respawn_mechanism():
    """Test the WornOutDummy respawn functionality."""
    framework = EvenniaTestFramework()
    
    # Define test scenario
    test_scenario = {
        "name": "worn_dummy_respawn_fix",
        "description": "Test WornOutDummy respawn after fixing TICKER_HANDLER",
        "commands": [
            # Create a test room and dummy
            ("@dig Test Arena", 2),
            ("Test Arena", 2),  # Go to the new room
            ("@create/drop Worn-Out Dummy:typeclasses.objects.WornOutDummy", 2),
            
            # Set respawn timer to 10 seconds for faster testing
            ("@py self.location.contents[-1].db.respawn_timer = 10", 2),
            
            # Show initial state
            ("look dummy", 2),
            
            # Hit the dummy repeatedly to destroy it
            ("hit dummy", 1),
            ("hit dummy", 1),
            ("hit dummy", 1),
            ("hit dummy", 1),
            ("hit dummy", 1),
            
            # Continue hitting until destroyed (100 hits total)
            # Using a loop approach
            *[("hit dummy", 0.2) for _ in range(95)],
            
            # Wait for respawn announcement
            ("look", 2),
            
            # Wait for respawn (10 seconds + buffer)
            ("", 12),
            
            # Check if dummy respawned
            ("look", 2),
            ("look dummy", 2),
            
            # Test hitting the respawned dummy
            ("hit dummy", 1),
            ("stats", 1),
        ]
    }
    
    print("\n=== Testing WornOutDummy Respawn Fix ===\n")
    
    try:
        # Ensure server is running
        if not framework.test_connection():
            print("Starting Evennia server...")
            framework.start_server()
            time.sleep(5)
        
        # Run the test
        success = framework.run_scenario(test_scenario)
        
        if success:
            print("\n✅ Test completed successfully!")
            print("The respawn mechanism appears to be working correctly.")
        else:
            print("\n❌ Test failed!")
            print("Check the output above for errors.")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
    
    return success

if __name__ == "__main__":
    test_respawn_mechanism()