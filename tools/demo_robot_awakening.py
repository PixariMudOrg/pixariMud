#!/usr/bin/env python
"""
Demo script for the Robot Awakening narrative features.

This script demonstrates:
1. Robot part discovery and attachment
2. Movement restrictions without legs
3. Substance contamination system
4. Faction interactions
5. Scanner bot behavior
"""

import argparse
import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.demo_scripts import DemoRunner


class RobotAwakeningDemo(DemoRunner):
    """Demo runner for robot awakening features."""
    
    def demo_robot_assembly(self):
        """Demonstrate robot part discovery and assembly."""
        print("\n" + "="*60)
        print("ROBOT ASSEMBLY DEMO")
        print("="*60)
        
        # Show initial state
        self.send_command("parts")
        self.wait(2)
        
        print("\n[Demo] You start with only one arm attached. Let's find more parts!")
        
        # Try to move without legs
        print("\n[Demo] First, let's try to walk...")
        self.send_command("north")
        self.wait(2)
        
        print("\n[Demo] Can't walk without legs! Let's crawl to the scrap heap.")
        self.send_command("crawl east")
        self.wait(6)  # Crawling has a 5 second cooldown
        
        # Search for parts
        print("\n[Demo] Now let's search for robot parts...")
        self.send_command("search")
        self.wait(3)
        
        print("\n[Demo] There's a cooldown between searches. Let's check the heap status.")
        self.send_command("heapstatus")
        self.wait(2)
        
        # Try searching again (should fail due to cooldown)
        print("\n[Demo] Trying to search again immediately...")
        self.send_command("search")
        self.wait(2)
        
        print("\n[Demo] Waiting for cooldown to expire...")
        self.wait(20)
        
        # Search again
        print("\n[Demo] Searching again...")
        self.send_command("search")
        self.wait(3)
        
        # Look for parts and attach them
        print("\n[Demo] Let's see what parts we found...")
        self.send_command("look")
        self.wait(2)
        
        print("\n[Demo] Let's get and attach a leg if we found one...")
        self.send_command("get leg")
        self.wait(1)
        self.send_command("attach leg")
        self.wait(2)
        
        # Check our parts again
        print("\n[Demo] Checking our configuration...")
        self.send_command("parts")
        self.wait(2)
        
        # Run diagnostics
        print("\n[Demo] Running system diagnostics...")
        self.send_command("diagnostics")
        self.wait(3)
        
    def demo_substance_system(self):
        """Demonstrate the Substance contamination system."""
        print("\n" + "="*60)
        print("SUBSTANCE SYSTEM DEMO")  
        print("="*60)
        
        print("\n[Demo] Let's visit the contaminated zone...")
        
        # Navigate to contaminated area (adjust path as needed)
        self.send_command("walk west")  # Back to awakening chamber
        self.wait(2)
        self.send_command("north")  # To hub
        self.wait(2)
        self.send_command("north")  # To reconstruction
        self.wait(2)
        self.send_command("north")  # To neutral territory
        self.wait(2)
        self.send_command("east")   # To checkpoint with scanner bot
        self.wait(3)
        
        print("\n[Demo] The scanner bot should scan us automatically...")
        self.wait(3)
        
        # Check substance level
        print("\n[Demo] Checking our substance contamination...")
        self.send_command("substance")
        self.wait(2)
        
        # Go to contaminated zone
        print("\n[Demo] Entering the contaminated zone...")
        self.send_command("east")
        self.wait(3)
        
        # Interact with infected machine
        print("\n[Demo] There might be infected machines here...")
        self.send_command("look")
        self.wait(2)
        
        # Attack infected machine to risk contamination
        print("\n[Demo] Attacking an infected machine (risky!)...")
        self.send_command("hit infected")
        self.wait(3)
        
        # Check contamination again
        print("\n[Demo] Checking contamination after combat...")
        self.send_command("substance")
        self.wait(2)
        
        # Find decontamination
        print("\n[Demo] Let's find the decontamination facility...")
        self.send_command("south")  # To maintenance
        self.wait(2)
        self.send_command("north")  # Back
        self.wait(2)
        self.send_command("west")   # To checkpoint
        self.wait(2)
        self.send_command("west")   # To neutral
        self.wait(2)
        self.send_command("south")  # To decon facility
        self.wait(2)
        
        print("\n[Demo] Requesting decontamination...")
        self.send_command("decontaminate")
        self.wait(3)
        
    def demo_faction_interactions(self):
        """Demonstrate faction system interactions."""
        print("\n" + "="*60)
        print("FACTION SYSTEM DEMO")
        print("="*60)
        
        # Check faction standings
        print("\n[Demo] Checking our faction standings...")
        self.send_command("faction")
        self.wait(2)
        
        # Visit Cogborn area
        print("\n[Demo] Let's visit the Cogborn and see their recruitment attempts...")
        # Navigate to Cogborn area
        self.send_command("north")  # From decon to neutral
        self.wait(2)
        self.send_command("east")   # To checkpoint  
        self.wait(2)
        self.send_command("east")   # To contaminated
        self.wait(2)
        self.send_command("north")  # To hidden passage
        self.wait(2)
        self.send_command("east")   # To enlightenment chamber
        self.wait(3)
        
        print("\n[Demo] The Cogborn should try to convert us...")
        self.wait(3)
        
        # Try talking about substance
        print("\n[Demo] Let's ask about the Substance...")
        self.send_command("say What is the Substance?")
        self.wait(3)
        
        print("\n[Demo] They might offer to infect us. We'll decline for now.")
        self.send_command("say I need to think about it")
        self.wait(3)
        
        # Visit neutral traders
        print("\n[Demo] Let's go back and talk to neutral scavengers...")
        self.send_command("west")   # Back to passage
        self.wait(2)
        self.send_command("west")   # To contaminated  
        self.wait(2)
        self.send_command("west")   # To checkpoint
        self.wait(2)
        self.send_command("west")   # To neutral territory
        self.wait(2)
        
        print("\n[Demo] Talking to neutral NPCs...")
        self.send_command("say Hello, I'm new here")
        self.wait(3)
        
        self.send_command("say Tell me about the Executors")
        self.wait(3)
        
        self.send_command("say Where can I find a keycard?")
        self.wait(3)
        
    def demo_scanner_bot(self):
        """Demonstrate scanner bot behavior."""
        print("\n" + "="*60)
        print("SCANNER BOT DEMO")
        print("="*60)
        
        print("\n[Demo] Let's go back to the scanner bot...")
        self.send_command("east")  # To checkpoint
        self.wait(3)
        
        print("\n[Demo] The scanner bot patrols and scans for contamination.")
        self.wait(3)
        
        # If we have contamination, it should react differently
        print("\n[Demo] Our contamination level affects its response.")
        self.send_command("substance")
        self.wait(2)
        
    def demo_hidden_content(self):
        """Demonstrate finding hidden keycards and secrets."""
        print("\n" + "="*60) 
        print("HIDDEN CONTENT DEMO")
        print("="*60)
        
        print("\n[Demo] Let's search for hidden items...")
        
        # Go to maintenance room
        self.send_command("east")   # To contaminated
        self.wait(2)
        self.send_command("south")  # To maintenance  
        self.wait(2)
        
        print("\n[Demo] Looking around the maintenance room...")
        self.send_command("look")
        self.wait(2)
        
        print("\n[Demo] Examining the compartment...")
        self.send_command("examine compartment")
        self.wait(3)
        
        print("\n[Demo] Getting the keycard...")
        self.send_command("get keycard")
        self.wait(2)
        
        self.send_command("inventory")
        self.wait(2)
        
    def run_full_demo(self):
        """Run complete robot awakening demonstration."""
        print("\n" + "="*60)
        print("COMPLETE ROBOT AWAKENING DEMO")
        print("="*60)
        print("\nThis demo showcases the narrative-driven robot awakening experience.")
        print("You play as a robot with missing parts in the underdark of a city.")
        self.wait(3)
        
        # Connect and setup
        if not self.connect():
            return
            
        self.login()
        self.wait(2)
        
        # Make sure we start in the right location
        print("\n[Demo] Setting up starting location...")
        self.send_command("@tel Robot Awakening Chamber")
        self.wait(2)
        
        # Run all demos in sequence
        self.demo_robot_assembly()
        self.wait(2)
        
        self.demo_substance_system()
        self.wait(2)
        
        self.demo_faction_interactions()
        self.wait(2)
        
        self.demo_scanner_bot()
        self.wait(2)
        
        self.demo_hidden_content()
        
        print("\n" + "="*60)
        print("DEMO COMPLETE!")
        print("="*60)
        print("\nThe robot awakening system provides:")
        print("- Modular body assembly with gameplay effects")
        print("- Movement restrictions creating progression")  
        print("- Substance contamination as a risk/reward system")
        print("- Rich faction interactions with different approaches")
        print("- Environmental storytelling through NPCs and objects")
        print("- Hidden content rewarding exploration")
        
        self.disconnect()


