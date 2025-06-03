"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

from evennia.objects.objects import DefaultCharacter

from .objects import ObjectParent


class Character(ObjectParent, DefaultCharacter):
    """
    The Character just re-implements some of the Object's methods and hooks
    to represent a Character entity in-game.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Object child classes like this.

    """

    def at_object_creation(self):
        """
        Called only once when character is first created.
        Initialize character stats.
        """
        super().at_object_creation()
        
        # Initialize character stats
        self.db.health = 100
        self.db.max_health = 100
        self.db.experience = 0
        self.db.level = 1
        
        # Set respawn location to current location initially
        self.db.respawn_location = self.location

    def ensure_stats_initialized(self):
        """
        Ensure character stats are initialized (for existing characters).
        """
        if self.db.health is None:
            self.db.health = 100
        if self.db.max_health is None:
            self.db.max_health = 100
        if self.db.experience is None:
            self.db.experience = 0
        if self.db.respawn_location is None:
            self.db.respawn_location = self.location

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
        Handle level up effects.
        """
        # Increase max health by 10 per level
        old_max = self.db.max_health
        self.db.max_health = 100 + ((new_level - 1) * 10)
        health_increase = self.db.max_health - old_max
        
        # Restore to full health on level up
        self.db.health = self.db.max_health
        
        self.msg(f"|gYour maximum health increased by {health_increase}! (Now {self.db.max_health})|n")
        self.msg(f"|gYou have been restored to full health!|n")

    def take_damage(self, amount):
        """
        Take damage and handle death if health reaches 0.
        """
        self.ensure_stats_initialized()
        self.db.health = max(0, self.db.health - amount)
        
        if self.db.health <= 0:
            self.die()
            return True  # Died
        return False  # Still alive

    def heal(self, amount):
        """
        Restore health, capped at max_health.
        """
        self.ensure_stats_initialized()
        old_health = self.db.health
        self.db.health = min(self.db.max_health, self.db.health + amount)
        actual_heal = self.db.health - old_health
        
        if actual_heal > 0:
            self.msg(f"|gYou heal for {actual_heal} health! ({self.db.health}/{self.db.max_health})|n")

    def die(self):
        """
        Handle character death and respawn.
        """
        self.ensure_stats_initialized()
        self.msg("|rYou have died!|n")
        self.location.msg_contents(f"|r{self.key} has died!|n", exclude=self)
        
        # Move to respawn location
        respawn_loc = self.db.respawn_location
        if respawn_loc:
            self.move_to(respawn_loc, quiet=True)
        
        # Restore to full health
        self.db.health = self.db.max_health
        
        self.msg("|gYou have respawned with full health!|n")
        self.location.msg_contents(f"|g{self.key} has respawned!|n", exclude=self)

    def set_respawn_location(self, location):
        """
        Set the respawn location for this character.
        """
        self.db.respawn_location = location
        self.msg(f"Respawn location set to {location.key}.")

    def return_appearance(self, looker, **kwargs):
        """
        Display character appearance including stats.
        """
        appearance = super().return_appearance(looker, **kwargs)
        
        # Add stats display for self
        if looker == self:
            self.ensure_stats_initialized()
            stats = f"\n|wStats:|n\n"
            stats += f"  Health: |{'g' if self.db.health > 20 else 'r'}{self.db.health}|n/{self.db.max_health}\n"
            stats += f"  Level: {self.level}\n"
            stats += f"  Experience: {self.db.experience}\n"
            appearance += stats
            
        return appearance
