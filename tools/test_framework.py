#!/usr/bin/env python3
"""
AI-Driven Evennia Test Framework

This framework provides automated testing capabilities for Evennia/pixariMud development.
It can start/stop the server, create test characters, script commands, and capture outputs.

Usage:
    python tools/test_framework.py --action start_server
    python tools/test_framework.py --action run_scenario --scenario basic_combat
    python tools/test_framework.py --action stop_server
"""

import os
import sys
import time
import signal
import subprocess
import argparse
import threading
import socket
import telnetlib
import json
from pathlib import Path


class EvenniaTestFramework:
    """
    Main test framework class for automating Evennia interactions.
    """
    
    def __init__(self, game_dir=None):
        """Initialize the framework."""
        self.game_dir = Path(game_dir) if game_dir else Path(__file__).parent.parent / "pixarimud"
        self.server_process = None
        self.portal_process = None
        self.telnet_port = 4000
        self.http_port = 4005
        self.telnet_connection = None
        self.test_character = None
        self.output_log = []
        
    def start_server(self, timeout=30):
        """
        Start the Evennia server in the background.
        
        Args:
            timeout (int): Maximum time to wait for server startup
            
        Returns:
            bool: True if server started successfully
        """
        print(f"Starting Evennia server from {self.game_dir}")
        
        # Change to game directory
        os.chdir(self.game_dir)
        
        # Check if server is already running
        if self.is_server_running():
            print("Server is already running")
            return True
        
        try:
            # Start the server
            result = subprocess.run([
                "evennia", "start"
            ], capture_output=True, text=True, timeout=timeout)
            
            if result.returncode != 0:
                print(f"Failed to start server: {result.stderr}")
                return False
                
            # Wait for server to be fully ready
            for i in range(timeout):
                if self.is_server_running():
                    print(f"Server started successfully (took {i+1}s)")
                    return True
                time.sleep(1)
                
            print("Server startup timed out")
            return False
            
        except subprocess.TimeoutExpired:
            print("Server startup timed out")
            return False
        except Exception as e:
            print(f"Error starting server: {e}")
            return False
    
    def stop_server(self, timeout=10):
        """
        Stop the Evennia server.
        
        Args:
            timeout (int): Maximum time to wait for server shutdown
            
        Returns:
            bool: True if server stopped successfully
        """
        print("Stopping Evennia server")
        
        # Disconnect any active connections
        self.disconnect_telnet()
        
        # Change to game directory
        os.chdir(self.game_dir)
        
        try:
            # Stop the server
            result = subprocess.run([
                "evennia", "stop"
            ], capture_output=True, text=True, timeout=timeout)
            
            # Wait for server to fully stop
            for i in range(timeout):
                if not self.is_server_running():
                    print(f"Server stopped successfully (took {i+1}s)")
                    return True
                time.sleep(1)
                
            print("Server shutdown timed out")
            return False
            
        except subprocess.TimeoutExpired:
            print("Server shutdown timed out")
            return False
        except Exception as e:
            print(f"Error stopping server: {e}")
            return False
    
    def is_server_running(self):
        """
        Check if the Evennia server is running.
        
        Returns:
            bool: True if server is running
        """
        try:
            # Try to connect to the telnet port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', self.telnet_port))
            sock.close()
            return result == 0
        except:
            return False
    
    def connect_telnet(self, timeout=10):
        """
        Connect to the Evennia telnet server.
        
        Args:
            timeout (int): Connection timeout
            
        Returns:
            bool: True if connected successfully
        """
        try:
            self.telnet_connection = telnetlib.Telnet(
                'localhost', self.telnet_port, timeout
            )
            print("Connected to telnet server")
            
            # Read welcome message
            initial_output = self.telnet_connection.read_until(b"Account name:", timeout=5)
            self.output_log.append(initial_output.decode('utf-8', errors='ignore'))
            return True
            
        except Exception as e:
            print(f"Failed to connect to telnet: {e}")
            return False
    
    def disconnect_telnet(self):
        """Disconnect from telnet server."""
        if self.telnet_connection:
            try:
                self.telnet_connection.close()
                print("Disconnected from telnet server")
            except:
                pass
            self.telnet_connection = None
    
    def send_command(self, command, wait_for=None, timeout=5):
        """
        Send a command to the server and capture output.
        
        Args:
            command (str): Command to send
            wait_for (str): String to wait for in response
            timeout (int): Response timeout
            
        Returns:
            str: Server response
        """
        if not self.telnet_connection:
            print("Not connected to telnet server")
            return ""
            
        try:
            # Send command
            self.telnet_connection.write(f"{command}\n".encode('utf-8'))
            print(f"Sent: {command}")
            
            # Read response
            if wait_for:
                response = self.telnet_connection.read_until(
                    wait_for.encode('utf-8'), timeout
                )
            else:
                # Wait a short time for output
                time.sleep(0.5)
                response = self.telnet_connection.read_very_eager()
            
            response_text = response.decode('utf-8', errors='ignore')
            self.output_log.append(f"Command: {command}")
            self.output_log.append(f"Response: {response_text}")
            print(f"Received: {response_text.strip()}")
            
            return response_text
            
        except Exception as e:
            print(f"Error sending command: {e}")
            return ""
    
    def create_test_character(self, account_name="testaccount", password="testpass", char_name="TestChar"):
        """
        Create a test account and character.
        
        Args:
            account_name (str): Account name
            password (str): Account password  
            char_name (str): Character name
            
        Returns:
            bool: True if character created successfully
        """
        if not self.telnet_connection:
            if not self.connect_telnet():
                return False
        
        try:
            # Try to login first (in case account already exists)
            self.send_command(account_name)
            response = self.send_command(password, timeout=3)
            
            if "Welcome back" in response or "you are already logged in" in response.lower():
                print(f"Logged in as existing account: {account_name}")
                self.test_character = char_name
                return True
            
            # Account doesn't exist, create new one
            print("Creating new account...")
            self.send_command("create " + account_name + " " + password)
            self.send_command(password)  # Confirm password
            
            # Create character
            response = self.send_command(char_name, wait_for=">", timeout=10)
            
            if "Welcome to your new character" in response or ">" in response:
                print(f"Successfully created character: {char_name}")
                self.test_character = char_name
                return True
            else:
                print("Failed to create character")
                return False
                
        except Exception as e:
            print(f"Error creating test character: {e}")
            return False
    
    def run_command_sequence(self, commands, delay=1):
        """
        Run a sequence of commands with delays.
        
        Args:
            commands (list): List of commands to execute
            delay (float): Delay between commands
            
        Returns:
            list: List of responses
        """
        responses = []
        
        for command in commands:
            response = self.send_command(command)
            responses.append(response)
            time.sleep(delay)
            
        return responses
    
    def run_scenario(self, scenario_name):
        """
        Run a predefined test scenario.
        
        Args:
            scenario_name (str): Name of scenario to run
            
        Returns:
            bool: True if scenario completed successfully
        """
        scenarios = {
            "basic_combat": self.scenario_basic_combat,
            "death_respawn": self.scenario_death_respawn,
            "worn_dummy": self.scenario_worn_dummy,
            "full_demo": self.scenario_full_demo
        }
        
        if scenario_name not in scenarios:
            print(f"Unknown scenario: {scenario_name}")
            print(f"Available scenarios: {list(scenarios.keys())}")
            return False
        
        print(f"Running scenario: {scenario_name}")
        return scenarios[scenario_name]()
    
    def scenario_basic_combat(self):
        """Test basic combat with combat dummy."""
        print("=== Basic Combat Scenario ===")
        
        if not self.test_character:
            if not self.create_test_character():
                return False
        
        # Setup commands
        commands = [
            "look",
            "stats",
            "hit dummy",
            "hit dummy", 
            "hit dummy",
            "stats",
            "look dummy"
        ]
        
        responses = self.run_command_sequence(commands)
        
        # Validate results
        success = any("You gain 1 experience" in r for r in responses)
        if success:
            print("✓ Basic combat scenario completed successfully")
        else:
            print("✗ Basic combat scenario failed")
            
        return success
    
    def scenario_death_respawn(self):
        """Test death and respawn mechanics."""
        print("=== Death & Respawn Scenario ===")
        
        if not self.test_character:
            if not self.create_test_character():
                return False
        
        commands = [
            "look",
            "stats",
            "setrespawn",
            "jump pit",
            "look",
            "stats"
        ]
        
        responses = self.run_command_sequence(commands)
        
        # Validate results
        success = any("You have died" in r or "respawned" in r for r in responses)
        if success:
            print("✓ Death & respawn scenario completed successfully")
        else:
            print("✗ Death & respawn scenario failed")
            
        return success
    
    def scenario_worn_dummy(self):
        """Test worn-out dummy mechanics."""
        print("=== Worn-Out Dummy Scenario ===")
        
        if not self.test_character:
            if not self.create_test_character():
                return False
        
        # Hit the worn dummy many times to test destruction
        commands = ["look", "stats"]
        commands.extend([f"hit worn"] * 105)  # Should destroy it
        commands.extend(["look", "stats"])
        
        responses = self.run_command_sequence(commands, delay=0.2)
        
        # Validate results
        success = any("destroyed" in r or "collapses" in r for r in responses)
        if success:
            print("✓ Worn-out dummy scenario completed successfully")
        else:
            print("✗ Worn-out dummy scenario failed")
            
        return success
    
    def scenario_full_demo(self):
        """Run full demonstration of all features."""
        print("=== Full Demo Scenario ===")
        
        scenarios = ["basic_combat", "death_respawn", "worn_dummy"]
        results = []
        
        for scenario in scenarios:
            result = self.run_scenario(scenario)
            results.append(result)
            time.sleep(2)  # Brief pause between scenarios
        
        success = all(results)
        if success:
            print("✓ Full demo completed successfully")
        else:
            print("✗ Some scenarios failed in full demo")
            
        return success
    
    def get_output_log(self):
        """Get the complete output log."""
        return self.output_log
    
    def save_output_log(self, filename="test_output.log"):
        """Save output log to file."""
        try:
            with open(filename, 'w') as f:
                f.write("\n".join(self.output_log))
            print(f"Output log saved to {filename}")
        except Exception as e:
            print(f"Error saving log: {e}")


