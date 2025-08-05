"""
Robot character system with modular body parts.

This module implements the core robot body mechanics where players
control robots that can attach/detach parts to gain abilities.
"""

from evennia.objects.objects import DefaultCharacter
from evennia.commands.command import Command
from evennia.commands.cmdset import CmdSet
from evennia.utils.evtable import EvTable
import time


class RobotCharacter(DefaultCharacter):
    """
    Robot characters that can have parts attached and detached.
    
    Players start with minimal parts and must find/attach more to
    gain full functionality. Different part combinations provide
    different stats and abilities.
    """
    
    def at_object_creation(self):
        """Initialize robot with minimal parts."""
        super().at_object_creation()
        
        # Core robot attributes
        self.db.is_robot = True
        self.db.robot_type = "scavenger"  # Could have different types later
        
        # Part slots - what can be attached where
        self.db.attached_parts = {
            "head": None,
            "torso": None,
            "left_arm": None,
            "right_arm": None,
            "left_leg": None,
            "right_leg": None
        }
        
        # Movement states based on attached parts
        self.db.movement_mode = "crawl"  # crawl, limp, walk, run
        self.db.manipulation_level = 0   # 0-2 based on arms
        
        # Robot-specific stats
        self.db.energy = 100
        self.db.max_energy = 100
        self.db.chassis_integrity = 100
        self.db.max_integrity = 100
        
        # Substance contamination level
        self.db.substance_level = 0
        
        # Add robot-specific command set
        self.cmdset.add(RobotCmdSet, persistent=True)
        
    def at_init(self):
        """Called when robot loads."""
        super().at_init()
        # Recalculate stats based on attached parts
        self.recalculate_stats()
        # Re-apply part command sets
        self.update_part_commands()
        
    def attach_part(self, part, slot=None):
        """
        Attach a robot part to this body.
        
        Args:
            part: RobotPart object to attach
            slot: Specific slot to use (auto-detect if None)
            
        Returns:
            success (bool), message (str)
        """
        # Check if it's a robot part by checking for required attributes
        if not hasattr(part.db, "part_type") or not hasattr(part.db, "part_slot"):
            return False, f"{part.key} is not a robot part."
            
        # Auto-detect slot if not specified
        if not slot:
            slot = part.db.part_slot
            
        # Check if slot exists
        if slot not in self.db.attached_parts:
            return False, f"No {slot} attachment point available."
            
        # Check if slot is occupied
        if self.db.attached_parts[slot]:
            return False, f"Your {slot} slot already has {self.db.attached_parts[slot].key} attached."
            
        # Check part compatibility
        if part.db.part_slot != slot:
            return False, f"{part.key} cannot be attached to {slot} slot."
            
        # Attach the part
        self.db.attached_parts[slot] = part
        part.location = None  # Remove from room
        part.db.attached_to = self
        
        # Add part's commands if any
        if hasattr(part, 'provide_commands'):
            cmdset = part.provide_commands()
            if cmdset:
                self.cmdset.add(cmdset)
                
        # Recalculate stats
        self.recalculate_stats()
        
        # Special messages for critical parts
        if part.db.part_type == "leg":
            if self.count_legs() == 1:
                return True, f"You attach {part.key}. You can now limp around slowly."
            elif self.count_legs() == 2:
                return True, f"You attach {part.key}. You can now walk normally!"
        elif part.db.part_type == "arm":
            if self.count_arms() == 1:
                return True, f"You attach {part.key}. Basic manipulation restored."
            elif self.count_arms() == 2:
                return True, f"You attach {part.key}. Full manipulation capabilities online!"
                
        return True, f"You successfully attach {part.key} to your {slot}."
        
    def detach_part(self, slot):
        """
        Remove a part from the specified slot.
        
        Args:
            slot: Slot name to detach from
            
        Returns:
            success (bool), message (str)
        """
        if slot not in self.db.attached_parts:
            return False, f"No {slot} attachment point."
            
        part = self.db.attached_parts[slot]
        if not part:
            return False, f"No part attached to {slot}."
            
        # Remove part
        self.db.attached_parts[slot] = None
        part.location = self.location
        part.db.attached_to = None
        
        # Remove part's commands
        if hasattr(part, 'provide_commands'):
            cmdset = part.provide_commands()
            if cmdset:
                # Create a removal cmdset with same key
                for cmd in cmdset.commands:
                    self.cmdset.remove(cmd)
                    
        # Recalculate stats
        self.recalculate_stats()
        
        return True, f"You detach {part.key} from your {slot}."
        
    def count_legs(self):
        """Return number of attached legs."""
        if not hasattr(self.db, "attached_parts") or self.db.attached_parts is None:
            self.db.attached_parts = {}
        return sum(1 for slot in ["left_leg", "right_leg"] 
                  if self.db.attached_parts.get(slot))
                  
    def count_arms(self):
        """Return number of attached arms."""
        if not hasattr(self.db, "attached_parts") or self.db.attached_parts is None:
            self.db.attached_parts = {}
        return sum(1 for slot in ["left_arm", "right_arm"] 
                  if self.db.attached_parts.get(slot))
                  
    def has_head(self):
        """Check if head is attached."""
        if not hasattr(self.db, "attached_parts") or self.db.attached_parts is None:
            self.db.attached_parts = {}
        return bool(self.db.attached_parts.get("head"))
        
    def has_torso(self):
        """Check if torso is attached."""
        if not hasattr(self.db, "attached_parts") or self.db.attached_parts is None:
            self.db.attached_parts = {}
        return bool(self.db.attached_parts.get("torso"))
        
    def recalculate_stats(self):
        """Recalculate all stats based on attached parts."""
        # Reset to base values
        speed = 0
        strength = 0  
        defense = 0
        energy_efficiency = 1.0
        
        # Sum up part contributions
        for slot, part in self.db.attached_parts.items():
            if part:
                mult = part.get_quality_multiplier()
                speed += int(part.db.speed_modifier * mult)
                strength += int(part.db.strength_modifier * mult)
                defense += int(part.db.defense_modifier * mult)
                energy_efficiency *= part.db.energy_efficiency * mult
                
        # Apply to character stats
        self.db.speed = max(1, speed)
        self.db.strength = max(1, strength)
        self.db.defense = max(1, defense)
        self.db.energy_efficiency = energy_efficiency
        
        # Update movement mode based on legs
        leg_count = self.count_legs()
        if leg_count == 0:
            self.db.movement_mode = "crawl"
            self.db.speed = max(1, self.db.speed // 4)  # 75% speed penalty
        elif leg_count == 1:
            self.db.movement_mode = "limp"
            self.db.movement_mode = "limp"
            self.db.speed = max(1, self.db.speed // 2)  # 50% speed penalty
        else:
            self.db.movement_mode = "walk"
            
        # Update manipulation based on arms
        self.db.manipulation_level = self.count_arms()
        
        # Update max health based on defense
        base_health = 100
        self.db.max_health = base_health + (self.db.defense * 5)
        
        # Update max energy based on efficiency
        base_energy = 100
        self.db.max_energy = int(base_energy * self.db.energy_efficiency)
        
    def update_part_commands(self):
        """Re-apply command sets from all attached parts."""
        for slot, part in self.db.attached_parts.items():
            if part and hasattr(part, 'provide_commands'):
                cmdset = part.provide_commands()
                if cmdset:
                    self.cmdset.add(cmdset)
                    
    def at_pre_move(self, destination, **kwargs):
        """Check movement restrictions before moving."""
        # Check if we have legs
        if self.count_legs() == 0:
            self.msg("|rYou cannot move without any legs! You'll need to crawl.|n")
            self.msg("Hint: Use 'crawl <direction>' to slowly drag yourself.")
            return False
            
        # Slower movement with one leg
        if self.count_legs() == 1:
            # Add a small delay to simulate limping
            delay = getattr(self.ndb, "last_move_time", 0)
            if time.time() - delay < 2:
                self.msg("You're still recovering from your last limping step.")
                return False
            self.ndb.last_move_time = time.time()
            
        return super().at_pre_move(destination, **kwargs)
        
    def return_appearance(self, looker, **kwargs):
        """Custom appearance showing attached parts."""
        # Get base appearance
        string = f"|c{self.key}|n\n"
        if self.db.desc:
            string += self.db.desc
        else:
            string += "A modular robot awaiting configuration."
            
        # Show attached parts
        string += "\n\n|wAttached Components:|n"
        
        parts_table = EvTable(
            "|wSlot|n", "|wAttached Part|n", "|wQuality|n",
            border="cells", width=60
        )
        
        for slot_name, part in self.db.attached_parts.items():
            slot_display = slot_name.replace('_', ' ').title()
            if part:
                parts_table.add_row(
                    slot_display,
                    part.key,
                    part.get_display_name()
                )
            else:
                parts_table.add_row(
                    slot_display,
                    "|r-MISSING-|n",
                    ""
                )
                
        string += f"\n{parts_table}"
        
        # Movement status
        string += f"\n\n|wMovement:|n {self.db.movement_mode.title()}"
        string += f"\n|wManipulation:|n Level {self.db.manipulation_level}"
        
        # Stats summary
        string += f"\n\n|wStats:|n"
        string += f"\n  Speed: {self.db.speed}"
        string += f"\n  Strength: {self.db.strength}"
        string += f"\n  Defense: {self.db.defense}"
        string += f"\n  Energy Efficiency: {int(self.db.energy_efficiency * 100)}%"
        
        # Substance warning
        if self.db.substance_level > 0:
            string += f"\n\n|rSubstance Contamination:|n Level {self.db.substance_level}"
            
        # Contents (inventory)
        things = [obj for obj in self.contents if obj != looker]
        if things:
            string += "\n\n|wCarrying:|n"
            for thing in things:
                string += f"\n  {thing.get_display_name(looker)}"
                
        return string


# Robot-specific commands

class CmdAttach(Command):
    """
    Attach a robot part to your body.
    
    Usage:
        attach <part>
        attach <part> to <slot>
        
    Attaches a robot part you're carrying to an available slot on
    your body. If no slot is specified, it will try to auto-detect
    the correct slot based on the part type.
    
    Examples:
        attach left arm
        attach servo to right_leg
    """
    
    key = "attach"
    aliases = ["install", "equip"]
    
    def func(self):
        if not self.args:
            self.caller.msg("Attach what part?")
            return
            
        # Parse arguments for "part to slot" format
        if " to " in self.args:
            part_name, slot = self.args.split(" to ", 1)
            slot = slot.strip().replace(' ', '_')
        else:
            part_name = self.args
            slot = None
            
        # Find the part in inventory
        part = self.caller.search(part_name, location=self.caller)
        if not part:
            return
            
        # Try to attach
        success, message = self.caller.attach_part(part, slot)
        self.caller.msg(message)
        
        if success:
            self.caller.location.msg_contents(
                f"{self.caller.key} attaches {part.key} with a series of clicks and whirs.",
                exclude=[self.caller]
            )


class CmdDetach(Command):
    """
    Remove an attached part from your body.
    
    Usage:
        detach <slot>
        remove <part name>
        
    Detaches a part and drops it on the ground. You can specify
    either the slot name or the part name.
    
    Examples:
        detach left_arm
        remove rusty servo
    """
    
    key = "detach"
    aliases = ["remove", "uninstall"]
    
    def func(self):
        if not self.args:
            self.caller.msg("Detach what part?")
            return
            
        # Try to match by slot name first
        slot = self.args.strip().replace(' ', '_')
        if slot in self.caller.db.attached_parts:
            success, message = self.caller.detach_part(slot)
            self.caller.msg(message)
            if success:
                self.caller.location.msg_contents(
                    f"{self.caller.key} detaches a part with a hiss of released pressure.",
                    exclude=[self.caller]
                )
            return
            
        # Try to find by part name
        for slot, part in self.caller.db.attached_parts.items():
            if part and self.args.lower() in part.key.lower():
                success, message = self.caller.detach_part(slot)
                self.caller.msg(message)
                if success:
                    self.caller.location.msg_contents(
                        f"{self.caller.key} detaches {part.key} with mechanical precision.",
                        exclude=[self.caller]
                    )
                return
                
        self.caller.msg(f"No part matching '{self.args}' is attached.")


class CmdParts(Command):
    """
    Display your attached parts and stats.
    
    Usage:
        parts
        components
        
    Shows all attachment slots, what's installed, and the stats
    provided by your current configuration.
    """
    
    key = "parts"
    aliases = ["components", "mods"]
    
    def func(self):
        self.caller.msg(self.caller.return_appearance(self.caller))


class CmdCrawl(Command):
    """
    Slowly crawl in a direction without legs.
    
    Usage:
        crawl <direction>
        
    When you have no legs attached, this is your only movement option.
    It's very slow and costs energy.
    """
    
    key = "crawl"
    aliases = ["drag"]
    
    def func(self):
        if not self.args:
            self.caller.msg("Crawl in which direction?")
            return
            
        # Check if they actually need to crawl
        if self.caller.count_legs() > 0:
            self.caller.msg("You have legs attached. Just walk normally!")
            return
            
        # Check energy
        if self.caller.db.energy < 5:
            self.caller.msg("You're too exhausted to crawl. You need to rest and recharge.")
            return
            
        # Check cooldown
        last_crawl = self.caller.db.last_crawl_time or 0
        if time.time() - last_crawl < 5:
            remaining = int(5 - (time.time() - last_crawl))
            self.caller.msg(f"You're still recovering. Wait {remaining} more seconds.")
            return
            
        # Find the exit
        exit_obj = self.caller.search(self.args, candidates=self.caller.location.exits)
        if not exit_obj:
            self.caller.msg("You can't crawl that way.")
            return
            
        # Consume energy
        self.caller.db.energy -= 5
        self.caller.db.last_crawl_time = time.time()
        
        # Announce the crawling
        self.caller.location.msg_contents(
            f"{self.caller.key} slowly drags themselves across the floor.",
            exclude=[self.caller]
        )
        
        # Move to destination
        self.caller.move_to(exit_obj.destination)
        
        # Announce arrival
        self.caller.location.msg_contents(
            f"{self.caller.key} crawls in from {exit_obj.reverse_exit().key if exit_obj.reverse_exit() else 'somewhere'}.",
            exclude=[self.caller]
        )
        
        self.caller.msg(f"You painfully drag yourself {exit_obj.key}.")


class CmdDiagnostics(Command):
    """
    Run a self-diagnostic check.
    
    Usage:
        diagnostics
        diag
        
    Displays detailed information about your robot's condition,
    including energy levels, part integrity, and any system warnings.
    """
    
    key = "diagnostics"
    aliases = ["diag", "status", "check"]
    
    def func(self):
        robot = self.caller
        
        self.caller.msg("|g=== SYSTEM DIAGNOSTICS ===|n")
        self.caller.msg(f"|wModel:|n {robot.key}")
        self.caller.msg(f"|wType:|n {robot.db.robot_type.title()}")
        
        # Energy status
        energy_percent = int((robot.db.energy / robot.db.max_energy) * 100)
        energy_bar = self.make_bar(energy_percent, 20, "|b", "|x")
        self.caller.msg(f"|wEnergy:|n [{energy_bar}|n] {robot.db.energy}/{robot.db.max_energy} ({energy_percent}%)")
        
        # Integrity status
        integrity_percent = int((robot.db.chassis_integrity / robot.db.max_integrity) * 100)
        integrity_bar = self.make_bar(integrity_percent, 20, "|g", "|r")
        self.caller.msg(f"|wIntegrity:|n [{integrity_bar}|n] {robot.db.chassis_integrity}/{robot.db.max_integrity} ({integrity_percent}%)")
        
        # Movement systems
        self.caller.msg(f"\n|wLocomotion:|n {robot.db.movement_mode.title()}")
        self.caller.msg(f"|wManipulators:|n Level {robot.db.manipulation_level}")
        
        # Part summary
        total_parts = sum(1 for p in robot.db.attached_parts.values() if p)
        self.caller.msg(f"\n|wInstalled Components:|n {total_parts}/6")
        
        # Warnings
        warnings = []
        if robot.count_legs() == 0:
            warnings.append("|rCRITICAL: No locomotion units installed|n")
        elif robot.count_legs() == 1:
            warnings.append("|yWARNING: Locomotion impaired - single leg mode|n")
            
        if robot.count_arms() == 0:
            warnings.append("|rCRITICAL: No manipulation units installed|n")
            
        if not robot.has_head():
            warnings.append("|yWARNING: No sensor package installed|n")
            
        if robot.db.substance_level > 0:
            warnings.append(f"|rALERT: Substance contamination detected (Level {robot.db.substance_level})|n")
            
        if warnings:
            self.caller.msg("\n|r=== SYSTEM WARNINGS ===|n")
            for warning in warnings:
                self.caller.msg(f"! {warning}")
                
    def make_bar(self, percent, width, full_color, empty_color):
        """Create a progress bar."""
        filled = int((percent / 100) * width)
        empty = width - filled
        return f"{full_color}{'█' * filled}{empty_color}{'░' * empty}|n"


# Command set for robots

class RobotCmdSet(CmdSet):
    """Commands available to robot characters."""
    
    def at_cmdset_creation(self):
        self.add(CmdAttach())
        self.add(CmdDetach())
        self.add(CmdParts())
        self.add(CmdCrawl())
        self.add(CmdDiagnostics())