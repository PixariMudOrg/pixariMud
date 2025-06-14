# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **pixariMud**, an Evennia-based MUD (Multi-User Dungeon) game. Evennia is a Python/Django framework for creating text-based multiplayer games. This repository contains game-specific customizations built on top of the Evennia engine.

## Development Setup

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\bin\activate.bat   # Windows

# Install dependencies
pip install -r requirements.txt

# Initialize database (run from pixarimud/ directory)
cd pixarimud
evennia migrate

# Start server (with logging to console)
evennia start -l

# Stop server
evennia stop
```

## Server Ports

- **4000**: Telnet connections (`telnet localhost 4000`)
- **4005**: HTTP web interface (`http://localhost:4005`)

## Architecture

### Core Evennia Patterns

**Typeclass System**: All game entities inherit from Evennia base classes
- `pixarimud/typeclasses/` - Custom game entity definitions
- Always inherit from Evennia defaults, never replace them
- Use `ObjectParent` mixin for shared functionality across all entities

**Command System**: Player interactions via structured commands
- `pixarimud/commands/command.py` - Custom command implementations  
- `pixarimud/commands/default_cmdsets.py` - Command organization and registration
- Commands inherit from `evennia.commands.command.Command`

### Key Directory Structure

```
pixarimud/
├── server/conf/        # Server configuration and hooks
│   └── settings.py     # Main config (SERVERNAME = "pixarimud")
├── typeclasses/        # Game entity definitions (characters, objects, rooms)
├── commands/           # Player command implementations
├── web/               # Django web interface customizations
└── world/             # Game content, prototypes, batch commands
```

### Entity Hierarchy

- **Account**: Player accounts (OOC entity)
- **Character**: Player avatars (inherit from Object)  
- **Object**: Items, NPCs, containers (base for most entities)
- **Room**: Locations (Objects with no location)
- **Exit**: Connections between rooms

### Hook-Driven Development

Evennia provides extensive hooks for customization:
- `at_object_creation()` - Run once when object created
- `at_pre_move()`/`at_post_move()` - Movement handling
- `return_appearance()` - How objects look when examined
- `at_pre_login()`/`at_post_login()` - Login process

### Data Persistence

- **Persistent attributes**: `obj.db.attribute_name = value`
- **Non-persistent**: `obj.ndb.temp_data = value`
- **Tags**: For categorization and searching
- **Locks**: Permission system using lock strings

## Development Principles

1. **Inherit, don't replace**: Always inherit from Evennia defaults
2. **Use hooks**: Leverage Evennia's hook system for customization  
3. **Call super()**: Preserve default behavior when overriding methods
4. **Separation of concerns**: 
   - Typeclasses define what entities ARE and CAN DO
   - Commands define what players CAN TELL the game to do
   - World files define specific game content
5. **Database-driven**: Everything important persists via Django ORM

## Common Development Tasks

- **Add custom commands**: Modify `commands/command.py` and register in `commands/default_cmdsets.py`
- **Customize entities**: Edit typeclasses in `typeclasses/` directory
- **World building**: Use `world/prototypes.py` for templates, `world/batch_cmds.ev` for programmatic creation
- **Web interface**: Customize templates in `web/templates/`, add routes in `web/*/urls.py`
- **Server behavior**: Modify hooks in `server/conf/` files

## Working Directory

All `evennia` commands must be run from the `pixarimud/` directory, not the repository root.

## Game Systems Implemented

### Character Progression System
**Location**: `pixarimud/typeclasses/characters.py`

**Core Stats:**
- `health` - Current health points (0 = dead)
- `max_health` - Maximum health capacity  
- `experience` - Total XP earned (persistent across sessions)
- `level` - Calculated from experience (100 XP per level)

**Key Methods:**
- `gain_experience(amount)` - Awards XP and handles level-up
- `take_damage(amount)` - Handles damage and death
- `heal(amount)` - Restores health (capped at max)
- `die()` - Death and respawn mechanics
- `set_respawn_location(location)` - Sets respawn point
- `ensure_stats_initialized()` - Backward compatibility for existing characters

**Level Progression:**
- Level 1: 0-99 XP, 100 max health
- Level 2: 100-199 XP, 110 max health  
- Level 3: 200-299 XP, 120 max health
- Each level adds +10 max health, full heal on level-up

### Combat System
**Location**: `pixarimud/commands/command.py`

**Commands Available:**
- `hit <target>` - Attack combat objects for XP
- `jump <target>` - Jump into dangerous objects  
- `stats` - Display character statistics
- `heal [amount]` - Restore health (testing command)
- `setrespawn` - Set current location as respawn point
- `suicide` - Test death mechanics (testing command)

**Aliases:**
- `hit` → `attack`, `strike`
- `jump` → `leap`  
- `stats` → `score`, `status`
- `setrespawn` → `respawn`

### Interactive Objects
**Location**: `pixarimud/typeclasses/objects.py`

