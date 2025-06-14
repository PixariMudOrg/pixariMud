#!/usr/bin/env python3
"""
Demo Scripts for pixariMud Combat System

High-level scripts for demonstrating the combat, death, and respawn features.
These use the test framework to create automated demonstrations.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path to import test_framework
sys.path.append(str(Path(__file__).parent))
from test_framework import EvenniaTestFramework


class DemoRunner:
    """High-level demo runner for pixariMud features."""
    
    def __init__(self):
        self.framework = EvenniaTestFramework()
        
    def setup_demo_world(self):
        """Set up the demo world with all necessary objects."""
        print("=== Setting Up Demo World ===")
        
        if not self.framework.create_test_character():
            return False
            
        # Create demo objects using Evennia's create command
        setup_commands = [
            # Create demo room
            "@dig Demo Arena = demo_arena",
            "@teleport demo_arena",
            
            # Create combat dummy
            "@create/drop Combat Dummy:typeclasses.objects.CombatDummy",
            
            # Create bottomless pit  
            "@create/drop Bottomless Pit:typeclasses.objects.BottomlessPit",
            
            # Create worn-out dummy
            "@create/drop Worn-Out Dummy:typeclasses.objects.WornOutDummy",
            
            # Set room description
            "@desc here = A training arena with various combat objects. There is a combat dummy for training, a bottomless pit for testing death mechanics, and a worn-out dummy that can be destroyed.",
            
            "look"
        ]
        
        responses = self.framework.run_command_sequence(setup_commands, delay=1)
        
        # Check if setup was successful
        success = any("Combat Dummy" in r and "Bottomless Pit" in r for r in responses)
        
        if success:
            print("✓ Demo world setup completed")
        else:
            print("✗ Demo world setup failed")
            print("Note: Objects may need to be created manually via the game interface")
            
        return success
    
    def demo_basic_combat(self):
        """Demonstrate basic combat mechanics."""
        print("\n=== DEMO: Basic Combat Training ===")
        print("Demonstrating XP gain from hitting combat dummy...")
        
        commands = [
            "look",
            "stats",
            "look combat",
            "hit combat",
            "hit combat", 
            "hit combat",
            "hit combat",
            "hit combat",
            "stats",
            "look combat"
        ]
        
        self.framework.run_command_sequence(commands, delay=1.5)
        print("✓ Basic combat demo completed")
    
    def demo_death_respawn(self):
        """Demonstrate death and respawn mechanics."""
        print("\n=== DEMO: Death & Respawn System ===")
        print("Demonstrating character death and automatic respawn...")
        
        commands = [
            "setrespawn",  # Set current location as respawn point
            "stats",
            "look pit",
            "jump pit",  # This should kill the character
            "look",
            "stats"
        ]
        
        self.framework.run_command_sequence(commands, delay=2)
        print("✓ Death & respawn demo completed")
    
    def demo_worn_dummy(self):
        """Demonstrate destructible dummy mechanics."""
        print("\n=== DEMO: Destructible Combat Dummy ===")
        print("Demonstrating dummy destruction and respawn...")
        
        # Check dummy health first
        self.framework.send_command("look worn")
        
        # Hit it many times to destroy it
        print("Attacking worn-out dummy repeatedly...")
        for i in range(25):
            response = self.framework.send_command("hit worn")
            if "destroyed" in response or "collapses" in response:
                print(f"Dummy destroyed after {i+1} hits!")
                break
            time.sleep(0.3)
        
        # Wait a bit for respawn message
        time.sleep(5)
        self.framework.send_command("look")
        print("✓ Destructible dummy demo completed")
    
    def demo_level_progression(self):
        """Demonstrate character level progression."""
        print("\n=== DEMO: Character Progression ===")
        print("Demonstrating XP accumulation and leveling up...")
        
        self.framework.send_command("stats")
        
        # Hit dummy many times to gain levels
        print("Training extensively to gain levels...")
        for i in range(50):
            response = self.framework.send_command("hit combat")
            if "level" in response.lower() and "reached" in response.lower():
                print(f"LEVEL UP after {i+1} hits!")
                break
            if i % 10 == 9:
                self.framework.send_command("stats")
            time.sleep(0.2)
        
        self.framework.send_command("stats")
        print("✓ Character progression demo completed")
    
    def run_full_demo(self):
        """Run the complete demonstration."""
        print("==================================================")
        print("          PIXARIMUD COMBAT SYSTEM DEMO")
        print("==================================================")
        
        # Start server if needed
        if not self.framework.is_server_running():
            print("Starting Evennia server...")
            if not self.framework.start_server():
                print("Failed to start server. Please start manually with: evennia start")
                return False
        
        # Connect and setup
        if not self.framework.connect_telnet():
            print("Failed to connect to server")
            return False
        
        # Note: World setup requires manual creation of objects
        # since we can't easily script the @create commands
        print("\nNOTE: This demo assumes demo objects exist in the game world.")
        print("If objects don't exist, create them manually:")
        print("  @create/drop Combat Dummy:typeclasses.objects.CombatDummy")
        print("  @create/drop Bottomless Pit:typeclasses.objects.BottomlessPit") 
        print("  @create/drop Worn-Out Dummy:typeclasses.objects.WornOutDummy")
        print()
        
        # Create test character
        if not self.framework.create_test_character():
            print("Failed to create test character")
            return False
        
        # Run all demos
        try:
            self.demo_basic_combat()
            time.sleep(3)
            
            self.demo_level_progression()
            time.sleep(3)
            
            self.demo_death_respawn()
            time.sleep(3)
            
            self.demo_worn_dummy()
            
            print("\n==================================================")
            print("              DEMO COMPLETED!")
            print("==================================================")
            print("All combat system features have been demonstrated:")
            print("✓ XP gain from combat")
            print("✓ Character level progression") 
            print("✓ Death and respawn mechanics")
            print("✓ Destructible objects with timed respawn")
            
            return True
            
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
            return False
        except Exception as e:
            print(f"Demo failed with error: {e}")
            return False
        finally:
            self.framework.disconnect_telnet()


def main():
    """Main entry point for demo scripts."""
    import argparse
    
    parser = argparse.ArgumentParser(description="pixariMud Demo Scripts")
    parser.add_argument("--demo", 
                       choices=["combat", "death", "dummy", "progression", "npcs", "security", "shop", "full"],
                       default="full",
                       help="Which demo to run")
    
    args = parser.parse_args()
    
    demo = DemoRunner()
    
    try:
        if args.demo == "full":
            success = demo.run_full_demo()
        elif args.demo == "combat":
            demo.framework.connect_telnet()
            demo.framework.create_test_character()
            demo.demo_basic_combat()
            success = True
        elif args.demo == "death":
            demo.framework.connect_telnet()
            demo.framework.create_test_character()
            demo.demo_death_respawn()
            success = True
        elif args.demo == "dummy":
            demo.framework.connect_telnet()
            demo.framework.create_test_character()
            demo.demo_worn_dummy()
            success = True
        elif args.demo == "progression":
            demo.framework.connect_telnet()
            demo.framework.create_test_character()
            demo.demo_level_progression()
            success = True
        elif args.demo == "npcs":
            # Run the dedicated NPC demo script
            import subprocess
            result = subprocess.run([sys.executable, "tools/demo_npcs.py", "--demo", "full"])
            success = result.returncode == 0
        elif args.demo == "security":
            # Run the dedicated security demo script
            import subprocess
            result = subprocess.run([sys.executable, "tools/demo_security.py", "--demo", "full"])
            success = result.returncode == 0
        elif args.demo == "shop":
            # Run the dedicated shop demo script
            import subprocess
            result = subprocess.run([sys.executable, "tools/demo_shop.py"])
            success = result.returncode == 0
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()