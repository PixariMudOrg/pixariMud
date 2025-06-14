"""
Prototypes

A prototype is a simple way to create individualized instances of a
given typeclass. It is dictionary with specific key names.

For example, you might have a Sword typeclass that implements everything a
Sword would need to do. The only difference between different individual Swords
would be their key, description and some Attributes. The Prototype system
allows to create a range of such Swords with only minor variations. Prototypes
can also inherit and combine together to form entire hierarchies (such as
giving all Sabres and all Broadswords some common properties). Note that bigger
variations, such as custom commands or functionality belong in a hierarchy of
typeclasses instead.

A prototype can either be a dictionary placed into a global variable in a
python module (a 'module-prototype') or stored in the database as a dict on a
special Script (a db-prototype). The former can be created just by adding dicts
to modules Evennia looks at for prototypes, the latter is easiest created
in-game via the `olc` command/menu.

Prototypes are read and used to create new objects with the `spawn` command
or directly via `evennia.spawn` or the full path `evennia.prototypes.spawner.spawn`.

A prototype dictionary have the following keywords:

Possible keywords are:
- `prototype_key` - the name of the prototype. This is required for db-prototypes,
  for module-prototypes, the global variable name of the dict is used instead
- `prototype_parent` - string pointing to parent prototype if any. Prototype inherits
  in a similar way as classes, with children overriding values in their parents.
- `key` - string, the main object identifier.
- `typeclass` - string, if not set, will use `settings.BASE_OBJECT_TYPECLASS`.
- `location` - this should be a valid object or #dbref.
- `home` - valid object or #dbref.
- `destination` - only valid for exits (object or #dbref).
- `permissions` - string or list of permission strings.
- `locks` - a lock-string to use for the spawned object.
- `aliases` - string or list of strings.
- `attrs` - Attributes, expressed as a list of tuples on the form `(attrname, value)`,
  `(attrname, value, category)`, or `(attrname, value, category, locks)`. If using one
   of the shorter forms, defaults are used for the rest.
- `tags` - Tags, as a list of tuples `(tag,)`, `(tag, category)` or `(tag, category, data)`.
-  Any other keywords are interpreted as Attributes with no category or lock.
   These will internally be added to `attrs` (equivalent to `(attrname, value)`.

See the `spawn` command and `evennia.prototypes.spawner.spawn` for more info.

"""

## example of module-based prototypes using
## the variable name as `prototype_key` and
## simple Attributes

# from random import randint
#
# GOBLIN = {
# "key": "goblin grunt",
# "health": lambda: randint(20,30),
# "resists": ["cold", "poison"],
# "attacks": ["fists"],
# "weaknesses": ["fire", "light"],
# "tags": = [("greenskin", "monster"), ("humanoid", "monster")]
# }
#
# GOBLIN_WIZARD = {
# "prototype_parent": "GOBLIN",
# "key": "goblin wizard",
# "spells": ["fire ball", "lighting bolt"]
# }
#
# GOBLIN_ARCHER = {
# "prototype_parent": "GOBLIN",
# "key": "goblin archer",
# "attacks": ["short bow"]
# }
#
# This is an example of a prototype without a prototype
# (nor key) of its own, so it should normally only be
# used as a mix-in, as in the example of the goblin
# archwizard below.
# ARCHWIZARD_MIXIN = {
# "attacks": ["archwizard staff"],
# "spells": ["greater fire ball", "greater lighting"]
# }
#
# GOBLIN_ARCHWIZARD = {
# "key": "goblin archwizard",
# "prototype_parent" : ("GOBLIN_WIZARD", "ARCHWIZARD_MIXIN")
# }


# =============================================================================
# PIXARIMUD DEMO PROTOTYPES
# =============================================================================

COMBAT_DUMMY = {
    "key": "combat dummy",
    "aliases": ["dummy", "training dummy"],
    "typeclass": "typeclasses.objects.CombatDummy",
    "desc": "A sturdy combat training dummy. You can 'hit dummy' to practice combat and gain experience.",
    "tags": [("combat", "equipment"), ("demo", "system")]
}

BOTTOMLESS_PIT = {
    "key": "bottomless pit", 
    "aliases": ["pit", "hole", "abyss"],
    "typeclass": "typeclasses.objects.BottomlessPit",
    "desc": "A dark, seemingly bottomless pit. The depths are shrouded in darkness. You can 'jump pit' or 'jump in pit' if you dare...",
    "tags": [("hazard", "environment"), ("demo", "system")]
}

WORN_DUMMY = {
    "key": "worn-out dummy",
    "aliases": ["worn", "old dummy", "broken dummy"],
    "typeclass": "typeclasses.objects.WornOutDummy", 
    "desc": "An old, worn-out combat dummy that looks like it's seen better days. You can 'hit dummy' to attack it, but be careful - it might break!",
    "tags": [("combat", "equipment"), ("destructible", "equipment"), ("demo", "system")]
}

