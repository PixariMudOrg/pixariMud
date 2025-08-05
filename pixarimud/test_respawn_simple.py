#!/usr/bin/env python3
"""
Simple test to verify WornOutDummy respawn works correctly.
Run this from the Evennia shell: @py exec(open('test_respawn_simple.py').read())
"""

# Get the caller (player character)
caller = me

# Create a test room
from evennia import create_object
from typeclasses.rooms import Room
from typeclasses.objects import WornOutDummy

test_room = create_object(Room, key="Respawn Test Arena")
caller.msg("|gCreated test room: Respawn Test Arena|n")

# Move to the test room
caller.move_to(test_room)
caller.msg("|gMoved to test room|n")

# Create a worn-out dummy with fast respawn
dummy = create_object(WornOutDummy, key="Test Dummy", location=test_room)
dummy.db.respawn_timer = 5  # 5 seconds for quick testing
dummy.db.health = 5  # Low health for quick destruction
dummy.db.max_health = 5
caller.msg("|gCreated Test Dummy with 5 HP and 5 second respawn|n")

# Show initial state
caller.msg(f"|wDummy health: {dummy.db.health}/{dummy.db.max_health}|n")
caller.msg("|y>>> Hit the dummy 5 times to destroy it and trigger respawn|n")
caller.msg("|y>>> Use: hit dummy|n")