#### CombatDummy
- **Purpose**: Basic combat training and XP farming
- **Interface**: `get_hit(attacker)` method
- **Behavior**: Awards 1 XP per hit, tracks hit count, indestructible
- **Usage**: `hit dummy` or `hit combat`

#### BottomlessPit  
- **Purpose**: Death/respawn mechanic testing
- **Interface**: `jump_into(jumper)` method
- **Behavior**: Instantly kills player, triggers respawn, tracks victims
- **Usage**: `jump pit` or `jump in pit`

#### WornOutDummy
- **Purpose**: Destructible object with respawn mechanics
- **Interface**: `get_hit(attacker)`, `die(killer)`, `respawn(location)` methods
- **Behavior**: 100 HP, awards 1 XP per hit, respawns after 60 seconds when destroyed
- **Usage**: `hit worn` repeatedly until destruction
- **Features**: Uses TICKER_HANDLER for timed respawn

### Object Creation and World Building

**Prototypes** (`world/prototypes.py`):
```python
# Spawn objects using prototypes
@spawn COMBAT_DUMMY
@spawn BOTTOMLESS_PIT  
@spawn WORN_DUMMY
@spawn DEMO_ROOM
@spawn RESPAWN_ROOM
```

**Batch Setup** (`world/demo_setup.ev`):
```bash
# Run complete world setup
@batchcommand world/demo_setup.ev
```

**Manual Creation**:
```bash
# Alternative object creation
@create/drop Combat Dummy:typeclasses.objects.CombatDummy
@create/drop Bottomless Pit:typeclasses.objects.BottomlessPit  
@create/drop Worn-Out Dummy:typeclasses.objects.WornOutDummy
```

### NPC System
**Location**: `pixarimud/typeclasses/npcs.py`

**Base NPC Class:**
- Inherits from `Character` class for full stat/combat capabilities
- `msg()` method intercepts all messages for listening
- Memory system tracks interactions with players
- State tracking (mood, faction, etc.)

**Key Methods:**
- `at_heard_say(message, speaker)` - React to normal speech
- `at_heard_whisper(message, whisperer)` - React to whispers
- `at_saw_emote(message, emoter)` - React to emotes
- `at_char_entered(character)` - React to arrivals
- `at_char_left(character)` - React to departures
- `remember_interaction()` - Store interaction history
- `get_interaction_count()` - Query past interactions

**NPC Types Implemented:**

#### ScannerBot
- **Purpose**: Security and threat detection
- **Behaviors**: 
  - Scans all arrivals and announces detection
  - Reacts to suspicious keywords in speech
  - Escalates threat level based on behavior
  - Tracks visit patterns

#### WhisperBot
- **Purpose**: Secretive guide that only whispers
- **Behaviors**:
  - Only communicates via whispers
  - Builds trust with players who whisper back
  - Recoils from loud speech
  - Shares secrets based on trust level

#### FactionGuard
- **Purpose**: Faction-based access control
- **Behaviors**:
  - Checks player faction on arrival
  - Friendly to allies, hostile to enemies
  - Warns then attacks hostile factions
  - Reacts to faction-related speech

#### MerchantNPC
- **Purpose**: Trading and commerce
- **Behaviors**:
  - Shows wares on request
  - Remembers customer interactions
  - Responds to trade keywords
  - Personalizes service for repeat customers

**Room Integration** (`pixarimud/typeclasses/rooms.py`):
- `at_object_receive()` - Notifies NPCs when players enter
- `at_object_leave()` - Notifies NPCs when players leave

**Commands Added** (`pixarimud/commands/command.py`):
- `whisper <target> = <message>` - Private communication
- `setfaction <faction>` - Set player faction for testing

**NPC Prototypes** (`pixarimud/world/prototypes.py`):
```python
@spawn SCANNER_BOT
@spawn WHISPER_BOT
@spawn FACTION_GUARD
@spawn MERCHANT_NPC
@spawn NATURE_GUARD
@spawn SCAVENGER_LOOKOUT
```

**Batch Setup** (`world/npc_demo_setup.ev`):
```bash
@batchcommand world/npc_demo_setup.ev
```

**Demo Script** (`tools/demo_npcs.py`):
```bash
python tools/demo_npcs.py --demo full      # All NPC demos
python tools/demo_npcs.py --demo scanner   # Scanner bot demo
python tools/demo_npcs.py --demo whisper   # Whisper guide demo
python tools/demo_npcs.py --demo faction   # Faction system demo
python tools/demo_npcs.py --demo merchant  # Merchant demo
```

### Security System (Keycards & Vault Doors)
**Location**: `pixarimud/typeclasses/objects.py`, `pixarimud/typeclasses/exits.py`

**Core Components:**

#### Keycard
- **Purpose**: Access control items for locked doors
- **Features**:
  - Four access levels: standard < security < admin < master
  - Optional unique ID for specific door access
  - Color-coded appearance by access level
  - Can be picked up by anyone