DEMO_ROOM = {
    "key": "Combat Training Arena",
    "aliases": ["arena", "training ground"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": "A spacious training arena with high ceilings and reinforced walls. Various combat training equipment is scattered around the room. This is where warriors come to hone their skills and test new techniques."
}

RESPAWN_ROOM = {
    "key": "Respawn Chamber",
    "aliases": ["chamber", "sanctuary", "respawn"],
    "typeclass": "typeclasses.rooms.Room", 
    "desc": "A mystical chamber where fallen warriors return to life. The air shimmers with magical energy, and soft light emanates from crystalline formations on the walls. This is a safe place for the recently deceased."
}

# =============================================================================
# NPC PROTOTYPES
# =============================================================================

SCANNER_BOT = {
    "key": "Scanner Bot",
    "aliases": ["scanner", "bot", "security"],
    "typeclass": "typeclasses.npcs.ScannerBot",
    "desc": "A hovering mechanical scanner bot with a rotating sensor array. Red lights blink as it continuously scans the area for activity.",
    "tags": [("npc", "system"), ("tech", "faction"), ("demo", "system")]
}

WHISPER_BOT = {
    "key": "Whispering Guide",
    "aliases": ["guide", "whisper", "robot"],
    "typeclass": "typeclasses.npcs.WhisperBot",
    "desc": "A slender robotic figure draped in a tattered cloak. Its voice module appears damaged, limiting it to whispered communications. A small sign reads: 'Speak softly, and I shall guide you.'",
    "tags": [("npc", "system"), ("guide", "role"), ("demo", "system")]
}

FACTION_GUARD = {
    "key": "Tech Consortium Guard",
    "aliases": ["guard", "tech guard", "consortium"],
    "typeclass": "typeclasses.npcs.FactionGuard",
    "desc": "A stern-looking guard wearing the colors of the Tech Consortium. Their augmented eyes scan everyone who passes, analyzing threat levels.",
    "attrs": [
        ("faction", "tech_consortium"),
        ("enemy_factions", ["nature_cult", "scavengers"]),
        ("allied_factions", ["tech_consortium", "cyborg_union"])
    ],
    "tags": [("npc", "system"), ("tech_consortium", "faction"), ("guard", "role"), ("demo", "system")]
}

MERCHANT_NPC = {
    "key": "Traveling Merchant",
    "aliases": ["merchant", "trader", "vendor"],
    "typeclass": "typeclasses.npcs.MerchantNPC",
    "desc": "A weathered merchant with keen eyes and a ready smile. Their pack is filled with various goods and curiosities. They seem eager to make a deal.",
    "attrs": [
        ("items_for_sale", {
            'healing potion': 50,
            'energy cell': 100,
            'ancient map': 500,
            'scanner jammer': 250
        })
    ],
    "tags": [("npc", "system"), ("merchant", "role"), ("demo", "system")]
}

# Faction-specific guard variants
NATURE_GUARD = {
    "prototype_parent": "FACTION_GUARD",
    "key": "Nature Cult Guardian",
    "aliases": ["guardian", "nature guard", "druid"],
    "desc": "A fierce guardian adorned with living vines and natural armor. Their eyes glow with an otherworldly green light as they protect the sacred groves.",
    "attrs": [
        ("faction", "nature_cult"),
        ("enemy_factions", ["tech_consortium", "cyborg_union"]),
        ("allied_factions", ["nature_cult"])
    ],
    "tags": [("npc", "system"), ("nature_cult", "faction"), ("guard", "role"), ("demo", "system")]
}

SCAVENGER_LOOKOUT = {
    "prototype_parent": "FACTION_GUARD",
    "key": "Scavenger Lookout",
    "aliases": ["lookout", "scav", "scout"],
    "desc": "A wiry figure in patched armor, constantly scanning for threats and opportunities. Their gear is a hodgepodge of salvaged technology and makeshift weapons.",
    "attrs": [
        ("faction", "scavengers"),
        ("enemy_factions", []),  # Scavengers are opportunists, no permanent enemies
        ("allied_factions", ["scavengers"])
    ],
    "tags": [("npc", "system"), ("scavengers", "faction"), ("guard", "role"), ("demo", "system")]
}

# =============================================================================
# KEYCARD AND SECURITY PROTOTYPES
# =============================================================================

STANDARD_KEYCARD = {
    "key": "standard keycard",
    "aliases": ["keycard", "card", "standard"],
    "typeclass": "typeclasses.objects.Keycard",
    "desc": "A white plastic keycard with a magnetic strip. The word 'STANDARD' is printed on one side.",
    "attrs": [
        ("access_level", "standard")
    ],
    "tags": [("keycard", "security"), ("demo", "system")]
}

SECURITY_KEYCARD = {
    "key": "security keycard", 
    "aliases": ["keycard", "card", "security", "yellow card"],
    "typeclass": "typeclasses.objects.Keycard",
    "desc": "A yellow security keycard with enhanced encryption. The word 'SECURITY' is embossed in black letters.",
    "attrs": [
        ("access_level", "security")
    ],
    "tags": [("keycard", "security"), ("demo", "system")]
}

ADMIN_KEYCARD = {
    "key": "admin keycard",
    "aliases": ["keycard", "card", "admin", "red card"],
    "typeclass": "typeclasses.objects.Keycard", 
    "desc": "A red administrative keycard with holographic security features. 'ADMIN ACCESS' glows faintly on the surface.",
    "attrs": [
        ("access_level", "admin")
    ],
    "tags": [("keycard", "security"), ("demo", "system")]
}

MASTER_KEYCARD = {
    "key": "master keycard",
    "aliases": ["keycard", "card", "master", "purple card"],
    "typeclass": "typeclasses.objects.Keycard",
    "desc": "A purple master keycard that seems to shimmer with internal circuitry. 'MASTER ACCESS' pulses with soft light.",
    "attrs": [
        ("access_level", "master")
    ],
    "tags": [("keycard", "security"), ("demo", "system")]
}

LAB_KEYCARD = {
    "key": "laboratory keycard",
    "aliases": ["keycard", "card", "lab card", "lab"],
    "typeclass": "typeclasses.objects.Keycard",
    "desc": "A specialized keycard with 'LABORATORY ACCESS' and a biohazard symbol. It has a unique serial number.",
    "attrs": [
        ("access_level", "security"),
        ("keycard_id", "LAB-7734")
    ],
    "tags": [("keycard", "security"), ("lab", "location"), ("demo", "system")]
}

# Vault Door Prototypes

BASIC_VAULT_DOOR = {
    "key": "security door",
    "aliases": ["door", "vault", "security"],
    "typeclass": "typeclasses.exits.VaultDoor",
    "desc": "A reinforced security door with a glowing card reader. A yellow light indicates 'SECURITY CLEARANCE REQUIRED'.",
    "attrs": [
        ("required_access_level", "security"),
        ("door_name", "security door")
    ],
    "tags": [("door", "security"), ("demo", "system")]
}

ADMIN_VAULT_DOOR = {
    "key": "restricted access door",
    "aliases": ["door", "restricted", "admin door"],
    "typeclass": "typeclasses.exits.VaultDoor",
    "desc": "A heavy blast door marked with red warning stripes. The card reader displays 'ADMIN ACCESS ONLY' in bold letters.",
    "attrs": [
        ("required_access_level", "admin"),
        ("door_name", "restricted access door")
    ],
    "tags": [("door", "security"), ("admin", "access"), ("demo", "system")]
}

LAB_VAULT_DOOR = {
    "key": "laboratory entrance",
    "aliases": ["lab door", "entrance", "lab"],
    "typeclass": "typeclasses.exits.VaultDoor",
    "desc": "A sealed laboratory entrance with biohazard warnings. The card reader shows 'AUTHORIZED PERSONNEL ONLY - ID REQUIRED'.",
    "attrs": [
        ("required_access_level", "security"),
        ("required_keycard_id", "LAB-7734"),
        ("door_name", "laboratory entrance")
    ],
    "tags": [("door", "security"), ("lab", "location"), ("demo", "system")]
}

MASTER_VAULT_DOOR = {
    "key": "command center door",
    "aliases": ["command door", "master door", "command"],
    "typeclass": "typeclasses.exits.VaultDoor",
    "desc": "An imposing door made of unknown alloys. Multiple scanners and a sophisticated card reader guard the entrance. 'MASTER CLEARANCE REQUIRED' pulses ominously.",
    "attrs": [
        ("required_access_level", "master"),
        ("door_name", "command center door")
    ],
    "tags": [("door", "security"), ("command", "location"), ("demo", "system")]
}

# Demo Rooms for Security System

SECURITY_LOBBY = {
    "key": "Security Checkpoint",
    "aliases": ["checkpoint", "lobby", "security"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": "A sterile security checkpoint with scanning equipment and monitors displaying various facility areas. Multiple doors lead to different sections, each requiring appropriate clearance. A security terminal provides information about access levels."
}

SECURE_STORAGE = {
    "key": "Secure Storage Room",
    "aliases": ["storage", "vault", "secure room"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": "A climate-controlled storage room filled with locked containers and shelving units. Security cameras monitor every corner. Various keycards and valuable items are stored here under tight security."
}

LABORATORY = {
    "key": "Research Laboratory", 
    "aliases": ["lab", "research", "laboratory"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": "A high-tech laboratory filled with experimental equipment and containment units. Warning signs indicate various hazards. Only authorized personnel with proper clearance should be here."
}

COMMAND_CENTER = {
    "key": "Command Center",
    "aliases": ["command", "center", "control room"],
    "typeclass": "typeclasses.rooms.Room",
    "desc": "The nerve center of the facility. Banks of monitors display critical systems and security feeds. A massive holographic display dominates the center of the room. This is where all major decisions are made."
}
