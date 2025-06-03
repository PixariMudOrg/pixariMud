"""
Object

The Object is the class for general items in the game world.

Use the ObjectParent class to implement common features for *all* entities
with a location in the game world (like Characters, Rooms, Exits).

"""

from evennia.objects.objects import DefaultObject
from evennia import TICKER_HANDLER


class ObjectParent:
    """
    This is a mixin that can be used to override *all* entities inheriting at
    some distance from DefaultObject (Objects, Exits, Characters and Rooms).

    Just add any method that exists on `DefaultObject` to this class. If one
    of the derived classes has itself defined that same hook already, that will
    take precedence.

    """


class Object(ObjectParent, DefaultObject):
    """
    This is the root Object typeclass, representing all entities that
    have an actual presence in-game. DefaultObjects generally have a
    location. They can also be manipulated and looked at. Game
    entities you define should inherit from DefaultObject at some distance.

    It is recommended to create children of this class using the
    `evennia.create_object()` function rather than to initialize the class
    directly - this will both set things up and efficiently save the object
    without `obj.save()` having to be called explicitly.

    Note: Check the autodocs for complete class members, this may not always
    be up-to date.

    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     date_created (string) - time stamp of object creation

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list, read only) - returns all objects inside this object
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser
     is_connected (bool, read-only) - True if this object is associated with
                            an Account with any connected sessions.
     has_account (bool, read-only) - True is this object has an associated account.
     is_superuser (bool, read-only): True if this object has an account and that
                        account is a superuser.

    * Handlers available

     aliases - alias-handler: use aliases.add/remove/get() to use.
     permissions - permission-handler: use permissions.add/remove() to
                   add/remove new perms.
     locks - lock-handler: use locks.add() to add new lock strings
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()
     attributes - attribute-handler. Use attributes.add/remove/get.
     db - attribute-handler: Shortcut for attribute-handler. Store/retrieve
            database attributes using self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
            a database entry when storing data

    * Helper methods (see src.objects.objects.py for full headers)

     get_search_query_replacement(searchdata, **kwargs)
     get_search_direct_match(searchdata, **kwargs)
     get_search_candidates(searchdata, **kwargs)
     get_search_result(searchdata, attribute_name=None, typeclass=None,
                       candidates=None, exact=False, use_dbref=None, tags=None, **kwargs)
     get_stacked_result(results, **kwargs)
     handle_search_results(searchdata, results, **kwargs)
     search(searchdata, global_search=False, use_nicks=True, typeclass=None,
            location=None, attribute_name=None, quiet=False, exact=False,
            candidates=None, use_locks=True, nofound_string=None,
            multimatch_string=None, use_dbref=None, tags=None, stacked=0)
     search_account(searchdata, quiet=False)
     execute_cmd(raw_string, session=None, **kwargs))
     msg(text=None, from_obj=None, session=None, options=None, **kwargs)
     for_contents(func, exclude=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, mapping=None,
                  raise_funcparse_errors=False, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     clear_contents()
     create(key, account, caller, method, **kwargs)
     copy(new_key=None)
     at_object_post_copy(new_obj, **kwargs)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False,
            no_superuser_bypass=False, **kwargs)
     filter_visible(obj_list, looker, **kwargs)
     get_default_lockstring()
     get_cmdsets(caller, current, **kwargs)
     check_permstring(permstring)
     get_cmdset_providers()
     get_display_name(looker=None, **kwargs)
     get_extra_display_name_info(looker=None, **kwargs)
     get_numbered_name(count, looker, **kwargs)
     get_display_header(looker, **kwargs)
     get_display_desc(looker, **kwargs)
     get_display_exits(looker, **kwargs)
     get_display_characters(looker, **kwargs)
     get_display_things(looker, **kwargs)
     get_display_footer(looker, **kwargs)
     format_appearance(appearance, looker, **kwargs)
     return_apperance(looker, **kwargs)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_first_save()
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.

     at_pre_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_post_move(source_location)          - always called after a move has
                        been successfully performed.
     at_pre_object_leave(leaving_object, destination, **kwargs)
     at_object_leave(obj, target_location, move_type="move", **kwargs)
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_pre_object_receive(obj, source_location)
     at_object_receive(obj, source_location, move_type="move", **kwargs) - called when this object receives
                        another object
     at_post_move(source_location, move_type="move", **kwargs)

     at_traverse(traversing_object, target_location, **kwargs) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_post_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_pre_get(getter, **kwargs)
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_pre_give(giver, getter, **kwargs)
     at_give(giver, getter, **kwargs)
     at_pre_drop(dropper, **kwargs)
     at_drop(dropper, **kwargs)          - called when this object has been dropped.
     at_pre_say(speaker, message, **kwargs)
     at_say(message, msg_self=None, msg_location=None, receivers=None, msg_receivers=None, **kwargs)

     at_look(target, **kwargs)
     at_desc(looker=None)

    """

    pass


