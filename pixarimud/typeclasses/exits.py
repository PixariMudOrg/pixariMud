"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""

from evennia.objects.objects import DefaultExit

from .objects import ObjectParent


class Exit(ObjectParent, DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property and overrides some hooks
    and methods to represent the exits.

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects child classes like this.

    """

    pass


class VaultDoor(Exit):
    """
    A secure vault door that requires a keycard to traverse.
    Can be configured to require specific keycard types or IDs.
    """
    
    def at_object_creation(self):
        """Set up the vault door with proper locks and messages."""
        super().at_object_creation()
        
        # Default description
        self.db.desc = "A heavy reinforced vault door with an electronic card reader."
        
        # Security settings
        self.db.required_access_level = "security"  # Minimum access level needed
        self.db.required_keycard_id = None  # Specific ID if needed
        self.db.door_name = "vault door"  # For messages
        
        # Set the lock - uses our custom keycard validation
        self.locks.add("traverse: holds_keycard() or perm(Builder)")
        
        # Custom error message
        self.db.err_traverse = (
            "|rAccess Denied.|n The {door_name}'s card reader flashes red. "
            "You need a valid keycard to open this door."
        )
        
    def at_failed_traverse(self, traversing_object):
        """
        Called when someone tries to go through but fails the lock.
        We'll provide more detailed feedback based on what they're carrying.
        """
        # Check if they have any keycard at all
        keycards = [obj for obj in traversing_object.contents 
                   if obj.is_typeclass("typeclasses.objects.Keycard")]
        
        if not keycards:
            # Use the default error message
            traversing_object.msg(
                self.db.err_traverse.format(door_name=self.db.door_name)
            )
        else:
            # They have a keycard, but it's not the right one
            keycard = keycards[0]  # Check the first one they're carrying
            
            if self.db.required_keycard_id:
                # Specific ID required
                if keycard.db.keycard_id != self.db.required_keycard_id:
                    traversing_object.msg(
                        f"|rAccess Denied.|n The {self.db.door_name}'s reader scans your "
                        f"{keycard.key} but rejects it. This door requires keycard ID: "
                        f"{self.db.required_keycard_id}."
                    )
                else:
                    # Right ID but wrong access level?
                    traversing_object.msg(
                        f"|rAccess Denied.|n Your {keycard.key} has insufficient "
                        f"access level for this {self.db.door_name}."
                    )
            else:
                # Access level check
                access_hierarchy = ["standard", "security", "admin", "master"]
                
                try:
                    card_level = access_hierarchy.index(keycard.db.access_level)
                    required_level = access_hierarchy.index(self.db.required_access_level)
                    
                    if card_level < required_level:
                        traversing_object.msg(
                            f"|rAccess Denied.|n The {self.db.door_name} requires "
                            f"|y{self.db.required_access_level}|n access or higher. "
                            f"Your {keycard.key} only has |w{keycard.db.access_level}|n access."
                        )
                    else:
                        # This shouldn't happen if locks are set correctly
                        traversing_object.msg(
                            f"|rAccess Denied.|n The {self.db.door_name} is malfunctioning."
                        )
                except ValueError:
                    traversing_object.msg(
                        f"|rSystem Error.|n Invalid access level configuration."
                    )
                    
    def check_traverse_access(self, traverser):
        """
        Custom access check for more sophisticated keycard validation.
        This is called by the lock system.
        """
        # First check if they're a builder (bypass)
        if traverser.check_permstring("Builder"):
            return True
            
        # Look for keycards in inventory
        keycards = [obj for obj in traverser.contents 
                   if obj.is_typeclass("typeclasses.objects.Keycard")]
        
        if not keycards:
            return False
            
        # Check each keycard
        access_hierarchy = ["standard", "security", "admin", "master"]
        
        for keycard in keycards:
            # Check specific ID if required
            if self.db.required_keycard_id:
                if keycard.db.keycard_id == self.db.required_keycard_id:
                    return True
                continue
                
            # Check access level
            try:
                card_level = access_hierarchy.index(keycard.db.access_level)
                required_level = access_hierarchy.index(self.db.required_access_level)
                
                if card_level >= required_level:
                    return True
            except ValueError:
                # Invalid access level
                continue
                
        return False
        
    def at_traverse(self, traversing_object, target_location):
        """
        Override to add special effects when successfully traversing.
        """
        # Find which keycard was used
        keycards = [obj for obj in traversing_object.contents 
                   if obj.is_typeclass("typeclasses.objects.Keycard")]
        
        if keycards and not traversing_object.check_permstring("Builder"):
            keycard = keycards[0]
            traversing_object.msg(
                f"|gAccess Granted.|n The {self.db.door_name}'s reader accepts your "
                f"{keycard.key} with a satisfying beep."
            )
            traversing_object.location.msg_contents(
                f"{traversing_object.key} swipes a keycard and the {self.db.door_name} opens.",
                exclude=traversing_object
            )
            
        # Continue with normal traversal
        super().at_traverse(traversing_object, target_location)