#### VaultDoor  
- **Purpose**: Secure exits requiring keycards
- **Features**:
  - Configurable access level requirements
  - Optional specific keycard ID requirement
  - Custom error messages based on failure reason
  - Visual/audio feedback on successful access
  - Builder permission bypass

**Lock System Integration** (`pixarimud/server/conf/lockfuncs.py`):
- Custom `holds_keycard()` lock function
- Checks both access level hierarchy and specific IDs
- Integrated with Evennia's lock system

**Security Prototypes** (`pixarimud/world/prototypes.py`):
```python
# Keycards
@spawn STANDARD_KEYCARD
@spawn SECURITY_KEYCARD  
@spawn ADMIN_KEYCARD
@spawn MASTER_KEYCARD
@spawn LAB_KEYCARD       # Has specific ID: LAB-7734

# Vault Doors
@spawn BASIC_VAULT_DOOR     # Requires security level
@spawn ADMIN_VAULT_DOOR     # Requires admin level
@spawn LAB_VAULT_DOOR       # Requires specific ID
@spawn MASTER_VAULT_DOOR    # Requires master level

# Demo Rooms
@spawn SECURITY_LOBBY
@spawn SECURE_STORAGE
@spawn LABORATORY
@spawn COMMAND_CENTER
```

**Batch Setup** (`world/security_demo.ev`):
```bash
@batchcommand world/security_demo.ev
```

**Demo Script** (`tools/demo_security.py`):
```bash
python tools/demo_security.py --demo full           # Complete security demo
python tools/demo_security.py --demo access_levels  # Access hierarchy demo
python tools/demo_security.py --demo specific_id    # ID-specific access demo
python tools/demo_security.py --demo errors         # Error messages demo
```

## AI-Driven Testing Framework

### Core Framework
**Location**: `tools/test_framework.py`

**Server Management:**
```bash
python tools/test_framework.py --action start_server    # Start Evennia
python tools/test_framework.py --action stop_server     # Stop Evennia  
python tools/test_framework.py --action test_connection # Test connectivity
```

**Test Scenarios:**
```bash
python tools/test_framework.py --action run_scenario --scenario basic_combat
python tools/test_framework.py --action run_scenario --scenario death_respawn
python tools/test_framework.py --action run_scenario --scenario worn_dummy
python tools/test_framework.py --action run_scenario --scenario full_demo
```

**Key Classes:**
- `EvenniaTestFramework` - Main automation class
- Server lifecycle management (start/stop/status)
- Telnet connection handling with automatic login
- Command sequence execution with configurable delays
- Output capture and logging with validation

### Demo Scripts
**Location**: `tools/demo_scripts.py`

**High-Level Demonstrations:**
```bash
python tools/demo_scripts.py --demo full        # Complete feature demo
python tools/demo_scripts.py --demo combat      # Basic combat training
python tools/demo_scripts.py --demo death       # Death/respawn mechanics  
python tools/demo_scripts.py --demo dummy       # Destructible objects
python tools/demo_scripts.py --demo progression # Character leveling
python tools/demo_scripts.py --demo security    # Keycard security system
```

**Demo Features:**
- Automated character creation and login
- Scripted command sequences demonstrating each feature
- Real-time output with explanatory messages
- Comprehensive testing of all game mechanics

### Framework Architecture

**Connection Management:**
- Telnet protocol via Python `telnetlib`
- Automatic account/character creation with fallback login
- Graceful connection handling and cleanup
- Configurable timeouts and retry logic

**Command Scripting:**
- Batch command execution with delays
- Response capture and validation  
- Output logging for debugging and analysis
- Support for complex multi-step scenarios

**Server Integration:**
- Programmatic Evennia server start/stop
- Health checking and status monitoring
- Log file management and error capture
- Cross-platform compatibility (Linux/macOS/Windows)

## Testing and Development Workflow

1. **Make code changes** to game mechanics
2. **Reload server**: `evennia reload` (from pixarimud/ directory)
3. **Run automated tests**:
   ```bash
   python tools/test_framework.py --action run_scenario --scenario full_demo
   ```
4. **Run live demos**:
   ```bash
   python tools/demo_scripts.py --demo full
   ```
5. **Review output logs** for validation and debugging

## Debugging and Troubleshooting

**Character Stats Issues:**
- Stats auto-initialize via `ensure_stats_initialized()` for backward compatibility
- Use `stats` command to verify character state
- Manual initialization: `@py self.db.experience = 0` etc.

**Object Creation Issues:**
- Verify prototypes are loaded: `@list_prototypes`
- Check typeclass paths in prototypes
- Use `@examine <object>` to inspect object state

**Testing Framework Issues:**
- Ensure server is running before tests
- Check telnet connectivity: `telnet localhost 4000`
- Review test logs for connection/command failures
- Verify virtual environment is activated

**Server Performance:**
- Use `evennia reload` instead of restart for faster development
- Monitor logs in `pixarimud/server/logs/`
- Check database locks: `@db_stats`