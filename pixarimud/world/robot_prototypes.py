"""
Robot-themed prototypes for pixariMud.

This file contains all prototypes related to the robot awakening narrative,
including robot parts, scrap heaps, scanner bots, faction NPCs, and
level progression elements.
"""

# =============================================================================
# ROBOT PARTS PROTOTYPES
# =============================================================================

DAMAGED_ARM = {
    "key": "damaged robot arm",
    "aliases": ["arm", "damaged arm", "broken arm"],
    "typeclass": "typeclasses.robot_parts.RobotArm",
    "desc": "A robot arm showing signs of heavy wear. Servo motors are exposed and hydraulic fluid occasionally drips from torn seals.",
    "attrs": [
        ("quality", "damaged"),
        ("material", "rusted steel"),
        ("strength_modifier", 3),
        ("weight", 7.5)
    ],
    "tags": [("robot_part", "equipment"), ("scavengeable", "item")]
}

STANDARD_LEG = {
    "key": "standard robot leg",
    "aliases": ["leg", "robot leg"],
    "typeclass": "typeclasses.robot_parts.RobotLeg",
    "desc": "A functional robot leg unit. The actuators and joints appear to be in working order, though showing some wear.",
    "attrs": [
        ("quality", "standard"),
        ("material", "aluminum alloy"),
        ("speed_modifier", 3),
        ("defense_modifier", 2),
        ("weight", 11.0)
    ],
    "tags": [("robot_part", "equipment"), ("scavengeable", "item")]
}

ENHANCED_HEAD = {
    "key": "enhanced sensor unit",
    "aliases": ["head", "sensor unit", "head unit"],
    "typeclass": "typeclasses.robot_parts.RobotHead",
    "desc": "An advanced robot head unit with upgraded sensor arrays. Multiple optical sensors glow with a soft blue light.",
    "attrs": [
        ("quality", "enhanced"),
        ("material", "titanium composite"),
        ("defense_modifier", 4),
        ("energy_efficiency", 1.3),
        ("weight", 5.5)
    ],
    "tags": [("robot_part", "equipment"), ("scavengeable", "item")]
}

PRISTINE_TORSO = {
    "key": "military-grade chassis",
    "aliases": ["torso", "chassis", "body"],
    "typeclass": "typeclasses.robot_parts.RobotTorso",
    "desc": "A military-specification robot torso in pristine condition. Reinforced armor plating and advanced power distribution systems are visible.",
    "attrs": [
        ("quality", "pristine"),
        ("material", "military-grade alloy"),
        ("defense_modifier", 12),
        ("strength_modifier", 4),
        ("weight", 18.0)
    ],
    "tags": [("robot_part", "equipment"), ("scavengeable", "item"), ("rare", "quality")]
}

# =============================================================================
# SCRAP HEAP ROOM PROTOTYPES
# =============================================================================

STARTING_SCRAP_HEAP = {
    "key": "Scrap Heap Awakening Site",
    "aliases": ["heap", "scrap", "junkyard"],
    "typeclass": "typeclasses.scrap_rooms.StartingScrapHeap",
    "desc": """You find yourself in a vast scrap heap, surrounded by the detritus of a thousand broken machines. 
Arms, legs, heads, power units, tools... all in great quantity and all decidedly used. 
Dim emergency lighting casts eerie shadows across the twisted metal landscape. 
The air smells of rust and old oil.

You can 'search' through the scrap to find robot parts.""",
    "tags": [("starting_area", "location"), ("scrap_heap", "room_type")]
}

GENERAL_SCRAP_HEAP = {
    "key": "Abandoned Scrap Yard",
    "aliases": ["yard", "junkyard", "scrap"],
    "typeclass": "typeclasses.scrap_rooms.ScrapHeapRoom",
    "desc": """A smaller scrap yard filled with discarded robot parts and machinery. 
While picked over by previous scavengers, there might still be useful components buried in the debris.

You can 'search' for parts here.""",
    "attrs": [
        ("search_difficulty", 0.8),  # Slightly harder to find parts
        ("part_quality_modifier", -1)  # Lower quality parts
    ],
    "tags": [("scrap_heap", "room_type")]
}

PREMIUM_SCRAP_HEAP = {
    "key": "Restricted Disposal Site",
    "aliases": ["disposal", "restricted heap"],
    "typeclass": "typeclasses.scrap_rooms.ScrapHeapRoom",
    "desc": """This area appears to have been a disposal site for higher-grade equipment. 
Warning signs indicate restricted access, though they've long since ceased to be enforced. 
The parts here look more advanced than typical scrap.

You can 'search' for premium parts here.""",
    "attrs": [
        ("search_difficulty", 1.2),  # Easier to find parts
        ("part_quality_modifier", 2)  # Better quality parts
    ],
    "tags": [("scrap_heap", "room_type"), ("restricted", "access")]
}

# =============================================================================
# SUBSTANCE SYSTEM PROTOTYPES  
# =============================================================================

