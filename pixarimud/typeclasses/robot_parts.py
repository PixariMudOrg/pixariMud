"""
Robot body parts and assembly system for pixariMud.

This module implements the limb collection and attachment mechanics where
players start with missing body parts and must find/attach them to gain
full mobility and capabilities.
"""

from evennia.objects.objects import DefaultObject
from evennia.commands.command import Command
from evennia.commands.cmdset import CmdSet
from evennia.utils.evtable import EvTable
from random import choice, randint
import time


class RobotPart(DefaultObject):
    """
    Base class for robot body parts that can be found and attached.
    
    Parts have quality levels that affect the stats they provide:
    - Damaged: 50-70% effectiveness
    - Standard: 80-100% effectiveness  
    - Enhanced: 110-130% effectiveness
    - Pristine: 140-160% effectiveness
    """
    
    def at_object_creation(self):
        """Set up the part with default values."""
        super().at_object_creation()
        
        # Part properties
        self.db.part_type = "generic"  # arm, leg, head, torso
        self.db.part_slot = "generic"  # left_arm, right_arm, etc.
        self.db.quality = "standard"   # damaged, standard, enhanced, pristine
        self.db.weight = 5.0
        
        # Stat modifiers
        self.db.speed_modifier = 0
        self.db.strength_modifier = 0  
        self.db.defense_modifier = 0
        self.db.energy_efficiency = 1.0
        
        # Visual description elements
        self.db.material = "steel"
        self.db.condition_desc = "functional"
        
    def get_quality_multiplier(self):
        """Return stat multiplier based on quality."""
        multipliers = {
            "damaged": 0.6,
            "standard": 0.9,
            "enhanced": 1.2,
            "pristine": 1.5
        }
        return multipliers.get(self.db.quality, 1.0)
    
    def get_display_name(self):
        """Return formatted name with quality indicator."""
        quality_colors = {
            "damaged": "|r",
            "standard": "|w",
            "enhanced": "|g",
            "pristine": "|m"
        }
        color = quality_colors.get(self.db.quality, "|w")
        return f"{color}{self.key}|n"
    
    def return_appearance(self, looker, **kwargs):
        """Detailed description when examined."""
        string = super().return_appearance(looker, **kwargs)
        
        # Add part details
        string += f"\n\n|cPart Type:|n {self.db.part_type.title()}"
        string += f"\n|cSlot:|n {self.db.part_slot.replace('_', ' ').title()}"
        string += f"\n|cQuality:|n {self.get_display_name()}"
        string += f"\n|cWeight:|n {self.db.weight} kg"
        string += f"\n|cMaterial:|n {self.db.material}"
        
        # Show stat modifiers
        mult = self.get_quality_multiplier()
        if self.db.speed_modifier:
            string += f"\n|cSpeed:|n +{int(self.db.speed_modifier * mult)}"
        if self.db.strength_modifier:
            string += f"\n|cStrength:|n +{int(self.db.strength_modifier * mult)}"
        if self.db.defense_modifier:
            string += f"\n|cDefense:|n +{int(self.db.defense_modifier * mult)}"
        if self.db.energy_efficiency != 1.0:
            string += f"\n|cEnergy Efficiency:|n {int(self.db.energy_efficiency * mult * 100)}%"
            
        return string


class RobotArm(RobotPart):
    """A robot arm that can be attached to left or right side."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.part_type = "arm"
        self.db.strength_modifier = 5
        self.db.weight = 8.0
        
        # Randomize which side if not set
        if not hasattr(self.db, "part_slot") or self.db.part_slot == "generic":
            self.db.part_slot = choice(["left_arm", "right_arm"])
            
        # Set name based on slot
        side = "Left" if "left" in self.db.part_slot else "Right"
        self.key = f"{side} Robot Arm"
        
    def provide_commands(self):
        """Return commands this arm enables."""
        from evennia import CmdSet
        
        cmdset = CmdSet()
        # Different commands for different quality levels
        if self.db.quality in ["enhanced", "pristine"]:
            cmdset.add(CmdPowerGrip())
        cmdset.add(CmdGrab())
        return cmdset


class RobotLeg(RobotPart):
    """A robot leg that enables movement."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.part_type = "leg"
        self.db.speed_modifier = 3
        self.db.defense_modifier = 2
        self.db.weight = 12.0
        
        # Randomize which side
        if not hasattr(self.db, "part_slot") or self.db.part_slot == "generic":
            self.db.part_slot = choice(["left_leg", "right_leg"])
            
        side = "Left" if "left" in self.db.part_slot else "Right"
        self.key = f"{side} Robot Leg"