class CombatDummy(Object):
    """
    A combat training dummy that can be hit for experience.
    Players can hit this dummy to gain 1 XP per hit.
    """

    def at_object_creation(self):
        """Set up the combat dummy."""
        super().at_object_creation()
        self.db.desc = "A sturdy combat training dummy. You can 'hit dummy' to practice combat and gain experience."
        self.db.hits_taken = 0
        
    def get_hit(self, attacker):
        """
        Handle being hit by a player.
        Awards 1 XP to the attacker.
        """
        if not hasattr(attacker, 'gain_experience'):
            attacker.msg("You can't gain experience!")
            return
            
        self.db.hits_taken += 1
        
        # Award experience
        attacker.gain_experience(1)
        
        # Dramatic combat messages
        attacker.msg(f"|yYou strike the {self.key} with force!|n")
        attacker.location.msg_contents(
            f"|y{attacker.key} strikes the {self.key}!|n", 
            exclude=attacker
        )
        
        # Show hit count occasionally
        if self.db.hits_taken % 10 == 0:
            attacker.location.msg_contents(
                f"|w{self.key} has taken {self.db.hits_taken} hits total.|n"
            )

    def return_appearance(self, looker, **kwargs):
        """Customize appearance to show hit count."""
        appearance = super().return_appearance(looker, **kwargs)
        if self.db.hits_taken > 0:
            appearance += f"\n|wThis dummy has been hit {self.db.hits_taken} times.|n"
        return appearance


class BottomlessPit(Object):
    """
    A dangerous pit that kills players who jump into it.
    Players respawn after jumping in.
    """

    def at_object_creation(self):
        """Set up the bottomless pit."""
        super().at_object_creation()
        self.db.desc = (
            "A dark, seemingly bottomless pit. The depths are shrouded in darkness. "
            "You can 'jump pit' or 'jump in pit' if you dare..."
        )
        self.db.victims = 0

    def jump_into(self, jumper):
        """
        Handle a player jumping into the pit.
        This kills the player, triggering respawn.
        """
        self.db.victims += 1
        
        # Dramatic death sequence
        jumper.msg("|rYou leap into the bottomless pit!|n")
        jumper.location.msg_contents(
            f"|r{jumper.key} leaps into the bottomless pit!|n", 
            exclude=jumper
        )
        
        jumper.msg("|rYou fall... and fall... and fall...|n")
        jumper.msg("|RThe darkness consumes you!|n")
        
        # Kill the player (triggers respawn via Character.die())
        jumper.db.health = 0
        jumper.die()
        
        # Update pit statistics
        if self.db.victims % 5 == 0:
            self.location.msg_contents(
                f"|w{self.key} has claimed {self.db.victims} victims.|n"
            )

    def return_appearance(self, looker, **kwargs):
        """Customize appearance to show victim count."""
        appearance = super().return_appearance(looker, **kwargs)
        if self.db.victims > 0:
            appearance += f"\n|rThis pit has claimed {self.db.victims} victims.|n"
        return appearance


class WornOutDummy(Object):
    """
    A combat dummy that can take damage and be destroyed.
    Has its own health pool and respawns after being destroyed.
    """

    def at_object_creation(self):
        """Set up the worn-out dummy."""
        super().at_object_creation()
        self.db.desc = (
            "An old, worn-out combat dummy that looks like it's seen better days. "
            "You can 'hit dummy' to attack it, but be careful - it might break!"
        )
        self.db.health = 100
        self.db.max_health = 100
        self.db.hits_given = 0
        self.db.respawn_location = self.location
        self.db.respawn_timer = 60  # seconds

    def get_hit(self, attacker):
        """
        Handle being hit by a player.
        Takes 1 damage, awards 1 XP to attacker.
        Dies when health reaches 0.
        """
        if not hasattr(attacker, 'gain_experience'):
            attacker.msg("You can't gain experience!")
            return
            
        # Take damage
        self.db.health -= 1
        self.db.hits_given += 1
        
        # Award experience
        attacker.gain_experience(1)
        
        # Combat messages
        attacker.msg(f"|yYou strike the {self.key}! It has {self.db.health} health left.|n")
        attacker.location.msg_contents(
            f"|y{attacker.key} strikes the {self.key}!|n", 
            exclude=attacker
        )
        
        # Check if dummy is destroyed
        if self.db.health <= 0:
            self.die(attacker)

    def die(self, killer=None):
        """
        Handle dummy destruction and setup respawn.
        """
        if killer:
            killer.msg(f"|rYou have destroyed the {self.key}!|n")
            killer.location.msg_contents(
                f"|r{killer.key} has destroyed the {self.key}!|n", 
                exclude=killer
            )
        
        self.location.msg_contents(
            f"|rThe {self.key} collapses into pieces!|n"
        )
        
        # Store respawn data
        respawn_location = self.db.respawn_location
        respawn_timer = self.db.respawn_timer
        
        # Remove from game temporarily
        self.move_to(None, quiet=True)
        
        # Schedule respawn
        TICKER_HANDLER.add(
            interval=respawn_timer,
            callback=self.respawn,
            idstring=f"respawn_{self.id}",
            kwargs={"location": respawn_location}
        )
        
        respawn_location.msg_contents(
            f"|gA new {self.key} will appear here in {respawn_timer} seconds.|n"
        )

    def respawn(self, location):
        """
        Respawn the dummy at the specified location.
        """
        # Reset stats
        self.db.health = self.db.max_health
        
        # Move back to the world
        self.move_to(location, quiet=True)
        
        # Announce respawn
        location.msg_contents(
            f"|gA new {self.key} has appeared!|n"
        )
        
        # Remove the ticker
        TICKER_HANDLER.remove(idstring=f"respawn_{self.id}")

    def return_appearance(self, looker, **kwargs):
        """Customize appearance to show health and stats."""
        appearance = super().return_appearance(looker, **kwargs)
        
        health_color = 'g' if self.db.health > 50 else 'y' if self.db.health > 20 else 'r'
        appearance += f"\n|wHealth:|n |{health_color}{self.db.health}|n/{self.db.max_health}"
        
        if self.db.hits_given > 0:
            appearance += f"\n|wHits Endured:|n {self.db.hits_given}"
            
        return appearance
