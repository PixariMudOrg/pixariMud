# pixariMud Testing Tools

This directory contains AI-driven testing tools for automated development and demonstration of the pixariMud combat system.

## Files

### `test_framework.py`
Core testing framework that provides:
- **Server Management**: Start/stop Evennia server programmatically
- **Command Scripting**: Send automated command sequences to game
- **Output Capture**: Capture and log server responses
- **Test Scenarios**: Pre-built test scenarios for various game features

**Usage:**
```bash
# Start server
python tools/test_framework.py --action start_server

# Run test scenarios
python tools/test_framework.py --action run_scenario --scenario basic_combat
python tools/test_framework.py --action run_scenario --scenario death_respawn
python tools/test_framework.py --action run_scenario --scenario worn_dummy
python tools/test_framework.py --action run_scenario --scenario full_demo

# Stop server
python tools/test_framework.py --action stop_server

# Test connection
python tools/test_framework.py --action test_connection
```

### `demo_scripts.py`
High-level demonstration scripts that showcase the combat system features:
- **Basic Combat**: XP gain from hitting combat dummy
- **Death & Respawn**: Character death and automatic respawn
- **Destructible Objects**: Worn-out dummy that can be destroyed and respawns
- **Character Progression**: Level-up mechanics and stat progression

**Usage:**
```bash
# Run full demonstration
python tools/demo_scripts.py --demo full

# Run individual demos
python tools/demo_scripts.py --demo combat
python tools/demo_scripts.py --demo death
python tools/demo_scripts.py --demo dummy
python tools/demo_scripts.py --demo progression
```

## Prerequisites

Before running the tools:

1. **Start Evennia server** (if not using automated start):
   ```bash
   cd pixarimud
   evennia start
   ```

2. **Create demo objects** (run once):
   ```bash
   # Connect to the game as superuser and run:
   @batchcommand world/demo_setup.ev
   
   # OR create objects manually:
   @spawn COMBAT_DUMMY
   @spawn BOTTOMLESS_PIT
   @spawn WORN_DUMMY
   ```

3. **Ensure virtual environment is activated**:
   ```bash
   source venv/bin/activate  # Linux/macOS
   # venv\bin\activate.bat   # Windows
   ```

## Framework Features

### Automated Testing
- Connects to Evennia via telnet
- Creates test characters automatically
- Executes command sequences with configurable delays
- Captures and validates server responses
- Logs all interactions for debugging

### Server Management
- Start/stop Evennia server programmatically
- Check server status and health
- Handle server startup/shutdown timeouts
- Manage connection lifecycle

### Demo Scenarios
- **basic_combat**: Test XP gain from combat dummy
- **death_respawn**: Test death mechanics and respawn
- **worn_dummy**: Test destructible object mechanics
- **full_demo**: Complete demonstration of all features

### Output Logging
- Captures all command/response pairs
- Saves logs to files for analysis
- Color-coded output for easy reading
- Validation of expected game responses

## Development Workflow

1. **Make code changes** to game mechanics
2. **Run automated tests** to verify functionality:
   ```bash
   python tools/test_framework.py --action run_scenario --scenario full_demo
   ```
3. **Review output logs** for any issues
4. **Run specific demos** to showcase features:
   ```bash
   python tools/demo_scripts.py --demo full
   ```

## Technical Details

### Connection Method
- Uses Python's `telnetlib` for server communication
- Connects to default Evennia ports (4000 for telnet, 4005 for HTTP)
- Handles connection timeouts and retries
- Graceful disconnect handling

### Command Processing
- Sends commands with proper line endings
- Waits for expected responses or timeouts
- Captures both command echoes and server responses
- Handles Evennia's color codes and formatting

### Error Handling
- Connection failure recovery
- Server startup/shutdown error handling
- Command timeout management
- Graceful cleanup on interruption

## Extending the Framework

To add new test scenarios:

1. **Add scenario method** to `EvenniaTestFramework` class:
   ```python
   def scenario_my_feature(self):
       commands = ["command1", "command2", "command3"]
       responses = self.run_command_sequence(commands)
       return self.validate_responses(responses)
   ```

2. **Register scenario** in the `run_scenario` method
3. **Add demo script** in `demo_scripts.py` if needed

## Troubleshooting

### Server Won't Start
- Check if Evennia is properly installed
- Ensure database is migrated: `evennia migrate`
- Check for port conflicts (4000, 4005)
- Review server logs in `pixarimud/server/logs/`

### Connection Failures
- Verify server is running: `python tools/test_framework.py --action test_connection`
- Check firewall settings
- Ensure correct ports are configured

### Demo Objects Missing
- Run the batch setup: `@batchcommand world/demo_setup.ev`
- Manually create objects: `@spawn COMBAT_DUMMY` etc.
- Check prototype definitions in `world/prototypes.py`

### Command Timeouts
- Increase timeout values in framework calls
- Check server performance and load
- Verify commands are valid and working manually