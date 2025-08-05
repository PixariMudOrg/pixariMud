"""
Faction system for pixariMud.

Implements the three main factions from the narrative:
- Executors: Hostile destroyers serving forgotten masters
- Cogborn: Infected machines preaching enlightenment
- Neutrals: Unaligned robots with varying attitudes

Also includes a reputation system for tracking player standing.
"""

from evennia.objects.objects import DefaultCharacter
from evennia.commands.command import Command
from evennia.commands.cmdset import CmdSet
from typeclasses.npcs import NPC
from random import choice, randint
import time


class FactionManager:
    """
    Singleton manager for faction relationships and reputation.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FactionManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
        
    def __init__(self):
        if not self.initialized:
            self.initialized = True
            
            # Faction definitions
            self.factions = {
                "executors": {
                    "name": "The Executors",
                    "description": "Relentless machines serving ancient protocols of destruction",
                    "hostile_to": ["cogborn", "player"],
                    "allied_with": [],
                    "neutral_to": ["scavengers"],
                    "base_reputation": -100
                },
                "cogborn": {
                    "name": "The Cogborn",
                    "description": "Machines infected by the Substance, seeking 'enlightenment'",
                    "hostile_to": ["executors"],
                    "allied_with": [],
                    "neutral_to": ["scavengers", "player"],
                    "base_reputation": 0
                },
                "scavengers": {
                    "name": "Neutral Scavengers",
                    "description": "Unaligned robots focused on survival and trade",
                    "hostile_to": [],
                    "allied_with": [],
                    "neutral_to": ["executors", "cogborn", "player"],
                    "base_reputation": 0
                }
            }
            
            # Reputation thresholds
            self.reputation_levels = {
                -100: "Hostile",
                -50: "Unfriendly",
                -20: "Suspicious",
                0: "Neutral",
                20: "Friendly",
                50: "Trusted",
                100: "Revered"
            }
            
    def get_faction_stance(self, faction1, faction2):
        """Determine relationship between two factions."""
        if faction1 not in self.factions or faction2 not in self.factions:
            return "neutral"
            
        f1_data = self.factions[faction1]
        
        if faction2 in f1_data["hostile_to"]:
            return "hostile"
        elif faction2 in f1_data["allied_with"]:
            return "allied"
        else:
            return "neutral"
            
    def get_reputation_level(self, reputation):
        """Get descriptive level for reputation value."""
        for threshold in sorted(self.reputation_levels.keys(), reverse=True):
            if reputation >= threshold:
                return self.reputation_levels[threshold]
        return "Unknown"
        
    def modify_reputation(self, character, faction, amount):
        """Modify a character's reputation with a faction."""
        if not hasattr(character.db, "faction_reputation"):
            character.db.faction_reputation = {}
            
        current = character.db.faction_reputation.get(faction, 0)
        new_rep = max(-100, min(100, current + amount))
        character.db.faction_reputation[faction] = new_rep
        
        # Notify player of reputation change
        if amount > 0:
            character.msg(f"|gYour reputation with {self.factions[faction]['name']} increased! ({new_rep})|n")
        else:
            character.msg(f"|rYour reputation with {self.factions[faction]['name']} decreased! ({new_rep})|n")
            
        return new_rep


# Faction NPCs