def main():
    """Main entry point for the test framework."""
    parser = argparse.ArgumentParser(description="Evennia Test Framework")
    parser.add_argument("--action", required=True, 
                       choices=["start_server", "stop_server", "run_scenario", "test_connection"],
                       help="Action to perform")
    parser.add_argument("--scenario", 
                       choices=["basic_combat", "death_respawn", "worn_dummy", "full_demo"],
                       help="Scenario to run (for run_scenario action)")
    parser.add_argument("--game-dir", 
                       help="Path to Evennia game directory")
    parser.add_argument("--output-log", 
                       help="Save output log to file")
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = EvenniaTestFramework(args.game_dir)
    
    try:
        if args.action == "start_server":
            success = framework.start_server()
            sys.exit(0 if success else 1)
            
        elif args.action == "stop_server":
            success = framework.stop_server()
            sys.exit(0 if success else 1)
            
        elif args.action == "test_connection":
            if framework.connect_telnet():
                print("Connection test successful")
                framework.disconnect_telnet()
                sys.exit(0)
            else:
                print("Connection test failed")
                sys.exit(1)
                
        elif args.action == "run_scenario":
            if not args.scenario:
                print("--scenario is required for run_scenario action")
                sys.exit(1)
                
            success = framework.run_scenario(args.scenario)
            
            # Save output log if requested
            if args.output_log:
                framework.save_output_log(args.output_log)
                
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        framework.disconnect_telnet()
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        framework.disconnect_telnet()
        sys.exit(1)


if __name__ == "__main__":
    main()