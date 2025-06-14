#!/usr/bin/env python3
"""
Security System Demo Script

Demonstrates the keycard and vault door security system in pixariMud.
Shows different access levels, error messages, and successful traversal.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from test_framework import EvenniaTestFramework


class SecurityDemo:
    """Handles security system demonstrations."""
    
    def __init__(self):
        self.framework = EvenniaTestFramework()
        
    def run_demo(self, demo_type="full"):
        """Run the specified security demo."""
        
        # Ensure server is running
        if not self.framework.check_server_status():
            print("\n[*] Starting Evennia server...")
            if not self.framework.start_server():
                print("[!] Failed to start server")
                return False
                
        # Connect to server
        print("\n[*] Connecting to server...")
        if not self.framework.connect():
            print("[!] Failed to connect to server")
            return False
            
        try:
            # Run the appropriate demo
            if demo_type == "full":
                self._full_security_demo()
            elif demo_type == "access_levels":
                self._access_levels_demo()
            elif demo_type == "specific_id":
                self._specific_id_demo()
            elif demo_type == "errors":
                self._error_messages_demo()
            else:
                print(f"[!] Unknown demo type: {demo_type}")
                return False
                
        finally:
            self.framework.disconnect()
            
        return True
        
    def _full_security_demo(self):
        """Complete demonstration of the security system."""
        print("\n" + "="*60)
        print("FULL SECURITY SYSTEM DEMONSTRATION")
        print("="*60)
        
        # Setup the demo area
        print("\n[*] Setting up security demo area...")
        self.framework.send_command("@batchcommand world/security_demo.ev")
        time.sleep(3)
        
        # Look around
        print("\n[*] Examining the security checkpoint...")
        self.framework.send_command("look")
        time.sleep(2)
        
        # Try doors without keycards
        print("\n[*] Testing doors without any keycards...")
        print("\n  -> Trying security door (north):")
        self.framework.send_command("north")
        time.sleep(2)
        
        print("\n  -> Trying laboratory entrance (east):")
        self.framework.send_command("east")
        time.sleep(2)
        
        print("\n  -> Trying command center (up):")
        self.framework.send_command("up")
        time.sleep(2)
        
        # Pick up standard keycard and try again
        print("\n[*] Testing with standard keycard...")
        self.framework.send_command("get standard")
        time.sleep(1)
        self.framework.send_command("inventory")
        time.sleep(1)
        
        print("\n  -> Trying security door with standard keycard:")
        self.framework.send_command("north")
        time.sleep(2)
        
        # Get security keycard
        print("\n[*] Testing with security keycard...")
        self.framework.send_command("get security")
        time.sleep(1)
        
        print("\n  -> Trying security door with security keycard:")
        self.framework.send_command("north")
        time.sleep(2)
        
        # Explore secure storage
        print("\n[*] Exploring secure storage...")
        self.framework.send_command("look")
        time.sleep(2)
        self.framework.send_command("get master")
        time.sleep(1)
        
        # Return to checkpoint
        print("\n[*] Returning to checkpoint...")
        self.framework.send_command("south")
        time.sleep(2)
        
        # Test laboratory with wrong keycard
        print("\n[*] Testing laboratory with wrong keycard...")
        self.framework.send_command("east")
        time.sleep(2)
        
        # Get lab keycard
        print("\n[*] Testing with correct lab keycard...")
        self.framework.send_command("get lab")
        time.sleep(1)
        self.framework.send_command("east")
        time.sleep(2)
        
        # Explore lab
        print("\n[*] Exploring laboratory...")
        self.framework.send_command("look")
        time.sleep(2)
        self.framework.send_command("west")
        time.sleep(2)
        
        # Test command center with master keycard
        print("\n[*] Testing command center with master keycard...")
        self.framework.send_command("up")
        time.sleep(2)
        
        # Explore command center
        print("\n[*] Exploring command center...")
        self.framework.send_command("look")
        time.sleep(2)
        
        print("\n[*] Security system demonstration complete!")
        
    def _access_levels_demo(self):
        """Demonstrate access level hierarchy."""
        print("\n" + "="*60)
        print("ACCESS LEVEL HIERARCHY DEMONSTRATION")
        print("="*60)
        
        # Setup
        self.framework.send_command("@batchcommand world/security_demo.ev")
        time.sleep(3)
        
        # Show hierarchy with security door
        print("\n[*] Security door requires 'security' level or higher...")
        
        access_tests = [
            ("standard", False),
            ("security", True),
            ("admin", True),
            ("master", True)
        ]
        
        for card_type, should_work in access_tests:
            print(f"\n[*] Testing with {card_type} keycard:")
            self.framework.send_command(f"get {card_type}")
            time.sleep(1)
            self.framework.send_command("north")
            time.sleep(2)
            
            if should_work:
                self.framework.send_command("south")
                time.sleep(1)
                
            self.framework.send_command(f"drop {card_type}")
            time.sleep(1)
            
    def _specific_id_demo(self):
        """Demonstrate ID-specific access control."""
        print("\n" + "="*60)
        print("ID-SPECIFIC ACCESS DEMONSTRATION")
        print("="*60)
        
        # Setup
        self.framework.send_command("@batchcommand world/security_demo.ev")
        time.sleep(3)
        
        print("\n[*] Laboratory requires specific keycard ID: LAB-7734")
        
        # Try with security keycard (wrong ID)
        print("\n[*] Testing with security keycard (no ID):")
        self.framework.send_command("get security")
        time.sleep(1)
        self.framework.send_command("east")
        time.sleep(2)
        
        # Try with admin keycard (wrong ID)  
        print("\n[*] Testing with admin keycard (no ID):")
        self.framework.send_command("drop security")
        self.framework.send_command("get admin")
        time.sleep(1)
        self.framework.send_command("east")
        time.sleep(2)
        
        # Try with correct lab keycard
        print("\n[*] Testing with laboratory keycard (ID: LAB-7734):")
        self.framework.send_command("drop admin")
        self.framework.send_command("get lab")
        time.sleep(1)
        self.framework.send_command("look lab")
        time.sleep(1)
        self.framework.send_command("east")
        time.sleep(2)
        
    def _error_messages_demo(self):
        """Demonstrate various error messages."""
        print("\n" + "="*60)
        print("ERROR MESSAGE DEMONSTRATION")
        print("="*60)
        
        # Setup
        self.framework.send_command("@batchcommand world/security_demo.ev")
        time.sleep(3)
        
        # No keycard error
        print("\n[*] Error: No keycard")
        self.framework.send_command("north")
        time.sleep(2)
        
        # Wrong access level error
        print("\n[*] Error: Insufficient access level")
        self.framework.send_command("get standard")
        time.sleep(1)
        self.framework.send_command("north")
        time.sleep(2)
        
        # Wrong ID error
        print("\n[*] Error: Wrong keycard ID")
        self.framework.send_command("drop standard")
        self.framework.send_command("get security")
        time.sleep(1)
        self.framework.send_command("east")
        time.sleep(2)
        
        # Master door with admin card
        print("\n[*] Error: High security door")
        self.framework.send_command("drop security")
        self.framework.send_command("get admin")
        time.sleep(1)
        self.framework.send_command("up")
        time.sleep(2)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run security system demonstrations")
    parser.add_argument(
        "--demo",
        choices=["full", "access_levels", "specific_id", "errors"],
        default="full",
        help="Which demo to run"
    )
    
    args = parser.parse_args()
    
    demo = SecurityDemo()
    if demo.run_demo(args.demo):
        print("\n[*] Demo completed successfully!")
    else:
        print("\n[!] Demo failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()