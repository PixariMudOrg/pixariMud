# Robot Awakening Systems Documentation

## Core Robot Systems

### Robot Body Assembly
**Location**: `pixarimud/typeclasses/robots.py`, `pixarimud/typeclasses/robot_parts.py`

**Character System:**
- All characters are robots (`RobotCharacter` class)
- Start with only one arm attached
- Must find and attach body parts to gain functionality
- Movement restricted without legs (must crawl)
- Stats determined by attached part quality

**Part Types:**
- **Arms**: Enable manipulation commands (grab, powergrip)
- **Legs**: Enable normal movement (without legs, must crawl)
- **Head**: Provides scanning abilities and sensor commands
- **Torso**: Increases defense and overall integrity

**Part Quality Levels:**
- Damaged (50-70% effectiveness)
- Standard (80-100% effectiveness)
- Enhanced (110-130% effectiveness)
- Pristine (140-160% effectiveness)

**Key Commands:**
- `search` - Search scrap heaps for parts (20 second cooldown)
- `attach <part>` - Attach a part to your body
- `detach <slot>` - Remove an attached part
- `parts` - View your attached components
- `crawl <direction>` - Move without legs (5 second cooldown)
- `diagnostics` - Full system check

### Scrap Heap Rooms
**Location**: `pixarimud/typeclasses/scrap_rooms.py`

**Features:**
- Searchable rooms containing robot parts
- Cooldown system between searches
- Part quality and availability tracking
- Automatic restocking over time
- Special starting heap with guaranteed essential parts

**Room Types:**
- `StartingScrapHeap` - Guarantees finding legs and arm
- `ScrapHeapRoom` - General scrap areas with random parts
- Premium heaps with better quality modifiers

### The Substance System
**Location**: `pixarimud/typeclasses/substance_system.py`

**Core Mechanics:**
- Mysterious contamination that transforms robots
- Spreads through contact with infected machines/crystals
- Affects stats and NPC interactions
- Can be removed at decontamination stations

**Contamination Levels:**
- 0: Clean
- 1-2: Minor contamination
- 3-4: Moderate contamination  
- 5-6: High contamination
- 7-8: Critical contamination
- 9-10: Maximum saturation

**NPCs:**
- **Scanner Bot**: Detects and announces contamination levels
- **Infected Machines**: Hostile NPCs that spread substance
- **Decontamination Unit**: Removes contamination for gold

**Commands:**
- `substance` - Check your contamination level
- `decontaminate` - Use decon station (costs gold)

### Faction System
**Location**: `pixarimud/typeclasses/factions.py`

**Three Main Factions:**

1. **The Executors**
   - Hostile destroyer robots
   - Attack all non-Executors on sight
   - Serve ancient termination protocols
   - Drop gold and special items

2. **The Cogborn**
   - Infected by the Substance
   - Try to convert players to their cause
   - Become hostile if repeatedly rejected
   - Can infect players who accept

3. **Neutral Scavengers**  
   - Unaligned survivors
   - Various personalities (trader, paranoid, helpful, grizzled)
   - Provide information and trading
   - React based on keywords

**Reputation System:**
- Track standing with each faction (-100 to +100)
- Actions affect reputation
- Reputation affects NPC reactions

**Commands:**
- `faction` - View faction standings
- `accept` - Accept Cogborn conversion (when offered)

## Setup and Demo

### World Setup
```bash
# Create the complete robot world
@batchcommand world/robot_world_setup.ev
```

This creates:
- Starting awakening chamber and scrap heap
- Level -8 hub and various locations
- Scanner bots and faction NPCs
- Contaminated zones and decon facilities
- Hidden keycards and secrets

### Prototypes
**Location**: `pixarimud/world/robot_prototypes.py`

```python
# Robot Parts
@spawn DAMAGED_ARM
@spawn STANDARD_LEG
@spawn ENHANCED_HEAD
@spawn PRISTINE_TORSO

# Scrap Heaps
@spawn STARTING_SCRAP_HEAP
@spawn GENERAL_SCRAP_HEAP
@spawn PREMIUM_SCRAP_HEAP

# Substance System
@spawn SCANNER_BOT_PATROL
@spawn INFECTED_MACHINE_WEAK
@spawn DECONTAMINATION_UNIT
@spawn SUBSTANCE_CRYSTAL

# Faction NPCs
@spawn EXECUTOR_SCOUT
@spawn COGBORN_INITIATE
@spawn NEUTRAL_TRADER
@spawn WHISPERING_GUIDE
```

### Demo Script
**Location**: `tools/demo_robot_awakening.py`

```bash
# Full robot awakening demo
python tools/demo_robot_awakening.py --demo full

# Individual feature demos
python tools/demo_robot_awakening.py --demo assembly    # Part system
python tools/demo_robot_awakening.py --demo substance   # Contamination
python tools/demo_robot_awakening.py --demo factions    # Faction interactions
python tools/demo_robot_awakening.py --demo scanner     # Scanner bot
python tools/demo_robot_awakening.py --demo hidden      # Finding secrets
```

## Gameplay Flow

1. **Awakening**: Player starts with only one arm in a scrap heap
2. **Part Collection**: Search for legs and other parts
3. **Movement Progression**: Crawl → Limp → Walk as parts are found
4. **Exploration**: Navigate Level -8 discovering factions and dangers
5. **Contamination Risk**: Encounter substance and infected machines
6. **Faction Politics**: Choose alliances or remain neutral
7. **Level Progression**: Find keycards to access higher levels
8. **Ultimate Goal**: Reach the surface (Level 0)

## Integration Points

### With Combat System
- Robots have chassis integrity instead of health
- Part quality affects combat stats
- Enhanced/pristine parts provide special combat abilities

### With Progression System  
- XP and leveling work normally
- Level ups increase max integrity and energy
- Gold economy for decontamination and trading

### With Shop System
- Neutral traders act as merchants
- Parts could be sold/bought in future
- Decontamination is a paid service

## Development Notes

### Key Design Principles
1. **Progressive Mobility**: Movement restrictions create natural progression
2. **Risk/Reward**: Substance offers power but at contamination cost
3. **Faction Dynamics**: Different approaches to robot existence
4. **Environmental Storytelling**: NPCs and objects reveal lore
5. **Player Choice**: Multiple paths through content

### Future Enhancements
- Equipment system for attached parts
- More part types (sensors, weapons, utilities)
- Crafting/upgrade system for parts
- Faction quest lines
- Guild system on higher levels
- Surface world content

### Testing Considerations
- Characters may need stat re-initialization
- Use `@py me.recalculate_stats()` to fix stat issues
- Contamination persists across sessions
- Faction reputation is permanent