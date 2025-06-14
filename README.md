# pixariMud 🤖

A narrative-driven MUD where players awaken as incomplete robots in the underdark of a dystopian city. Built with [Evennia](https://www.evennia.com/).

## Game Features

### 🦾 Robot Body Assembly
- Start with only one arm - find and attach missing limbs
- Different quality parts affect your stats and abilities
- Movement restricted without legs (must crawl)
- Modular system allows customization

### ☢️ The Substance
- Mysterious contamination spreading through the underdark
- Scanner bots detect contamination levels
- Choose to avoid it, embrace it, or seek decontamination
- Central to faction conflicts

### ⚔️ Three Factions
- **Executors**: Relentless destroyers following ancient protocols
- **Cogborn**: Substance-infected machines seeking "enlightenment"
- **Neutrals**: Unaligned survivors with varying personalities

### 🗝️ Multi-Level Progression
- 8 underground levels (Level -8 to Level 0/Surface)
- Keycard-locked vault doors between levels
- Hidden secrets and puzzles to discover
- Ultimate goal: reach the surface

## Quick Start

### Setup a Development Server

## Set up a virtual environment

After cloning, make your choice of virtual environment manager, such as `uv`, `poetry`, or `conda`; Here's a basic usage of `venv`:

```
python3 -m venv venv

# linux/*nix
source venv/bin/activate

# windows(?)
venv\bin\activate.bat
```

Install libraries.

```
pip install -r requirements.txt
```

Create your local db.

```
cd pixarimud
evennia migrate
```

## Start Evennia

If you used a package manager, you need to activate your virtual environment each time you return to the directory before using Evennia commands. (`source venv/bin/activate`)


Start the server.

```
evennia start -l
```

You'll need to configure a superuser account for your local instance.

## Stop Evennia

Evennia will run in the background. You need to stop the server, or it will keep listening for ports.

```
evennia stop
```

## Connect

Evennia listens on port 4000 for telnet connections, and 4005 for HTTP connections.

```
telnet localhost 4000
```

or browse to [http://localhost:4005](http://localhost:4005)

## Playing the Game

### First Time Setup

After connecting, create the robot world:

```
@batchcommand world/robot_world_setup.ev
```

This creates the complete robot awakening experience including starting areas, NPCs, and challenges.

### Essential Commands

**Robot Management:**
- `search` - Search scrap heaps for parts (20s cooldown)
- `attach <part>` - Install a robot part
- `detach <slot>` - Remove a part
- `parts` - View your configuration
- `diagnostics` - System check
- `crawl <direction>` - Move without legs

**Survival:**
- `substance` - Check contamination level
- `decontaminate` - Remove contamination (costs gold)
- `faction` - View faction standings
- `stats` - Character statistics

**Interaction:**
- `whisper <target> = <message>` - Private communication
- `say <message>` - Normal speech
- `hit <target>` - Attack
- `examine <object>` - Detailed inspection

### Running Demos

Test all features with the automated demo:

```bash
python tools/demo_robot_awakening.py --demo full
```

Or test specific systems:
- `--demo assembly` - Robot part system
- `--demo substance` - Contamination mechanics
- `--demo factions` - Faction interactions
- `--demo scanner` - Scanner bot behavior
- `--demo hidden` - Finding secrets

## Development

### Key Files

- `typeclasses/robots.py` - Core robot character system
- `typeclasses/robot_parts.py` - Body part mechanics
- `typeclasses/scrap_rooms.py` - Searchable heap rooms
- `typeclasses/substance_system.py` - Contamination system
- `typeclasses/factions.py` - Faction NPCs and reputation
- `world/robot_prototypes.py` - All robot-related prototypes
- `world/robot_world_setup.ev` - World creation batch file

### Documentation

- `CLAUDE.md` - General development guidance for AI assistants
- `CLAUDE_robot_docs.md` - Detailed robot system documentation
- `README_robot_awakening.md` - Player-focused game guide

## Contributing

This is an experimental narrative-driven MUD exploring themes of identity, evolution, and survival in a post-human world. Contributions that enhance the robot awakening experience are welcome!

## License

Built with [Evennia](https://www.evennia.com/) - see their license for the underlying framework.


