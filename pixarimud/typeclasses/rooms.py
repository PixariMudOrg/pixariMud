"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom
from evennia import utils

from .objects import ObjectParent


class Room(ObjectParent, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See mygame/typeclasses/objects.py for a list of
    properties and methods available on all Objects.
    """

    def at_object_receive(self, arriving_obj, source_location, **kwargs):
        """
        Called when an object enters this room.
        Notifies all NPCs in the room about the new arrival.
        
        Args:
            arriving_obj (Object): The object arriving
            source_location (Object): Where the object came from
            **kwargs: Additional movement data
        """
        # First, call the parent method
        super().at_object_receive(arriving_obj, source_location, **kwargs)
        
        # Check if this is a character with an account (player)
        if hasattr(arriving_obj, 'account') and arriving_obj.account:
            # Notify all NPCs in the room
            for obj in self.contents:
                # Check if object is an NPC
                if (hasattr(obj, 'db') and obj.db.is_npc and 
                    hasattr(obj, 'at_char_entered')):
                    # Call the NPC's character entered hook
                    obj.at_char_entered(arriving_obj, **kwargs)
                    
    def at_object_leave(self, leaving_obj, destination, **kwargs):
        """
        Called when an object leaves this room.
        Notifies all NPCs in the room about the departure.
        
        Args:
            leaving_obj (Object): The object leaving
            destination (Object): Where the object is going
            **kwargs: Additional movement data
        """
        # First, call the parent method
        super().at_object_leave(leaving_obj, destination, **kwargs)
        
        # Check if this is a character with an account (player)
        if hasattr(leaving_obj, 'account') and leaving_obj.account:
            # Notify all NPCs in the room
            for obj in self.contents:
                # Check if object is an NPC
                if (hasattr(obj, 'db') and obj.db.is_npc and 
                    hasattr(obj, 'at_char_left')):
                    # Call the NPC's character left hook
                    obj.at_char_left(leaving_obj, **kwargs)