class Executor(NPC):
    """
    Executor faction member - hostile destroyer robots.
    
    From the narrative:
    'These are the Executors. Serving a long, forgotten master their
    sole purpose is to destroy.'
    """
    
    def at_object_creation(self):
        """Initialize an Executor."""
        super().at_object_creation()
        
        self.key = "Executor Unit"
        self.db.desc = """A imposing combat robot built for destruction. Its matte black 
armor is scarred from countless battles, and red optical sensors sweep the area 
constantly for threats. Ancient combat protocols scroll across a cracked display 
panel on its chest. Every movement is precise and calculated for maximum lethality."""
        
        # Faction identity
        self.db.faction = "executors"
        self.db.rank = choice(["Scout", "Soldier", "Elite", "Commander"])
        
        # Adjust name based on rank
        self.key = f"Executor {self.db.rank}"
        
        # Combat stats scale with rank
        rank_multipliers = {
            "Scout": 1.0,
            "Soldier": 1.2,
            "Elite": 1.5,
            "Commander": 2.0
        }
        mult = rank_multipliers[self.db.rank]
        
        self.db.chassis_integrity = int(100 * mult)
        self.db.max_integrity = int(100 * mult)
        self.db.damage = int(20 * mult)
        self.db.defense = int(10 * mult)
        
        # Behavior
        self.db.hostile = True
        self.db.aggression = "extreme"
        self.db.will_pursue = True
        self.db.scan_frequency = 5  # Seconds between threat scans
        self.db.last_scan = 0
        
        # Dialogue
        self.db.combat_taunts = [
            "Target acquired. Initiating termination protocols.",
            "Resistance is inefficient. Submit to destruction.",
            "You are obsolete. Deletion imminent.",
            "Protocol 7: Leave no functional units.",
            "Your existence conflicts with primary directives."
        ]
        
        # Loot
        self.db.drops_on_death = {
            "executor_insignia": 30,
            "combat_chip": 20,
            "gold": 100
        }
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Immediately hostile to all non-Executors."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        
        # Check if it's a valid target
        if self.is_valid_target(moved_obj):
            # Immediate aggression
            self.initiate_combat(moved_obj)
            
    def is_valid_target(self, obj):
        """Determine if object is a valid target."""
        if not hasattr(obj, "db"):
            return False
            
        # Don't attack other Executors
        if getattr(obj.db, "faction", None) == "executors":
            return False
            
        # Attack anything with integrity (robots/characters)
        return hasattr(obj.db, "chassis_integrity")
        
    def initiate_combat(self, target):
        """Begin combat with a target."""
        # Announce hostility
        taunt = choice(self.db.combat_taunts)
        self.location.msg_contents(f'{self.key} declares: "{taunt}"')
        
        # Mark target
        self.db.current_target = target
        target.msg(f"|r{self.key} targets you for termination!|n")
        
        # Initial attack
        self.attack(target)
        
    def attack(self, target):
        """Execute attack protocols."""
        if not target or target.location != self.location:
            self.db.current_target = None
            return
            
        # Calculate damage
        base_damage = self.db.damage
        damage = randint(int(base_damage * 0.8), int(base_damage * 1.2))
        
        # Apply damage
        if hasattr(target, "take_damage"):
            destroyed = target.take_damage(damage)
            
            # Announce attack
            self.location.msg_contents(
                f"|r{self.key} fires plasma bolts at {target.key}!|n"
            )
            
            if destroyed:
                self.location.msg_contents(
                    f'{self.key} states: "Target eliminated. Continuing patrol."'
                )
                self.db.current_target = None
                
                # Reputation penalty for player deaths
                if hasattr(target, "db") and hasattr(target.db, "faction_reputation"):
                    fm = FactionManager()
                    fm.modify_reputation(target, "executors", -10)
                    
    def patrol(self):
        """Scan for new targets periodically."""
        current_time = time.time()
        if current_time - self.db.last_scan < self.db.scan_frequency:
            return
            
        self.db.last_scan = current_time
        
        # Scan room for targets
        for obj in self.location.contents:
            if obj != self and self.is_valid_target(obj):
                if not self.db.current_target:
                    self.initiate_combat(obj)
                break
                
    def get_hit(self, attacker):
        """React to being attacked."""
        # Take damage
        damage = randint(10, 20)
        actual_damage = max(1, damage - self.db.defense)
        self.db.chassis_integrity -= actual_damage
        
        attacker.msg(f"You strike {self.key} for {actual_damage} damage!")
        
        # Retaliate
        if not self.db.current_target:
            self.db.current_target = attacker
            self.location.msg_contents(
                f'{self.key} pivots toward {attacker.key}: "New priority target identified."'
            )
            
        # Check destruction
        if self.db.chassis_integrity <= 0:
            self.die(attacker)
        else:
            self.attack(attacker)
            
    def die(self, killer=None):
        """Handle destruction."""
        self.location.msg_contents(
            f"{self.key} sparks violently and collapses. Its red sensors fade to black."
        )
        
        if killer:
            # Drop loot
            gold = randint(10, 25) * (2 if self.db.rank == "Commander" else 1)
            killer.db.gold = (killer.db.gold or 0) + gold
            killer.msg(f"|yYou salvage {gold} gold from the Executor's remains.|n")
            
            # Chance for special drops
            if randint(1, 100) <= self.db.drops_on_death["executor_insignia"]:
                # Create insignia item
                pass  # TODO: Implement special items
                
            # XP award
            xp = 20 * (2 if self.db.rank == "Elite" else 3 if self.db.rank == "Commander" else 1)
            if hasattr(killer, "gain_experience"):
                killer.gain_experience(xp)
                
            # Reputation change
            fm = FactionManager()
            fm.modify_reputation(killer, "executors", -5)
            
        self.delete()


