#!/usr/bin/env python3
"""
NPC Demo Script

Demonstrates various NPC behaviors in pixariMud:
- Scanner bot detection and reactions
- Whispering guide interactions
- Faction-based guard responses
- Merchant trading conversations

Usage:
    python tools/demo_npcs.py [--demo <type>]
    
Demo types:
    scanner - Scanner bot detection demo
    whisper - Whispering guide demo
    faction - Faction guard demo
    merchant - Merchant interaction demo
    full - Complete NPC demonstration (default)
"""

import sys
import time
import argparse
from test_framework import EvenniaTestFramework


class NPCDemoRunner:
    """Runs NPC interaction demonstrations."""
    
    def __init__(self):
        self.framework = EvenniaTestFramework()
        
    def run_scanner_demo(self):
        """Demonstrate scanner bot behaviors."""
        print("\n" + "="*60)
        print("SCANNER BOT DEMONSTRATION")
        print("="*60)
        
        commands = [
            # Travel to scanner area
            ("north", 2, "Moving to Scanner Security Zone"),
            ("look", 2, "Examining the security area"),
            
            # Scanner should detect us
            ("look scanner", 2, "The scanner bot notices us"),
            
            # Test scanner reactions to keywords
            ("say Hello scanner bot!", 3, "Speaking normally to scanner"),
            ("say I'm planning to attack the dummy", 3, "Saying suspicious words"),
            ("say Let me disable this scanner", 3, "Threatening the scanner directly"),
            
            # Leave and return to test pattern detection
            ("south", 2, "Leaving the area"),
            ("north", 2, "Returning - scanner tracks visits"),
            ("south", 2, "Leave again"),
            ("north", 2, "Third visit - pattern detected"),
            
            # Return to hub
            ("south", 2, "Returning to hub"),
        ]
        
        self.framework.run_command_sequence(commands, "Scanner Bot Demo")
        
    def run_whisper_demo(self):
        """Demonstrate whispering guide behaviors."""
        print("\n" + "="*60)
        print("WHISPERING GUIDE DEMONSTRATION")
        print("="*60)
        
        commands = [
            # Travel to whisper chambers
            ("east", 2, "Moving to Whisper Chambers"),
            ("look", 2, "Examining the quiet room"),
            
            # The guide should whisper a greeting
            ("look guide", 2, "The whispering guide notices us"),
            
            # Test loud vs quiet communication
            ("say HELLO GUIDE!", 3, "Speaking loudly - guide dislikes this"),
            ("whisper guide = hello", 3, "Whispering - guide appreciates this"),
            ("whisper guide = help", 3, "Asking for help quietly"),
            
            # Build trust
            ("whisper guide = I need guidance", 3, "Building trust"),
            ("whisper guide = tell me more", 3, "More trust building"),
            ("whisper guide = what secrets do you know?", 3, "Asking about secrets"),
            
            # Try loud speech again
            ("say YOU'RE VERY MYSTERIOUS!", 3, "Being loud again - losing trust"),
            
            # Return to hub
            ("west", 2, "Returning to hub"),
        ]
        
        self.framework.run_command_sequence(commands, "Whispering Guide Demo")
        
    def run_faction_demo(self):
        """Demonstrate faction guard behaviors."""
        print("\n" + "="*60)
        print("FACTION GUARD DEMONSTRATION")
        print("="*60)
        
        commands = [
            # First visit as neutral
            ("setfaction", 2, "Checking current faction (should be none)"),
            ("northeast", 2, "Approaching Tech Consortium checkpoint"),
            ("look", 2, "Guard should ask our business"),
            
            # Test neutral interactions
            ("say I'm just passing through", 3, "Neutral response"),
            ("say Tell me about the Tech Consortium", 3, "Asking about their faction"),
            
            # Return and change faction to ally
            ("southwest", 2, "Leaving checkpoint"),
            ("setfaction cyborg_union", 2, "Joining allied faction"),
            ("northeast", 2, "Returning as ally"),
            
            # Should get friendly reception
            ("say Technology is the future!", 3, "Speaking as ally"),
            
            # Change to enemy faction
            ("southwest", 2, "Leaving again"),
            ("setfaction nature_cult", 2, "Joining enemy faction"),
            ("northeast", 2, "Returning as enemy - guard warns us"),
            
            # Test hostile interaction
            ("say Nature will reclaim all!", 3, "Provocative statement"),
            ("southwest", 2, "Leaving before violence"),
            
            # Visit nature cult area as member
            ("northwest", 2, "Visiting Nature Cult grove"),
            ("look", 2, "Friendly reception from nature guard"),
            
            # Return to hub and clear faction
            ("southeast", 2, "Back to hub"),
            ("setfaction none", 2, "Clearing faction"),
        ]
        
        self.framework.run_command_sequence(commands, "Faction Guard Demo")
        
    def run_merchant_demo(self):
        """Demonstrate merchant interactions."""
        print("\n" + "="*60)
        print("MERCHANT INTERACTION DEMONSTRATION")
        print("="*60)
        
        commands = [
            # Visit market
            ("south", 2, "Going to Market Square"),
            ("look", 2, "Examining the marketplace"),
            
            # First interaction with merchant
            ("look merchant", 2, "Merchant greets new customer"),
            ("say Hello merchant!", 3, "Greeting the merchant"),
            ("say Show me your wares", 3, "Asking to see inventory"),
            
            # Ask about specific items
            ("say How much for the healing potion?", 3, "Asking about price"),
            ("say What does the scanner jammer do?", 3, "Asking about items"),
            ("say I'd like to buy an energy cell", 3, "Expressing purchase interest"),
            
            # Leave and return to test memory
            ("north", 2, "Leaving market"),
            ("south", 2, "Returning - merchant remembers us"),
            
            # More interactions
            ("say Do you have any special deals?", 3, "Haggling attempt"),
            ("say Thank you for your time", 3, "Polite farewell"),
            
            # Visit scavenger outpost
            ("west", 2, "Checking scavenger outpost"),
            ("look lookout", 2, "Scavenger notices us"),
            ("say Any good salvage today?", 3, "Casual interaction"),
            
            # Return to hub
            ("east", 2, "Back to market"),
            ("north", 2, "Returning to hub"),
        ]
        
        self.framework.run_command_sequence(commands, "Merchant Demo")
        
    def run_full_demo(self):
        """Run complete NPC demonstration."""
        print("\n" + "="*60)
        print("COMPLETE NPC DEMONSTRATION")
        print("="*60)
        print("\nThis demo showcases all NPC types and their unique behaviors.")
        print("NPCs in pixariMud can listen, react, and remember interactions.")
        print("="*60)
        
        # Initial setup
        setup_commands = [
            ("look", 2, "Starting in NPC Testing Hub"),
            ("help whisper", 2, "Learning about whisper command"),
            ("help setfaction", 2, "Learning about faction system"),
        ]
        
        print("\n--- Initial Setup ---")
        self.framework.run_command_sequence(setup_commands, "Setup")
        
        # Run each demo in sequence
        self.run_scanner_demo()
        time.sleep(2)
        
        self.run_whisper_demo()
        time.sleep(2)
        
        self.run_faction_demo()
        time.sleep(2)
        
        self.run_merchant_demo()
        
        print("\n" + "="*60)
        print("NPC DEMONSTRATION COMPLETE")
        print("="*60)
        print("\nKey NPC Features Demonstrated:")
        print("- Scanner Bot: Detects keywords, tracks visits, escalates threat")
        print("- Whispering Guide: Reacts to volume, builds trust, shares secrets")
        print("- Faction Guards: Check allegiance, react based on faction")
        print("- Merchant: Remembers customers, shows wares, handles queries")
        print("\nNPCs use memory, state tracking, and contextual responses!")
        

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Run pixariMud NPC demonstrations')
    parser.add_argument('--demo', 
                       choices=['scanner', 'whisper', 'faction', 'merchant', 'full'],
                       default='full',
                       help='Which demo to run (default: full)')
    
    args = parser.parse_args()
    
    runner = NPCDemoRunner()
    
    # First ensure we're connected
    if not runner.framework.test_connection():
        print("Failed to connect to Evennia. Ensure server is running.")
        return 1
        
    try:
        # Create the NPC world if needed
        print("\nSetting up NPC demo world...")
        setup_commands = [
            ("@batchcommand world/npc_demo_setup.ev", 5, "Creating NPC demo world"),
        ]
        runner.framework.run_command_sequence(setup_commands, "World Setup")
        
        # Run the requested demo
        if args.demo == 'scanner':
            runner.run_scanner_demo()
        elif args.demo == 'whisper':
            runner.run_whisper_demo()
        elif args.demo == 'faction':
            runner.run_faction_demo()
        elif args.demo == 'merchant':
            runner.run_merchant_demo()
        else:  # full
            runner.run_full_demo()
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")
        return 1
    finally:
        runner.framework.disconnect()
        
    return 0


if __name__ == "__main__":
    sys.exit(main())