class RobotHead(RobotPart):
    """A robot head unit with sensors and processing."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.part_type = "head"
        self.db.part_slot = "head"
        self.db.defense_modifier = 3
        self.db.energy_efficiency = 1.2
        self.db.weight = 6.0
        self.key = "Robot Head Unit"
        
    def provide_commands(self):
        """Head units provide scanning abilities."""
        from evennia import CmdSet
        
        cmdset = CmdSet()
        cmdset.add(CmdScan())
        if self.db.quality in ["enhanced", "pristine"]:
            cmdset.add(CmdAnalyze())
        return cmdset


class RobotTorso(RobotPart):
    """A robot torso/chassis that serves as the main body."""
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.part_type = "torso"  
        self.db.part_slot = "torso"
        self.db.defense_modifier = 8
        self.db.strength_modifier = 2
        self.db.weight = 20.0
        self.key = "Robot Torso"


# Part generation functions

def generate_random_part(part_type=None, quality=None):
    """
    Generate a random robot part with randomized properties.
    
    Args:
        part_type: Specific type to generate (arm, leg, head, torso)
        quality: Specific quality level
        
    Returns:
        RobotPart instance
    """
    # Choose random type if not specified
    if not part_type:
        part_type = choice(["arm", "arm", "leg", "leg", "head", "torso"])
        
    # Choose random quality with weighted distribution
    if not quality:
        qualities = ["damaged"] * 40 + ["standard"] * 40 + ["enhanced"] * 15 + ["pristine"] * 5
        quality = choice(qualities)
    
    # Create the appropriate part
    part_classes = {
        "arm": RobotArm,
        "leg": RobotLeg,
        "head": RobotHead,
        "torso": RobotTorso
    }
    
    part_class = part_classes.get(part_type, RobotPart)
    part = part_class(key=f"Robot {part_type.title()}")
    part.save()
    part.db.quality = quality
    
    # Randomize materials and descriptions based on quality
    materials = {
        "damaged": ["rusted steel", "cracked aluminum", "worn iron"],
        "standard": ["steel", "aluminum alloy", "reinforced plastic"],
        "enhanced": ["titanium alloy", "carbon composite", "hardened steel"],
        "pristine": ["military-grade alloy", "nanocomposite", "quantum steel"]
    }
    
    part.db.material = choice(materials.get(quality, ["steel"]))
    
    # Add some flavor text
    conditions = {
        "damaged": ["heavily worn", "barely functional", "held together with tape"],
        "standard": ["functional", "serviceable", "well-used"],
        "enhanced": ["high-performance", "upgraded", "modified"],
        "pristine": ["factory-new", "military-spec", "cutting-edge"]
    }
    
    part.db.condition_desc = choice(conditions.get(quality, ["functional"]))
    
    return part


# Commands provided by parts

class CmdGrab(Command):
    """
    Grab objects with your robot arm.
    
    Usage:
        grab <object>
        
    Basic gripping functionality provided by any robot arm.
    """
    key = "grab"
    aliases = ["grip", "grasp"]
    
    def func(self):
        if not self.args:
            self.caller.msg("Grab what?")
            return
            
        obj = self.caller.search(self.args, location=self.caller.location)
        if not obj:
            return
            
        # Check if we can grab it
        if obj.db.weight and obj.db.weight > 20:
            self.caller.msg(f"{obj.key} is too heavy for your arm to lift.")
            return
            
        self.caller.msg(f"You grab {obj.key} with your robot arm.")
        self.caller.location.msg_contents(
            f"{self.caller.key} grabs {obj.key} with their robot arm.",
            exclude=[self.caller]
        )


class CmdPowerGrip(Command):
    """
    Enhanced gripping with superior robot arms.
    
    Usage:
        powergrip <object>
        crush <object>
        
    Only available with enhanced or pristine arms.
    """
    key = "powergrip"
    aliases = ["crush", "squeeze"]
    
    def func(self):
        if not self.args:
            self.caller.msg("Power grip what?")
            return
            
        obj = self.caller.search(self.args, location=self.caller.location)
        if not obj:
            return
            
        self.caller.msg(f"You apply crushing force to {obj.key} with your enhanced arm!")
        self.caller.location.msg_contents(
            f"{self.caller.key}'s arm servos whine as they crush {obj.key}!",
            exclude=[self.caller]
        )
        
        # Could add actual crushing mechanics here
        if hasattr(obj, "at_crush"):
            obj.at_crush(self.caller)


class CmdScan(Command):
    """
    Scan your surroundings with head sensors.
    
    Usage:
        scan
        scan <object>
        
    Requires a robot head unit to be attached.
    """
    key = "scan"
    aliases = ["sensors"]
    
    def func(self):
        if self.args:
            # Scan specific object
            obj = self.caller.search(self.args)
            if not obj:
                return
                
            self.caller.msg(f"|cScanning {obj.key}...|n")
            
            # Show extra info based on head quality
            robot = self.caller.db.robot_body
            head_quality = "standard"
            if robot and robot.db.attached_parts.get("head"):
                head = robot.db.attached_parts["head"]
                head_quality = head.db.quality
                
            if head_quality in ["enhanced", "pristine"]:
                # Show hidden attributes
                if hasattr(obj.db, "substance_level"):
                    self.caller.msg(f"|rSubstance Detected:|n Level {obj.db.substance_level}")
                if hasattr(obj.db, "hidden_compartment"):
                    self.caller.msg("|gHidden compartment detected!|n")
        else:
            # General area scan
            self.caller.msg("|cActivating area sensors...|n")
            
            # Count objects and exits
            room = self.caller.location
            object_count = len([obj for obj in room.contents if obj != self.caller])
            exit_count = len(room.exits)
            
            self.caller.msg(f"Detected: {object_count} objects, {exit_count} exits")
            
            # Check for substance
            if room.db.substance_level:
                self.caller.msg(f"|rWarning: Substance detected in area!|n")


class CmdAnalyze(Command):
    """
    Deep analysis with advanced head units.
    
    Usage:
        analyze <object>
        
    Only available with enhanced or pristine head units.
    """
    key = "analyze" 
    
    def func(self):
        if not self.args:
            self.caller.msg("Analyze what?")
            return
            
        obj = self.caller.search(self.args)
        if not obj:
            return
            
        self.caller.msg(f"|cPerforming deep analysis of {obj.key}...|n")
        
        # Show all available information
        if hasattr(obj, "db"):
            attrs = [attr for attr in dir(obj.db) if not attr.startswith('_')]
            if attrs:
                self.caller.msg("|gDetailed scan results:|n")
                for attr in attrs[:5]:  # Limit output
                    value = getattr(obj.db, attr)
                    if value is not None:
                        self.caller.msg(f"  {attr}: {value}")