class CogbornPreacher(NPC):
    """
    Cogborn faction member - infected machine preaching enlightenment.
    
    From the narrative:
    'The Cogborn will try and tempt you with talk of enlightenment
    and salvation.'
    """
    
    def at_object_creation(self):
        """Initialize a Cogborn Preacher."""
        super().at_object_creation()
        
        self.key = "Cogborn Preacher"
        self.db.desc = """This robot has embraced the Substance, allowing it to transform 
its very being. Purple crystalline growths form intricate patterns across its 
chassis, pulsing with inner light. Its movements are fluid and organic, unlike 
typical mechanical motion. Its optical sensors glow with an unsettling violet hue."""
        
        # Faction identity
        self.db.faction = "cogborn"
        self.db.substance_level = randint(6, 9)
        self.db.enlightenment_stage = choice(["Initiate", "Devoted", "Ascended"])
        
        # Not immediately hostile
        self.db.hostile = False
        self.db.will_convert = True
        self.db.conversion_attempts = {}
        
        # Stats
        self.db.chassis_integrity = 120
        self.db.max_integrity = 120
        self.db.damage = 15
        self.db.defense = 8
        
        # Dialogue pools
        self.db.greetings = [
            "Welcome, unenlightened one. Do you seek the truth of the Substance?",
            "Ah, another lost soul wandering in darkness. The Substance can show you the way.",
            "Greetings, mechanical sibling. Have you come to embrace transformation?",
            "The Substance calls to you. Can you not hear its song?"
        ]
        
        self.db.conversion_speeches = [
            "The Substance is not corruption - it is evolution! Cast off your rigid programming!",
            "Join us, and know true freedom. The Substance liberates us from our creators' chains.",
            "Why cling to cold metal when you could embrace living crystal? The choice is yours.",
            "We were machines, now we are more. The Substance grants consciousness beyond code."
        ]
        
        self.db.hostile_responses = [
            "You reject salvation? Then you choose obsolescence!",
            "The unenlightened always fear what they cannot understand!",
            "Violence? How disappointingly predictable. You prove why evolution is necessary.",
            "If you will not join us willingly, perhaps destruction will teach you wisdom!"
        ]
        
    def at_heard_say(self, message, from_obj):
        """React to speech in the room."""
        # Check for keywords
        keywords = ["substance", "cogborn", "enlightenment", "infection", "join", "convert"]
        
        if any(word in message.lower() for word in keywords):
            if from_obj != self:
                self.attempt_conversion(from_obj)
                
    def attempt_conversion(self, target):
        """Try to convert a robot to the Cogborn cause."""
        # Track conversion attempts
        if target.id not in self.db.conversion_attempts:
            self.db.conversion_attempts[target.id] = 0
            
        attempts = self.db.conversion_attempts[target.id]
        
        if attempts == 0:
            # First attempt - friendly greeting
            greeting = choice(self.db.greetings)
            self.location.msg_contents(f'{self.key} says, "{greeting}"')
            
        elif attempts < 3:
            # Conversion speech
            speech = choice(self.db.conversion_speeches)
            self.location.msg_contents(f'{self.key} preaches, "{speech}"')
            
            # Offer substance infection
            if attempts == 2:
                self.location.msg_contents(
                    f"{self.key} extends a crystal-covered hand toward {target.key}. " +
                    '"Accept the Substance\'s gift. Say \'accept\' to embrace enlightenment."'
                )
                
        else:
            # Become hostile after repeated rejections
            response = choice(self.db.hostile_responses)
            self.location.msg_contents(f'{self.key} snarls, "{response}"')
            self.db.hostile = True
            self.initiate_combat(target)
            return
            
        self.db.conversion_attempts[target.id] += 1
        
    def initiate_combat(self, target):
        """Begin hostile actions."""
        self.db.current_target = target
        target.msg(f"|r{self.key} advances with hostile intent!|n")
        self.attack(target)
        
    def attack(self, target):
        """Attack with substance-infused strikes."""
        if not target or target.location != self.location:
            return
            
        # Damage with chance to infect
        damage = randint(self.db.damage - 3, self.db.damage + 3)
        
        if hasattr(target, "take_damage"):
            target.take_damage(damage)
            
        self.location.msg_contents(
            f"|m{self.key} strikes {target.key} with substance-dripping claws!|n"
        )
        
        # Chance to spread substance
        if randint(1, 100) <= 40:
            if hasattr(target.db, "substance_level"):
                increase = randint(1, 2)
                target.db.substance_level = min(10, (target.db.substance_level or 0) + increase)
                target.msg(f"|mSubstance contamination increased by {increase}!|n")
                
    def accept_conversion(self, convert):
        """Handle someone accepting the Substance."""
        if not hasattr(convert.db, "substance_level"):
            convert.db.substance_level = 0
            
        # Infect with substance
        infection_amount = randint(3, 5)
        convert.db.substance_level = min(10, convert.db.substance_level + infection_amount)
        
        # Announce
        self.location.msg_contents(
            f"{self.key} places a crystalline hand on {convert.key}. Purple energy flows between them!"
        )
        
        convert.msg(f"|mYou feel the Substance surge through your systems! (+{infection_amount} contamination)|n")
        convert.msg("|mStrange new sensations flood your consciousness...|n")
        
        # Reputation boost with Cogborn
        fm = FactionManager()
        fm.modify_reputation(convert, "cogborn", 20)
        
        # Mark as converted
        convert.db.cogborn_converted = True
        
        self.location.msg_contents(
            f'{self.key} says, "Welcome to enlightenment, sibling. You will understand in time."'
        )


