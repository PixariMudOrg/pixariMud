"""
The Substance system and infected machines for pixariMud.

The Substance is a dangerous material that infects robots and drives
the central conflict between factions. Scanner bots detect it, and
infected machines pose threats to players.
"""

from evennia.objects.objects import DefaultCharacter, DefaultRoom
from evennia.commands.command import Command
from evennia.commands.cmdset import CmdSet
from evennia.scripts.scripts import DefaultScript
from evennia.utils.evtable import EvTable
from typeclasses.npcs import NPC
from random import choice, randint
import time


class SubstanceScript(DefaultScript):
    """
    Script that handles substance spread and effects.
    
    This script runs periodically to update substance levels
    and spread contamination between objects.
    """
    
    def at_script_creation(self):
        """Initialize the substance tracking script."""
        self.key = "substance_tracker"
        self.desc = "Tracks and spreads substance contamination"
        self.interval = 60  # Check every minute
        self.persistent = True
        self.db.contaminated_objects = []
        
    def at_repeat(self):
        """Called every interval to update substance effects."""
        # Update contamination spread
        for obj_id in list(self.db.contaminated_objects):
            obj = self.search(f"#{obj_id}", global_search=True)
            if obj and hasattr(obj.db, "substance_level"):
                self.spread_contamination(obj)
                
    def spread_contamination(self, source):
        """Spread substance from contaminated object to nearby objects."""
        if not source.location:
            return
            
        # Higher substance levels spread more aggressively
        spread_chance = source.db.substance_level * 10
        
        # Check all objects in the same location
        for obj in source.location.contents:
            if obj == source or not hasattr(obj, "db"):
                continue
                
            # Roll for contamination spread
            if randint(1, 100) <= spread_chance:
                self.contaminate_object(obj, source.db.substance_level // 2)
                
    def contaminate_object(self, obj, level):
        """Add substance contamination to an object."""
        if not hasattr(obj.db, "substance_level"):
            obj.db.substance_level = 0
            
        # Increase contamination
        old_level = obj.db.substance_level
        obj.db.substance_level = min(10, obj.db.substance_level + level)
        
        if old_level == 0 and obj.db.substance_level > 0:
            # Newly contaminated
            self.db.contaminated_objects.append(obj.id)
            
            # Notify if it's a character
            if hasattr(obj, "msg"):
                obj.msg("|rYou feel a strange tingling as the Substance begins to affect you!|n")


class SubstanceScannerBot(NPC):
    """
    Small autonomous bot that scans for substance contamination.
    
    As described in the narrative:
    'A small floor-level bot, oddly cleaner than everything else around
    whizzes up to you and bathes you in a brilliant green light that
    stops you in your tracks.'
    """
    
    def at_object_creation(self):
        """Initialize the scanner bot."""
        super().at_object_creation()
        
        self.key = "Scanner Bot"
        self.db.desc = """A small, wheeled robot about the size of a dinner plate. 
Its polished chrome surface is oddly pristine compared to everything else 
down here. A rotating sensor array on top emits periodic sweeps of green 
light. It moves with purposeful efficiency, constantly scanning its 
environment."""
        
        # Scanner properties
        self.db.is_npc = True
        self.db.scanner_type = "substance_detector"
        self.db.scan_range = 5  # Meters
        self.db.scan_interval = 30  # Seconds between area scans
        self.db.last_scan_time = 0
        self.db.threat_level = 0  # Current area threat assessment
        
        # Movement pattern
        self.db.patrol_route = []
        self.db.current_patrol_index = 0
        self.db.is_scanning = False
        
        # Scan results memory
        self.db.scan_log = []
        self.db.contaminated_entities = []
        
        # Scanner dialogue
        self.db.scan_messages = {
            0: "No substance detected in subject, allow to proceed, no further action to be taken.",
            1: "Trace substance levels detected. Subject flagged for monitoring.",
            2: "Moderate substance contamination. Alert: Decontamination recommended.",
            3: "High substance levels detected! Warning: Subject poses contamination risk.",
            4: "CRITICAL CONTAMINATION! Initiating containment protocols!",
            5: "MAXIMUM SUBSTANCE SATURATION! EMERGENCY! EMERGENCY!"
        }
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """React when someone enters the scanner's location."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        
        # Only scan characters
        if hasattr(moved_obj, "db") and hasattr(moved_obj.db, "is_robot"):
            # Immediate scan of new arrivals
            self.scan_entity(moved_obj)
            
    def scan_entity(self, target):
        """Perform a substance scan on a target."""
        if self.db.is_scanning:
            return  # Already scanning something
            
        self.db.is_scanning = True
        
        # Announce the scan
        self.location.msg_contents(
            f"{self.key} whirs to life and approaches {target.key}, " +
            "bathing them in brilliant green light!"
        )
        
        # Check substance level
        substance_level = getattr(target.db, "substance_level", 0)
        
        # Determine threat category
        if substance_level == 0:
            threat_category = 0
        elif substance_level <= 2:
            threat_category = 1
        elif substance_level <= 4:
            threat_category = 2
        elif substance_level <= 6:
            threat_category = 3
        elif substance_level <= 8:
            threat_category = 4
        else:
            threat_category = 5
            
        # Get appropriate message
        scan_result = self.db.scan_messages.get(threat_category, 
                                                self.db.scan_messages[0])
        
        # Announce result
        self.location.msg_contents(
            f'{self.key} announces in a tinny voice: "{scan_result}"'
        )
        
        # Log the scan
        self.db.scan_log.append({
            "target": target.key,
            "substance_level": substance_level,
            "threat_category": threat_category,
            "timestamp": time.time()
        })
        
        # Track contaminated entities
        if substance_level > 0 and target.id not in self.db.contaminated_entities:
            self.db.contaminated_entities.append(target.id)
            
        # React based on threat level
        if threat_category >= 4:
            self.emergency_protocol(target)
        elif threat_category >= 2:
            self.alert_protocol(target)
            
        self.db.is_scanning = False
        self.db.last_scan_time = time.time()
        
    def emergency_protocol(self, target):
        """Handle critical contamination detection."""
        self.location.msg_contents(
            f"|r{self.key} emits a piercing alarm! Red lights flash wildly!|n"
        )
        
        # Could trigger area lockdown, summon security, etc.
        
    def alert_protocol(self, target):
        """Handle moderate contamination detection."""
        self.location.msg_contents(
            f"|y{self.key}'s lights flash amber as it backs away cautiously.|n"
        )
        
    def area_scan(self):
        """Perform periodic area scan for substance."""
        if time.time() - self.db.last_scan_time < self.db.scan_interval:
            return
            
        # Check room contamination
        room_substance = getattr(self.location.db, "substance_level", 0)
        
        if room_substance > 0:
            self.location.msg_contents(
                f"{self.key} emits a concerned beeping. " +
                f'"Area contamination detected: Level {room_substance}"'
            )
            
        # Update threat assessment
        self.db.threat_level = room_substance
        
        # Scan all entities in room
        for obj in self.location.contents:
            if obj != self and hasattr(obj.db, "substance_level"):
                if obj.db.substance_level > 0:
                    self.scan_entity(obj)
                    break  # Only scan one at a time


class InfectedMachine(NPC):
    """
    A machine corrupted by the Substance.
    
    These are dangerous enemies that spread contamination and
    attack non-infected robots. They represent the Cogborn faction's
    corrupted members.
    """
    
    def at_object_creation(self):
        """Initialize an infected machine."""
        super().at_object_creation()
        
        self.key = "Infected Machine"
        self.db.desc = """This robot has been heavily corrupted by the Substance. 
Strange crystalline growths pulse with an eerie purple light across its 
chassis. Its movements are erratic and twitchy, and a low humming emanates 
from within. Oil-like substance occasionally drips from its joints."""
        
        # Combat stats
        self.db.is_npc = True
        self.db.hostile = True
        self.db.chassis_integrity = 150
        self.db.max_integrity = 150
        self.db.damage = 15
        self.db.defense = 5
        
        # Substance properties
        self.db.substance_level = randint(5, 8)
        self.db.substance_type = "infected"
        self.db.can_spread = True
        self.db.spread_chance = 30  # Percent chance to spread on hit
        
        # Behavior
        self.db.aggression = "high"
        self.db.faction = "cogborn"
        self.db.speaks_coherently = False
        
        # Combat messages
        self.db.attack_messages = [
            "lunges with substance-dripping claws",
            "releases a burst of contaminated vapor",
            "strikes with crystalline growths",
            "emits a piercing shriek and charges"
        ]
        
        # Loot
        self.db.drops_on_death = {
            "substance_sample": 50,  # 50% chance
            "corrupted_parts": 75,   # 75% chance
            "gold": 100             # Always drops 5-15 gold
        }
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """React aggressively to non-infected arrivals."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        
        # Attack non-infected robots
        if hasattr(moved_obj, "db") and hasattr(moved_obj.db, "chassis_integrity"):
            if getattr(moved_obj.db, "substance_level", 0) < 3:
                # Hostile to non-infected
                moved_obj.msg(f"|r{self.key} turns toward you with hostile intent!|n")
                self.location.msg_contents(
                    f"{self.key} emits a distorted growl and advances on {moved_obj.key}!",
                    exclude=[moved_obj]
                )
                
    def get_hit(self, attacker):
        """React to being attacked."""
        # Take damage
        damage = randint(10, 20)
        self.db.chassis_integrity -= damage
        
        attacker.msg(f"You strike {self.key} for {damage} damage!")
        self.location.msg_contents(
            f"{attacker.key} damages {self.key}! Purple fluid leaks from the wound.",
            exclude=[attacker]
        )
        
        # Chance to spread substance
        if self.db.can_spread and randint(1, 100) <= self.db.spread_chance:
            self.spread_substance(attacker)
            
        # Check for death
        if self.db.chassis_integrity <= 0:
            self.die(attacker)
        else:
            # Counter-attack
            self.attack(attacker)
            
    def spread_substance(self, target):
        """Attempt to contaminate a target."""
        if not hasattr(target.db, "substance_level"):
            target.db.substance_level = 0
            
        # Increase target's contamination
        increase = randint(1, 2)
        target.db.substance_level = min(10, target.db.substance_level + increase)
        
        target.msg(f"|rThe Substance splashes onto you! (Contamination +{increase})|n")
        
        # Get substance tracker script
        tracker = self.search("substance_tracker", global_search=True)
        if tracker and hasattr(tracker, "contaminate_object"):
            tracker.contaminate_object(target, increase)
            
    def attack(self, target):
        """Attack a target."""
        # Choose attack message
        attack_desc = choice(self.db.attack_messages)
        
        # Calculate damage
        damage = randint(self.db.damage - 5, self.db.damage + 5)
        
        # Apply damage
        if hasattr(target, "take_damage"):
            target.take_damage(damage)
            
        # Announce attack
        self.location.msg_contents(
            f"|r{self.key} {attack_desc} at {target.key}!|n"
        )
        
    def die(self, killer=None):
        """Handle death and drops."""
        self.location.msg_contents(
            f"|g{self.key} shudders and collapses, purple fluid pooling beneath it.|n"
        )
        
        # Drop loot
        if killer:
            # Gold
            gold_amount = randint(5, 15)
            killer.db.gold = (killer.db.gold or 0) + gold_amount
            killer.msg(f"|yYou collect {gold_amount} gold from the remains.|n")
            
            # Substance sample
            if randint(1, 100) <= self.db.drops_on_death["substance_sample"]:
                from evennia.objects.objects import DefaultObject
                sample = DefaultObject(key="Substance Sample")
                sample.location = self.location
                sample.save()
                sample.db.desc = "A sealed vial containing a sample of the mysterious Substance. It glows faintly purple."
                sample.db.item_type = "quest_item"
                sample.db.value = 50
                
            # Award XP
            if hasattr(killer, "gain_experience"):
                killer.gain_experience(25)
                
        # Remove from game
        self.delete()


class SubstancePurifier(DefaultCharacter):
    """
    Special NPC that can reduce substance contamination.
    
    These rare NPCs offer decontamination services, usually for
    a price or quest requirement.
    """
    
    def at_object_creation(self):
        """Initialize the purifier."""
        super().at_object_creation()
        
        self.key = "Decontamination Unit"
        self.db.desc = """A large, cylindrical machine with multiple articulated 
arms ending in various tools and nozzles. Clean white panels cover most of 
its surface, marked with faded medical symbols. A soft blue light emanates 
from within, and the air around it smells of ozone and cleaning chemicals."""
        
        self.db.is_npc = True
        self.db.service_type = "decontamination"
        self.db.cost_per_level = 10  # Gold per contamination level
        self.db.can_fully_purify = True
        
        # Add decontamination command set
        self.cmdset.add(DecontaminationCmdSet, persistent=True)
        
    def decontaminate(self, target):
        """Remove substance contamination from a target."""
        if not hasattr(target.db, "substance_level") or target.db.substance_level == 0:
            target.msg("You are not contaminated.")
            return False
            
        # Calculate cost
        cost = self.db.cost_per_level * target.db.substance_level
        
        if getattr(target.db, "gold", 0) < cost:
            target.msg(f"Decontamination costs {cost} gold. You only have {target.db.gold or 0}.")
            return False
            
        # Perform decontamination
        target.db.gold -= cost
        old_level = target.db.substance_level
        target.db.substance_level = 0
        
        # Announce
        self.location.msg_contents(
            f"{self.key} extends multiple arms toward {target.key}, " +
            "bathing them in cleansing blue light and chemical sprays."
        )
        
        target.msg(f"|gDecontamination complete! {old_level} levels of Substance removed.|n")
        target.msg(f"|yYou paid {cost} gold for the service.|n")
        
        return True


# Commands for substance-related interactions

class CmdDecontaminate(Command):
    """
    Request decontamination services.
    
    Usage:
        decontaminate
        purify
        
    If you're near a Decontamination Unit, you can pay to have
    substance contamination removed from your systems.
    """
    
    key = "decontaminate"
    aliases = ["purify", "cleanse"]
    
    def func(self):
        # Find decontamination unit in room
        for obj in self.caller.location.contents:
            if hasattr(obj.db, "service_type") and obj.db.service_type == "decontamination":
                obj.decontaminate(self.caller)
                return
                
        self.caller.msg("There's no decontamination service available here.")


class CmdScanSubstance(Command):
    """
    Check your current substance contamination level.
    
    Usage:
        substance
        contamination
        
    Display your current substance contamination level and its effects.
    """
    
    key = "substance"
    aliases = ["contamination"]
    
    def func(self):
        level = getattr(self.caller.db, "substance_level", 0)
        
        self.caller.msg("|m=== Substance Contamination ===|n")
        self.caller.msg(f"|wCurrent Level:|n {level}/10")
        
        # Show contamination bar
        bar_length = 20
        filled = int((level / 10) * bar_length)
        bar = "|m" + "█" * filled + "|x" + "░" * (bar_length - filled) + "|n"
        self.caller.msg(f"|wContamination:|n [{bar}]")
        
        # Describe effects
        if level == 0:
            self.caller.msg("|gYou are free of substance contamination.|n")
        elif level <= 2:
            self.caller.msg("|yMinor contamination detected. Slight system irregularities.|n")
        elif level <= 4:
            self.caller.msg("|yModerate contamination. Performance degradation noticeable.|n")
        elif level <= 6:
            self.caller.msg("|rHigh contamination! Systems experiencing errors.|n")
        elif level <= 8:
            self.caller.msg("|rCritical contamination! Major system corruption!|n")
        else:
            self.caller.msg("|m[MAXIMUM CONTAMINATION - SYSTEM CRITICAL]|n")
            
        # Show effects on stats
        if level > 0:
            speed_penalty = level * 2
            defense_penalty = level
            self.caller.msg(f"\n|wEffects:|n")
            self.caller.msg(f"  Speed: -{speed_penalty}")
            self.caller.msg(f"  Defense: -{defense_penalty}")
            if level >= 5:
                self.caller.msg(f"  |rRandom system glitches|n")


# Command sets

class DecontaminationCmdSet(CmdSet):
    """Commands available near decontamination units."""
    def at_cmdset_creation(self):
        self.add(CmdDecontaminate())
        
        
class SubstanceCmdSet(CmdSet):
    """General substance-related commands."""
    def at_cmdset_creation(self):
        self.add(CmdScanSubstance())