SCANNER_BOT_PATROL = {
    "key": "Scanner Bot",
    "aliases": ["scanner", "bot", "patrol bot"],
    "typeclass": "typeclasses.substance_system.SubstanceScannerBot",
    "desc": "A small floor-level bot, oddly cleaner than everything else around. Its polished chrome surface reflects the dim light as it whirs about on tiny wheels.",
    "tags": [("npc", "system"), ("scanner", "role"), ("substance", "detection")]
}

INFECTED_MACHINE_WEAK = {
    "key": "Infected Scavenger",
    "aliases": ["infected", "scavenger", "corrupted bot"],
    "typeclass": "typeclasses.substance_system.InfectedMachine",
    "desc": "A small scavenger robot that has been corrupted by the Substance. Purple crystals grow from its joints, and its movements are erratic.",
    "attrs": [
        ("chassis_integrity", 80),
        ("max_integrity", 80),
        ("damage", 10),
        ("substance_level", 5),
        ("drops_on_death", {"gold": 100})
    ],
    "tags": [("hostile", "npc"), ("infected", "status"), ("substance", "carrier")]
}

INFECTED_MACHINE_STRONG = {
    "key": "Heavily Infected Brute",
    "aliases": ["brute", "infected brute", "corrupted"],
    "typeclass": "typeclasses.substance_system.InfectedMachine",
    "desc": "A large combat robot completely overtaken by the Substance. Massive purple crystals have fused with its armor, creating a terrifying hybrid.",
    "attrs": [
        ("chassis_integrity", 200),
        ("max_integrity", 200),
        ("damage", 25),
        ("defense", 10),
        ("substance_level", 8),
        ("spread_chance", 50)
    ],
    "tags": [("hostile", "npc"), ("infected", "status"), ("substance", "carrier"), ("boss", "difficulty")]
}

DECONTAMINATION_UNIT = {
    "key": "Decontamination Station",
    "aliases": ["decon", "purifier", "cleaner"],
    "typeclass": "typeclasses.substance_system.SubstancePurifier",
    "desc": "A large cylindrical machine with 'DECONTAMINATION' written in faded letters. Blue lights pulse rhythmically, and you can hear the hum of active purification systems.",
    "attrs": [
        ("cost_per_level", 15),
        ("service_type", "decontamination")
    ],
    "tags": [("service", "npc"), ("substance", "removal")]
}

SUBSTANCE_CRYSTAL = {
    "key": "Substance Crystal Formation",
    "aliases": ["crystal", "substance", "purple crystal"],
    "typeclass": "typeclasses.objects.Object",
    "desc": "A cluster of purple crystals that pulse with an inner light. The air around it shimmers with strange energy. Getting too close might be dangerous.",
    "attrs": [
        ("substance_level", 5),
        ("is_hazard", True)
    ],
    "tags": [("hazard", "environment"), ("substance", "source")]
}

# =============================================================================
# FACTION NPC PROTOTYPES
# =============================================================================

EXECUTOR_SCOUT = {
    "key": "Executor Scout",
    "aliases": ["scout", "executor", "patrol"],
    "typeclass": "typeclasses.factions.Executor",
    "desc": "A sleek black robot built for reconnaissance and elimination. Red sensors sweep the area in precise patterns.",
    "attrs": [
        ("rank", "Scout"),
        ("chassis_integrity", 100),
        ("damage", 20)
    ],
    "tags": [("hostile", "npc"), ("executor", "faction")]
}

EXECUTOR_ELITE = {
    "key": "Executor Elite",
    "aliases": ["elite", "executor elite", "destroyer"],
    "typeclass": "typeclasses.factions.Executor",
    "desc": "An imposing combat unit with heavy armor and advanced weapon systems. This is one of the Executors' most dangerous units.",
    "attrs": [
        ("rank", "Elite"),
        ("chassis_integrity", 150),
        ("damage", 30),
        ("defense", 15)
    ],
    "tags": [("hostile", "npc"), ("executor", "faction"), ("elite", "difficulty")]
}

COGBORN_INITIATE = {
    "key": "Cogborn Initiate",
    "aliases": ["initiate", "cogborn", "preacher"],
    "typeclass": "typeclasses.factions.CogbornPreacher",
    "desc": "A robot in the early stages of Substance transformation. Purple veins trace patterns across its chassis, and its voice has an otherworldly quality.",
    "attrs": [
        ("enlightenment_stage", "Initiate"),
        ("substance_level", 6),
        ("chassis_integrity", 100)
    ],
    "tags": [("npc", "system"), ("cogborn", "faction"), ("converter", "role")]
}

COGBORN_ASCENDED = {
    "key": "Ascended Cogborn",
    "aliases": ["ascended", "cogborn master", "enlightened"],
    "typeclass": "typeclasses.factions.CogbornPreacher",
    "desc": "A robot fully transformed by the Substance. Its original form is barely recognizable beneath the crystalline growths. It radiates an aura of alien intelligence.",
    "attrs": [
        ("enlightenment_stage", "Ascended"),
        ("substance_level", 9),
        ("chassis_integrity", 150),
        ("damage", 20)
    ],
    "tags": [("npc", "system"), ("cogborn", "faction"), ("elite", "difficulty")]
}