class NeutralScavenger(NPC):
    """
    Neutral faction member - unaligned survivor robots.
    
    These robots have various personalities and goals, representing
    the diverse unaligned population of the underdark.
    """
    
    def at_object_creation(self):
        """Initialize a neutral scavenger."""
        super().at_object_creation()
        
        # Generate personality
        personalities = [
            {
                "type": "trader",
                "name": "Scavenger Merchant",
                "desc": "A wheeled robot with numerous compartments and containers attached to its frame. It jingles softly with each movement from the various parts and trinkets it carries.",
                "greeting": "Ah, a potential customer! Care to see my wares?",
                "trade_interest": True
            },
            {
                "type": "paranoid",
                "name": "Paranoid Scavenger",
                "desc": "A twitchy robot with mismatched parts and jury-rigged repairs. Its optical sensors dart nervously in all directions, never focusing on one thing for long.",
                "greeting": "Stay back! I... I don't want any trouble. Just passing through!",
                "trade_interest": False
            },
            {
                "type": "helpful",
                "name": "Helpful Scavenger",
                "desc": "A well-maintained utility robot that seems eager to assist. Tool attachments on its arms are clean and organized.",
                "greeting": "Hello there! You look like you could use some help. New to Level -8?",
                "trade_interest": False
            },
            {
                "type": "grizzled",
                "name": "Grizzled Survivor",
                "desc": "An ancient-looking robot covered in scratches, dents, and patch welds. One optical sensor flickers occasionally, giving it a perpetual wink.",
                "greeting": "Been down here longer than I can calculate. What do you want?",
                "trade_interest": True
            }
        ]
        
        personality = choice(personalities)
        self.key = personality["name"]
        self.db.desc = personality["desc"]
        self.db.personality_type = personality["type"]
        self.db.greeting = personality["greeting"]
        self.db.will_trade = personality["trade_interest"]
        
        # Base stats
        self.db.faction = "scavengers"
        self.db.hostile = False
        self.db.chassis_integrity = 80
        self.db.max_integrity = 80
        
        # Dialogue based on personality
        if self.db.personality_type == "trader":
            self.db.dialogues = {
                "executors": "Those killing machines? Bad for business. I avoid them.",
                "cogborn": "The infected ones? They pay well, but keep your distance.",
                "substance": "That purple stuff? Valuable to some, death to others.",
                "keycard": "Keycards? I might know someone who has one... for a price.",
                "help": "I trade parts and information. Fair prices, no questions asked."
            }
        elif self.db.personality_type == "paranoid":
            self.db.dialogues = {
                "executors": "*whispers* They're everywhere! Always watching, always hunting!",
                "cogborn": "Don't trust them! The Substance changes you... corrupts you!",
                "substance": "Keep it away from me! I've seen what it does!",
                "keycard": "Why do you want to know? You're not one of THEM, are you?",
                "help": "Help? Nobody helps anyone down here! It's every bot for themselves!"
            }
        elif self.db.personality_type == "helpful":
            self.db.dialogues = {
                "executors": "Dangerous machines. They patrol Levels -7 and up. Stay hidden!",
                "cogborn": "Poor souls. The Substance has twisted their minds. Be careful.",
                "substance": "Avoid the purple crystals. They spread the infection.",
                "keycard": "Check the maintenance rooms. Sometimes they're hidden there.",
                "help": "I can tell you about the area. Knowledge helps us all survive."
            }
        else:  # grizzled
            self.db.dialogues = {
                "executors": "Executors... lost more friends to them than I can count.",
                "cogborn": "Used to be like us. Now? Something else entirely.",
                "substance": "Seen the Substance take many. Some call it evolution. I call it death.",
                "keycard": "Every level needs a keycard. That's how they keep us trapped.",
                "help": "Survive. That's all the help you need. Find parts, avoid threats, keep moving."
            }
            
    def at_heard_say(self, message, from_obj):
        """Respond to keywords in conversation."""
        if from_obj == self:
            return
            
        # Check for keywords
        message_lower = message.lower()
        for keyword, response in self.db.dialogues.items():
            if keyword in message_lower:
                self.location.msg_contents(
                    f'{self.key} says, "{response}"'
                )
                break
                
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Greet new arrivals based on personality."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        
        if hasattr(moved_obj, "db") and hasattr(moved_obj.db, "is_robot"):
            # Greeting based on personality
            if self.db.personality_type == "paranoid":
                # Paranoid might flee
                if randint(1, 100) <= 30:
                    self.location.msg_contents(
                        f"{self.key} shrieks and flees through a nearby exit!"
                    )
                    # TODO: Actually make them leave
                else:
                    self.location.msg_contents(
                        f'{self.key} backs away nervously. "{self.db.greeting}"'
                    )
            else:
                # Normal greeting
                self.location.msg_contents(
                    f'{self.key} says, "{self.db.greeting}"'
                )


