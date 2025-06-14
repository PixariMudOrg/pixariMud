"""

Lockfuncs

Lock functions are functions available when defining lock strings,
which in turn limits access to various game systems.

All functions defined globally in this module are assumed to be
available for use in lockstrings to determine access. See the
Evennia documentation for more info on locks.

A lock function is always called with two arguments, accessing_obj and
accessed_obj, followed by any number of arguments. All possible
arguments should be handled with *args, **kwargs. The lock function
should handle all eventual tracebacks by logging the error and
returning False.

Lock functions in this module extend (and will overload same-named)
lock functions from evennia.locks.lockfuncs.

"""

# def myfalse(accessing_obj, accessed_obj, *args, **kwargs):
#    """
#    called in lockstring with myfalse().
#    A simple logger that always returns false. Prints to stdout
#    for simplicity, should use utils.logger for real operation.
#    """
#    print "%s tried to access %s. Access denied." % (accessing_obj, accessed_obj)
#    return False


def holds_keycard(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Lock function to check if the accessing object holds a valid keycard
    for the vault door being accessed.
    
    Usage in lockstring: holds_keycard()
    
    This is more sophisticated than the basic holds() function as it
    checks keycard access levels and specific IDs.
    """
    # Check if accessed_obj is a VaultDoor
    if not hasattr(accessed_obj, 'db') or not hasattr(accessed_obj.db, 'required_access_level'):
        return False
        
    # Look for keycards in inventory
    keycards = [obj for obj in accessing_obj.contents 
               if obj.is_typeclass("typeclasses.objects.Keycard")]
    
    if not keycards:
        return False
        
    # Check each keycard
    access_hierarchy = ["standard", "security", "admin", "master"]
    
    for keycard in keycards:
        # Check specific ID if required
        if accessed_obj.db.required_keycard_id:
            if keycard.db.keycard_id == accessed_obj.db.required_keycard_id:
                return True
            continue
            
        # Check access level
        try:
            card_level = access_hierarchy.index(keycard.db.access_level)
            required_level = access_hierarchy.index(accessed_obj.db.required_access_level)
            
            if card_level >= required_level:
                return True
        except (ValueError, AttributeError):
            # Invalid access level or missing attributes
            continue
            
    return False