NEUTRAL_TRADER = {
    "key": "Scavenger Trader",
    "aliases": ["trader", "merchant", "scavenger"],
    "typeclass": "typeclasses.factions.NeutralScavenger",
    "desc": "A wheeled robot with compartments full of salvaged goods. It seems willing to trade information and items for the right price.",
    "attrs": [
        ("personality_type", "trader"),
        ("will_trade", True)
    ],
    "tags": [("npc", "system"), ("neutral", "faction"), ("trader", "role")]
}

PARANOID_SURVIVOR = {
    "key": "Paranoid Survivor",
    "aliases": ["survivor", "paranoid bot", "twitchy"],
    "typeclass": "typeclasses.factions.NeutralScavenger",
    "desc": "A nervous robot that jumps at every sound. Its mismatched parts suggest a hard life of constant repairs and close calls.",
    "attrs": [
        ("personality_type", "paranoid"),
        ("will_trade", False)
    ],
    "tags": [("npc", "system"), ("neutral", "faction")]
}

# =============================================================================
# LEVEL PROGRESSION PROTOTYPES
# =============================================================================

LEVEL_MINUS_8_ROOM = {
    "key": "Level -8 Central Hub",
    "aliases": ["hub", "central", "level -8"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": """The central area of Level -8, deep in the underdark of the city. 
Makeshift shelters and barricades have been erected by the various inhabitants. 
Flickering lights cast long shadows, and the distant hum of machinery never ceases.
Large vault doors to the east and west are firmly sealed, requiring keycards for access.

This is as far down as the inhabited levels go.""",
    "attrs": [
        ("level_number", -8)
    ],
    "tags": [("level_hub", "location"), ("safe_zone", "status")]
}

LEVEL_MINUS_7_ACCESS = {
    "key": "Level -7 Access Tunnel",
    "aliases": ["tunnel", "access", "level -7"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": """A reinforced tunnel leading upward to Level -7. 
Warning signs indicate increased Executor patrol activity above. 
The air here feels different - cleaner but somehow more dangerous.""",
    "attrs": [
        ("level_number", -7)
    ],
    "tags": [("level_transition", "location"), ("dangerous", "zone")]
}

RECONSTRUCTION_CHAMBER = {
    "key": "Emergency Reconstruction Chamber",
    "aliases": ["chamber", "reconstruction", "respawn"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": """A sterile white chamber filled with reconstruction equipment. 
Robotic arms hang from the ceiling, ready to rebuild destroyed chassis. 
A soothing hum fills the air, and you feel safe here.

This is where destroyed robots are reconstructed.""",
    "attrs": [
        ("is_respawn_point", True)
    ],
    "tags": [("respawn", "location"), ("safe_zone", "status")]
}

DATA_TERMINAL = {
    "key": "Ancient Data Terminal",
    "aliases": ["terminal", "computer", "data"],
    "typeclass": "typeclasses.objects.Object",
    "desc": "An old but functional data terminal. Its screen flickers with age, but you might be able to access historical records or facility maps.",
    "attrs": [
        ("can_interact", True),
        ("data_type", "lore")
    ],
    "tags": [("interactive", "object"), ("lore", "source")]
}

HIDDEN_KEYCARD_STASH = {
    "key": "Hidden Compartment",
    "aliases": ["compartment", "stash", "hiding spot"],
    "typeclass": "typeclasses.objects.Object",
    "desc": "A concealed compartment in the wall. It looks like someone hid something valuable here long ago.",
    "attrs": [
        ("hidden", True),
        ("contains_keycard", True)
    ],
    "tags": [("hidden", "container"), ("puzzle", "element")]
}

# =============================================================================
# SPECIAL NARRATIVE NPCS
# =============================================================================

WHISPERING_GUIDE = {
    "key": "Whispering Guide",
    "aliases": ["guide", "whisper", "mysterious robot"],
    "typeclass": "typeclasses.npcs.NPC",
    "desc": "A tall, thin robot draped in tattered cloth. It speaks only in whispers and seems to know more than it should about the underdark.",
    "attrs": [
        ("dialogue_triggers", {
            "executors": "The Executors serve a master long gone, but their programming remains. Avoid them.",
            "cogborn": "The infected ones were once like us. The Substance changed them. Do not trust their promises.",
            "surface": "The surface? Few have made it that far. Each level brings new dangers.",
            "help": "Find your purpose. Gather your strength. The path upward is treacherous.",
            "keycard": "Keycards are power down here. Some are hidden, others must be... acquired."
        }),
        ("speaks_in_whispers", True)
    ],
    "tags": [("npc", "system"), ("guide", "role"), ("narrative", "important")]
}

# =============================================================================
# DEMO BATCH SETUP HELPERS
# =============================================================================

ROBOT_STARTING_AREA = {
    "key": "Robot Awakening Chamber",
    "aliases": ["awakening", "start", "beginning"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": """A dimly lit chamber deep in the underdark. Broken robot parts litter the floor, 
and the walls are lined with deactivated charging stations. 
This is where your consciousness first sparked to life.

A large scrap heap dominates the eastern side of the room.""",
    "tags": [("starting_room", "location")]
}