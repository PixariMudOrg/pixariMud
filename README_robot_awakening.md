# PixariMud: Robot Awakening

A narrative-driven MUD where players awaken as incomplete robots in the underdark of a dystopian city.

## Quick Start

1. **Start the server** (from pixarimud/ directory):
   ```bash
   evennia start -l
   ```

2. **Create the robot world**:
   ```bash
   telnet localhost 4000
   # Login as admin
   @batchcommand world/robot_world_setup.ev
   ```

3. **Connect as a player**:
   - Telnet: `telnet localhost 4000`
   - Web: `http://localhost:4005`
   - Create new account and character

4. **Start playing**:
   - You begin with only one arm
   - Use `search` to find parts in the scrap heap
   - Use `get <part>` then `attach <part>` to install
   - Use `crawl <direction>` until you have legs
   - Explore and survive!

## Key Features

### 🤖 Robot Body Assembly
- Start with missing limbs
- Find and attach different quality parts
- Parts affect your stats and abilities
- Movement restricted without legs

### ☢️ The Substance
- Mysterious contamination spreading through the underdark
- Scanner bots detect contamination levels
- Infected machines attack and spread it
- Choose: avoid it, embrace it, or cleanse it

### ⚔️ Three Factions
- **Executors**: Relentless destroyers following ancient protocols
- **Cogborn**: Substance-infected seeking "enlightenment"
- **Neutrals**: Unaligned survivors just trying to exist

### 🗝️ Level Progression
- 8 underground levels from -8 to 0 (surface)
- Keycard-locked vault doors between levels
- Each level has unique challenges and rewards
- Ultimate goal: reach the surface

## Essential Commands

### Robot Commands
- `search` - Look for parts in scrap heaps (20s cooldown)
- `attach <part>` - Install a robot part
- `detach <slot>` - Remove a part
- `parts` - View your components
- `diagnostics` - System check
- `crawl <direction>` - Move without legs

### Survival Commands  
- `substance` - Check contamination level
- `decontaminate` - Remove contamination (costs gold)
- `faction` - View faction standings
- `stats` - Character statistics

### Interaction
- `whisper <target> = <message>` - Private communication
- `say <message>` - Speak normally
- `hit <target>` - Attack
- `examine <object>` - Detailed look

## Running the Demo

```bash
# Complete demonstration
python tools/demo_robot_awakening.py --demo full

# Feature-specific demos
python tools/demo_robot_awakening.py --demo assembly
python tools/demo_robot_awakening.py --demo substance  
python tools/demo_robot_awakening.py --demo factions
```

## Game Flow

1. **Awakening Phase**: Find essential parts to gain mobility
2. **Exploration Phase**: Navigate Level -8 and meet factions
3. **Survival Phase**: Manage contamination and faction relations
4. **Progression Phase**: Find keycards and ascend levels
5. **End Game**: Reach the surface (not yet implemented)

## Tips for New Players

- Search multiple times - the scrap heap has many parts
- Quality matters - better parts give better stats
- Scanner bots are harmless unless you're contaminated
- Executors attack on sight - avoid or be prepared
- Cogborn will try to convert you - choose wisely
- Neutral traders have valuable information
- Hidden keycards unlock progression

## Development

See `CLAUDE_robot_docs.md` for complete technical documentation.

### Adding Content
- New robot parts: `typeclasses/robot_parts.py`
- New NPCs: `typeclasses/factions.py`
- New rooms: Use prototypes in `world/robot_prototypes.py`
- New areas: Extend `world/robot_world_setup.ev`

### Testing
```bash
# Run automated tests
python tools/test_framework.py --action run_scenario --scenario robot_awakening

# Manual testing with demo account
python tools/demo_robot_awakening.py --demo full
```

## Known Issues

- Guild system not yet implemented
- Surface levels (above -7) not yet created
- Part trading/shops not implemented
- Some faction quest lines incomplete

## Credits

Built with [Evennia](https://www.evennia.com/) - the Python MUD/MU* creation system.