"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent
from .robots import RobotCharacter


class Character(ObjectParent, RobotCharacter):
    """
    The Character is a robot entity that players control.
    
    All characters in pixariMud are robots that start with minimal parts
    and must find/attach components to gain full functionality. This class
    combines the robot assembly mechanics with RPG progression systems.
    """

    def at_object_creation(self):
        """
        Called only once when character is first created.
        Initialize both robot and RPG stats.
        """
        # Initialize robot components first
        super().at_object_creation()
        
        # RPG stats (in addition to robot stats)
        self.db.experience = 0
        self.db.gold = 50  # Starting gold
        
        # Set respawn location to current location initially
        self.db.respawn_location = self.location
        
        # Start with only right arm attached (as per narrative)
        from evennia import create_object
        from typeclasses.robot_parts import RobotArm
        starting_arm = create_object(RobotArm, key="Right Robot Arm")
        starting_arm.db.part_slot = "right_arm"
        starting_arm.db.quality = "standard"
        starting_arm.db.material = "worn steel"
        self.attach_part(starting_arm, "right_arm")

    def ensure_stats_initialized(self):
        """
        Ensure both robot and RPG stats are initialized (for existing characters).
        """
        # Robot stats (energy and integrity replace health)
        if self.db.energy is None:
            self.db.energy = 100
        if self.db.max_energy is None:
            self.db.max_energy = 100
        if self.db.chassis_integrity is None:
            self.db.chassis_integrity = 100
        if self.db.max_integrity is None:
            self.db.max_integrity = 100
            
        # RPG stats
        if self.db.experience is None:
            self.db.experience = 0
        if self.db.respawn_location is None:
            self.db.respawn_location = self.location
        if self.db.gold is None:
            self.db.gold = 50
            
        # Robot parts - ensure basic structure
        if not hasattr(self.db, "attached_parts"):
            self.db.attached_parts = {
                "head": None,
                "torso": None,
                "left_arm": None,
                "right_arm": None,
                "left_leg": None,
                "right_leg": None
            }
        if not hasattr(self.db, "movement_mode"):
            self.recalculate_stats()

    @property
    def level(self):
        """Calculate level based on experience (every 100 XP = 1 level)"""
        self.ensure_stats_initialized()
        return max(1, (self.db.experience // 100) + 1)

    def gain_experience(self, amount):
        """
        Add experience points and check for level up.
        """
        self.ensure_stats_initialized()
        old_level = self.level
        self.db.experience += amount
        new_level = self.level
        
        self.msg(f"You gain {amount} experience! (Total: {self.db.experience})")
        
        # Check for level up
        if new_level > old_level:
            self.msg(f"|yYou have reached level {new_level}!|n")
            self.level_up(new_level)

    def level_up(self, new_level):
        """
        Handle level up effects for robots.
        """
        # Increase max integrity by 10 per level
        old_max_integrity = self.db.max_integrity
        self.db.max_integrity = 100 + ((new_level - 1) * 10)
        integrity_increase = self.db.max_integrity - old_max_integrity
        
        # Increase max energy by 5 per level
        old_max_energy = self.db.max_energy
        self.db.max_energy = int((100 + ((new_level - 1) * 5)) * self.db.energy_efficiency)
        energy_increase = self.db.max_energy - old_max_energy
        
        # Full repair and recharge on level up
        self.db.chassis_integrity = self.db.max_integrity
        self.db.energy = self.db.max_energy
        
        self.msg(f"|gMaximum integrity increased by {integrity_increase}! (Now {self.db.max_integrity})|n")
        self.msg(f"|gMaximum energy increased by {energy_increase}! (Now {self.db.max_energy})|n")
        self.msg(f"|gFully repaired and recharged!|n")

    def take_damage(self, amount):
        """
        Take damage to chassis integrity and handle destruction if it reaches 0.
        """
        self.ensure_stats_initialized()
        # Apply defense from parts
        actual_damage = max(1, amount - (self.db.defense // 2))
        self.db.chassis_integrity = max(0, self.db.chassis_integrity - actual_damage)
        
        self.msg(f"|rYou take {actual_damage} damage! (Integrity: {self.db.chassis_integrity}/{self.db.max_integrity})|n")
        
        if self.db.chassis_integrity <= 0:
            self.die()
            return True  # Destroyed
        return False  # Still functional

    def heal(self, amount):
        """
        Repair chassis integrity, capped at max_integrity.
        """
        self.ensure_stats_initialized()
        old_integrity = self.db.chassis_integrity
        self.db.chassis_integrity = min(self.db.max_integrity, self.db.chassis_integrity + amount)
        actual_repair = self.db.chassis_integrity - old_integrity
        
        if actual_repair > 0:
            self.msg(f"|gYou repair {actual_repair} integrity! ({self.db.chassis_integrity}/{self.db.max_integrity})|n")

    def die(self):
        """
        Handle robot destruction and reconstruction.
        """
        self.ensure_stats_initialized()
        self.msg("|rCRITICAL SYSTEM FAILURE! Chassis destroyed!|n")
        self.location.msg_contents(f"|r{self.key}'s chassis crumbles into scrap!|n", exclude=self)
        
        # Move to respawn location
        respawn_loc = self.db.respawn_location
        if respawn_loc:
            self.move_to(respawn_loc, quiet=True)
        
        # Restore to full integrity and energy
        self.db.chassis_integrity = self.db.max_integrity
        self.db.energy = self.db.max_energy
        
        self.msg("|gEmergency reconstruction complete! Systems online!|n")
        self.location.msg_contents(f"|g{self.key} emerges from the reconstruction chamber!|n", exclude=self)

    def set_respawn_location(self, location):
        """
        Set the reconstruction chamber location for this robot.
        """
        self.db.respawn_location = location
        self.msg(f"Reconstruction chamber location set to {location.key}.")