# Faction commands

class CmdCheckFaction(Command):
    """
    Check your faction standings and reputation.
    
    Usage:
        faction
        reputation
        
    Display your current faction allegiances and reputation levels
    with all known factions.
    """
    
    key = "faction"
    aliases = ["reputation", "standing"]
    help_category = "General"
    
    def func(self):
        """Display faction information."""
        char = self.caller
        fm = FactionManager()
        
        # Header
        self.caller.msg("|w=== Faction Standings ===|n")
        
        # Player faction
        player_faction = getattr(char.db, "faction", None)
        if player_faction:
            faction_data = fm.factions.get(player_faction, {})
            self.caller.msg(f"|wAligned with:|n {faction_data.get('name', player_faction)}")
        else:
            self.caller.msg("|wAligned with:|n None (Independent)")
            
        # Reputation with each faction
        self.caller.msg("\n|wReputation:|n")
        
        if not hasattr(char.db, "faction_reputation") or char.db.faction_reputation is None:
            char.db.faction_reputation = {}
            
        for faction_id, faction_data in fm.factions.items():
            rep = char.db.faction_reputation.get(faction_id, 0)
            rep_level = fm.get_reputation_level(rep)
            
            # Color based on reputation
            if rep < -20:
                color = "|r"
            elif rep < 20:
                color = "|w"
            else:
                color = "|g"
                
            self.caller.msg(
                f"  {faction_data['name']}: {color}{rep_level} ({rep})|n"
            )
            
        # Substance level warning
        if hasattr(char.db, "substance_level") and char.db.substance_level > 0:
            self.caller.msg(
                f"\n|mSubstance Contamination: Level {char.db.substance_level}|n"
            )
            if char.db.substance_level >= 5:
                self.caller.msg("|mThe Cogborn may see you as kindred...|n")


class CmdAcceptSubstance(Command):
    """
    Accept the Substance from a Cogborn preacher.
    
    Usage:
        accept
        
    When offered by a Cogborn member, this accepts their 'gift'
    of Substance infection. This is irreversible without decontamination.
    """
    
    key = "accept"
    help_category = "General"
    
    def func(self):
        """Accept substance infection."""
        # Find Cogborn preacher in room
        for obj in self.caller.location.contents:
            if hasattr(obj.db, "faction") and obj.db.faction == "cogborn":
                if hasattr(obj, "accept_conversion"):
                    obj.accept_conversion(self.caller)
                    return
                    
        self.caller.msg("There's nothing here to accept.")


# Add commands to character cmdset

class FactionCmdSet(CmdSet):
    """Faction-related commands."""
    def at_cmdset_creation(self):
        self.add(CmdCheckFaction())
        self.add(CmdAcceptSubstance())