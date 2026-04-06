# TICKER_HANDLER Callback Fix

## Issue
The `WornOutDummy` respawn mechanism was failing with the error:
```
TypeError: WornOutDummy.respawn() got an unexpected keyword argument 'location'
```

## Root Cause
The TICKER_HANDLER in Evennia doesn't pass positional arguments to callbacks as keyword arguments. When we tried to pass the respawn location as a kwarg in the `add()` call, it wasn't being received properly by the callback method.

## Solution
Instead of passing the location as an argument to the ticker callback, we:

1. Store the respawn location in a temporary attribute on the object before scheduling the ticker
2. Modified the `respawn()` method to take no arguments and retrieve the location from the stored attribute
3. Clean up the temporary attribute after respawn

## Code Changes

### Before (Broken)
```python
# In die() method:
TICKER_HANDLER.add(
    interval=respawn_timer,
    callback=self.respawn,
    idstring=f"respawn_{self.id}",
    kwargs={"location": respawn_location}  # This doesn't work!
)

def respawn(self, location, **kwargs):
    # This signature expected kwargs but they weren't passed correctly
```

### After (Fixed)
```python
# In die() method:
# Store the respawn location for the callback
self.db.pending_respawn_location = respawn_location

TICKER_HANDLER.add(
    interval=respawn_timer,
    callback=self.respawn,
    idstring=f"respawn_{self.id}",
    persistent=False
)

def respawn(self):
    # Get the stored respawn location
    location = self.db.pending_respawn_location
    if not location:
        location = self.db.respawn_location
    # ... rest of respawn logic
    # Clean up
    self.db.pending_respawn_location = None
```

## Testing

To test the fix:

1. Reload the server: `evennia reload`
2. Create a worn-out dummy: `@create/drop Test Dummy:typeclasses.objects.WornOutDummy`
3. Set fast respawn for testing: `@py self.location.contents[-1].db.respawn_timer = 5`
4. Reduce health for quick test: `@py self.location.contents[-1].db.health = 5`
5. Hit the dummy 5 times: `hit dummy` (repeat 5x)
6. Wait for respawn message and verify the dummy reappears

## Alternative Approaches

Other ways to handle this in Evennia:

1. **Using Scripts**: Create a Script object for respawn instead of TICKER_HANDLER
2. **Using utils.delay**: For one-time delays, `evennia.utils.delay()` is simpler
3. **Storing in class attribute**: Use `self.ndb` for non-persistent storage instead of `self.db`

## Lessons Learned

- TICKER_HANDLER callbacks should generally not expect arguments
- Store any needed state on the object itself before scheduling the ticker
- Always check Evennia's documentation for the exact API of built-in systems
- Use `persistent=False` for temporary tickers that shouldn't survive server restarts