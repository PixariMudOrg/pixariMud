"""
Shop items and equipment for pixariMud.
"""

from evennia.objects.objects import DefaultObject
from typeclasses.objects import ObjectParent


class ShopItem(ObjectParent):
    """
    Base class for items that can be bought and sold.
    """
    
    def at_object_creation(self):
        """Called when item is first created."""
        super().at_object_creation()
        self.db.gold_value = 10  # Default price
        self.db.sellable = True   # Can be sold back to merchants
        

class HealthPotion(ShopItem):
    """
    A potion that restores health when consumed.
    """
    
    def at_object_creation(self):
        """Set up the health potion."""
        super().at_object_creation()
        self.db.gold_value = 25
        self.db.heal_amount = 50
        self.db.desc = "A small red potion that glows with healing energy. Use 'drink potion' to consume it."
        
    def use(self, user):
        """
        Consume the potion and heal the user.
        """
        heal_amount = self.db.heal_amount or 50
        old_health = user.db.health
        user.heal(heal_amount)
        new_health = user.db.health
        
        actual_healed = new_health - old_health
        user.msg(f"|gYou drink the {self.name} and recover {actual_healed} health!|n")
        user.location.msg_contents(
            f"{user.name} drinks a {self.name}.",
            exclude=[user]
        )
        
        # Delete the potion after use
        self.delete()
        

class IronSword(ShopItem):
    """
    A basic weapon that increases damage dealt.
    """
    
    def at_object_creation(self):
        """Set up the iron sword."""
        super().at_object_creation()
        self.db.gold_value = 100
        self.db.damage_bonus = 5
        self.db.desc = "A well-crafted iron sword. When equipped, it increases your damage by 5."
        self.db.equipment_slot = "weapon"
        
        
class LeatherArmor(ShopItem):
    """
    Basic armor that reduces damage taken.
    """
    
    def at_object_creation(self):
        """Set up the leather armor."""
        super().at_object_creation()
        self.db.gold_value = 150
        self.db.defense_bonus = 3
        self.db.desc = "Sturdy leather armor. When equipped, it reduces damage taken by 3."
        self.db.equipment_slot = "armor"
        

class LuckyCharm(ShopItem):
    """
    An accessory that increases experience gained.
    """
    
    def at_object_creation(self):
        """Set up the lucky charm."""
        super().at_object_creation()
        self.db.gold_value = 200
        self.db.xp_bonus = 0.5  # 50% more XP
        self.db.desc = "A mysterious charm that brings good fortune. When equipped, you gain 50% more experience."
        self.db.equipment_slot = "accessory"
        

class TeleportScroll(ShopItem):
    """
    A consumable scroll that teleports the user to their respawn point.
    """
    
    def at_object_creation(self):
        """Set up the teleport scroll."""
        super().at_object_creation()
        self.db.gold_value = 50
        self.db.desc = "A magical scroll inscribed with teleportation runes. Use 'read scroll' to return to your respawn point."
        
    def use(self, user):
        """
        Teleport the user to their respawn location.
        """
        respawn_location = user.db.respawn_location or user.home
        
        if not respawn_location:
            user.msg("|rYou have no respawn point set!|n")
            return
            
        user.msg("|cThe scroll glows brightly as you read the ancient runes...|n")
        user.location.msg_contents(
            f"{user.name} vanishes in a flash of light!",
            exclude=[user]
        )
        
        # Move to respawn point
        user.move_to(respawn_location)
        user.location.msg_contents(
            f"{user.name} appears in a flash of light!",
            exclude=[user]
        )
        
        # Delete the scroll after use
        self.delete()