def main():
    parser = argparse.ArgumentParser(description='Robot Awakening Demo Script')
    parser.add_argument('--demo', choices=['full', 'assembly', 'substance', 'factions', 'scanner', 'hidden'],
                       default='full', help='Which demo to run')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=4000, help='Server port')
    parser.add_argument('--player', default='demo_player', help='Player account name')
    parser.add_argument('--password', default='demo123', help='Player password')
    
    args = parser.parse_args()
    
    # Create demo runner
    demo = RobotAwakeningDemo(
        host=args.host,
        port=args.port,
        account_name=args.player,
        password=args.password
    )
    
    # Run selected demo
    if args.demo == 'full':
        demo.run_full_demo()
    elif args.demo == 'assembly':
        if demo.connect() and demo.login():
            demo.demo_robot_assembly()
            demo.disconnect()
    elif args.demo == 'substance':
        if demo.connect() and demo.login():
            demo.demo_substance_system()
            demo.disconnect()
    elif args.demo == 'factions':
        if demo.connect() and demo.login():
            demo.demo_faction_interactions()
            demo.disconnect()
    elif args.demo == 'scanner':
        if demo.connect() and demo.login():
            demo.demo_scanner_bot()
            demo.disconnect()
    elif args.demo == 'hidden':
        if demo.connect() and demo.login():
            demo.demo_hidden_content()
            demo.disconnect()


if __name__ == '__main__':
    main()