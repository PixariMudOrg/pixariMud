"""
Scrap heap and junkyard room types for pixariMud.

These rooms allow players to search for robot parts with cooldowns
and randomized discovery mechanics.
"""

from evennia.objects.objects import DefaultRoom
from evennia.commands.command import Command
from evennia.commands.cmdset import CmdSet
from evennia.utils.evtable import EvTable
from random import choice, randint
import time


class ScrapHeapRoom(DefaultRoom):
    """
    A room filled with robot parts and scrap that can be searched.
    
    Players can search the scrap heap to find random robot parts with
    a cooldown between searches. The room tracks what has been found
    and can be restocked over time.
    """
    
    def at_object_creation(self):
        """Initialize the scrap heap."""
        super().at_object_creation()
        
        # Room properties
        self.db.room_type = "scrap_heap"
        self.db.search_difficulty = 1.0  # Modifier for search success
        self.db.part_quality_modifier = 0  # Affects part quality chances
        
        # Search tracking
        self.db.total_searches = 0
        self.db.successful_searches = 0
        self.db.last_restock_time = time.time()
        
        # Part availability
        self.db.available_parts = self.generate_initial_parts()
        self.db.guaranteed_parts = []  # Parts that will definitely be found
        
        # Flavor elements
        self.db.scrap_materials = [
            "rusted metal sheets", "tangled wires", "broken servos",
            "cracked display panels", "burnt circuit boards", "hydraulic tubing",
            "shattered optics", "corroded battery packs", "bent chassis frames"
        ]
        
        # Add search command
        self.cmdset.add(ScrapHeapCmdSet, persistent=True)
        
    def generate_initial_parts(self):
        """Generate the starting pool of discoverable parts."""
        parts_pool = []
        
        # Ensure at least one of each critical part type
        for part_type in ["arm", "arm", "leg", "leg"]:
            parts_pool.append({
                "type": part_type,
                "quality": choice(["damaged", "standard"]),
                "weight": randint(5, 15),
                "found": False
            })
            
        # Add some random extras
        for _ in range(randint(3, 7)):
            parts_pool.append({
                "type": choice(["arm", "leg", "head", "torso"]),
                "quality": choice(["damaged", "damaged", "standard", "enhanced"]),
                "weight": randint(5, 20),
                "found": False
            })
            
        return parts_pool
        
    def restock_parts(self):
        """Add new parts to the heap over time."""
        current_time = time.time()
        hours_passed = (current_time - self.db.last_restock_time) / 3600
        
        if hours_passed >= 1:
            # Add new parts based on time passed
            new_parts = int(hours_passed)
            for _ in range(new_parts):
                self.db.available_parts.append({
                    "type": choice(["arm", "leg", "head", "torso"]),
                    "quality": choice(["damaged", "standard", "enhanced"]),
                    "weight": randint(5, 20),
                    "found": False
                })
                
            self.db.last_restock_time = current_time
            
    def search_heap(self, searcher):
        """
        Perform a search of the scrap heap.
        
        Args:
            searcher: Character doing the searching
            
        Returns:
            found_part: RobotPart object or None
            message: Description of the search
        """
        self.db.total_searches += 1
        
        # Check for restocking
        self.restock_parts()
        
        # Get unfound parts
        unfound_parts = [p for p in self.db.available_parts if not p["found"]]
        
        # Import here to avoid circular imports
        from typeclasses.robot_parts import generate_random_part
        
        # Check guaranteed parts first
        if self.db.guaranteed_parts:
            part_data = self.db.guaranteed_parts.pop(0)
            part = generate_random_part(
                part_type=part_data.get("type"),
                quality=part_data.get("quality")
            )
            self.db.successful_searches += 1
            return part, self.get_success_message(part)
            
        # Random chance to find nothing
        if not unfound_parts or randint(1, 100) > (70 * self.db.search_difficulty):
            return None, self.get_failure_message()
            
        # Find a random part
        part_data = choice(unfound_parts)
        part_data["found"] = True
        
        # Generate the actual part object
        part = generate_random_part(
            part_type=part_data["type"],
            quality=part_data["quality"]
        )
        
        # Apply room quality modifier
        if self.db.part_quality_modifier > 0 and randint(1, 100) <= self.db.part_quality_modifier * 10:
            # Upgrade quality by one tier
            quality_tiers = ["damaged", "standard", "enhanced", "pristine"]
            current_idx = quality_tiers.index(part.db.quality)
            if current_idx < len(quality_tiers) - 1:
                part.db.quality = quality_tiers[current_idx + 1]
                
        self.db.successful_searches += 1
        return part, self.get_success_message(part)
        
    def get_success_message(self, part):
        """Generate a flavorful success message."""
        messages = [
            f"Digging through {choice(self.db.scrap_materials)}, you uncover {part.get_display_name()}!",
            f"Your servos strain as you shift debris, revealing {part.get_display_name()}.",
            f"After careful searching, you extract {part.get_display_name()} from the heap.",
            f"Success! Buried beneath the scrap, you find {part.get_display_name()}.",
            f"Your sensors detect something useful - {part.get_display_name()}!"
        ]
        return choice(messages)
        
    def get_failure_message(self):
        """Generate a flavorful failure message."""
        messages = [
            f"You search through {choice(self.db.scrap_materials)} but find nothing useful.",
            "Despite your efforts, this section of the heap yields only worthless junk.",
            "Your search turns up nothing but corroded components and scrap metal.",
            "You dig for a while but come up empty-handed.",
            f"All you find is {choice(self.db.scrap_materials)} - nothing salvageable."
        ]
        return choice(messages)
        
    def return_appearance(self, looker, **kwargs):
        """Custom appearance for scrap heap rooms."""
        string = super().return_appearance(looker, **kwargs)
        
        # Add search statistics
        string += f"\n\n|wScrap Heap Status:|n"
        unfound_count = len([p for p in self.db.available_parts if not p["found"]])
        
        if unfound_count > 10:
            string += "\nThe heap looks largely untouched, with plenty to search through."
        elif unfound_count > 5:
            string += "\nThe heap has been picked over but still has promising areas."
        elif unfound_count > 0:
            string += "\nMost of the good spots have been searched already."
        else:
            string += "\nThe heap has been thoroughly ransacked."
            
        # Add hint about searching
        if hasattr(looker.db, "attached_parts"):
            missing_parts = [slot for slot, part in looker.db.attached_parts.items() if not part]
            if missing_parts:
                string += f"\n\n|yYou still need: {', '.join(missing_parts)}|n"
                string += "\n|wHint: Use 'search' to look for parts.|n"
                
        return string


class StartingScrapHeap(ScrapHeapRoom):
    """
    Special scrap heap for the starting area.
    
    Guarantees the player will find the minimum parts needed to
    progress (both legs and one arm) within reasonable searches.
    """
    
    def at_object_creation(self):
        super().at_object_creation()
        
        # Ensure starting parts are available
        self.db.guaranteed_parts = [
            {"type": "leg", "quality": "damaged"},
            {"type": "leg", "quality": "damaged"},
            {"type": "arm", "quality": "standard"}
        ]
        
        # Better quality chances for starting area
        self.db.part_quality_modifier = 2
        
        # Tutorial hints
        self.db.has_shown_search_hint = False
        self.db.has_shown_attach_hint = False
        
    def at_object_receive(self, moved_obj, source_location, **kwargs):
        """Called when someone enters the room."""
        super().at_object_receive(moved_obj, source_location, **kwargs)
        
        # Show tutorial hints for new robots
        if hasattr(moved_obj, "db") and hasattr(moved_obj.db, "is_robot"):
            if not self.db.has_shown_search_hint:
                moved_obj.msg("\n|y[Tutorial]|n You can 'search' the scrap heap for robot parts.")
                moved_obj.msg("There's a cooldown between searches, so be patient!")
                self.db.has_shown_search_hint = True


# Commands for scrap heap rooms

class CmdSearch(Command):
    """
    Search through the scrap heap for useful parts.
    
    Usage:
        search
        scavenge
        
    Searches take time and you must wait between attempts. The quality
    and type of parts you find is somewhat random, but critical parts
    are guaranteed to appear eventually.
    """
    
    key = "rummage"
    aliases = ["scavenge", "dig", "forage"]
    
    # Search cooldown in seconds
    cooldown_duration = 20
    
    def func(self):
        # Check if we're in a scrap heap
        if not hasattr(self.caller.location.db, "room_type") or \
           self.caller.location.db.room_type != "scrap_heap":
            self.caller.msg("There's nothing to search here.")
            return
            
        # Check cooldown
        now = time.time()
        last_search = self.caller.db.last_search_time or 0
        
        if now - last_search < self.cooldown_duration:
            remaining = int(self.cooldown_duration - (now - last_search))
            self.caller.msg(f"You're still tired from searching. Wait {remaining} more seconds.")
            
            # Show progress bar
            progress = int(((now - last_search) / self.cooldown_duration) * 10)
            bar = "█" * progress + "░" * (10 - progress)
            self.caller.msg(f"Cooldown: [{bar}]")
            return
            
        # Update cooldown
        self.caller.db.last_search_time = now
        
        # Perform the search
        self.caller.msg("You begin searching through the scrap heap...")
        
        # Small delay for atmosphere
        yield 2
        
        # Get search result
        part, message = self.caller.location.search_heap(self.caller)
        self.caller.msg(message)
        
        if part:
            # Place the part in the room
            part.location = self.caller.location
            self.caller.location.msg_contents(
                f"{self.caller.key} pulls {part.get_display_name()} from the scrap heap!",
                exclude=[self.caller]
            )
            
            # Tutorial hint for attaching
            if hasattr(self.caller.location.db, "has_shown_attach_hint") and \
               not self.caller.location.db.has_shown_attach_hint:
                if hasattr(self.caller.db, "attached_parts"):
                    missing = [s for s, p in self.caller.db.attached_parts.items() if not p]
                    if missing and part.db.part_slot in missing:
                        self.caller.msg(f"\n|y[Tutorial]|n Use 'get {part.key}' then 'attach {part.key}' to install it!")
                        self.caller.location.db.has_shown_attach_hint = True


class CmdHeapStatus(Command):
    """
    Check the status of the scrap heap.
    
    Usage:
        heapstatus
        heap
        
    Shows information about the scrap heap's condition and your
    search history in this location.
    """
    
    key = "heapstatus"
    aliases = ["heap", "scrapstatus"]
    
    def func(self):
        # Check if we're in a scrap heap
        if not hasattr(self.caller.location.db, "room_type") or \
           self.caller.location.db.room_type != "scrap_heap":
            self.caller.msg("This isn't a scrap heap.")
            return
            
        room = self.caller.location
        
        # Display heap information
        self.caller.msg("|w=== Scrap Heap Analysis ===|n")
        
        # Parts remaining
        unfound = len([p for p in room.db.available_parts if not p["found"]])
        total = len(room.db.available_parts)
        percent_searched = int(((total - unfound) / total * 100) if total > 0 else 100)
        
        self.caller.msg(f"|wSearched:|n {percent_searched}% of accessible areas")
        self.caller.msg(f"|wDetectable items:|n {'Many' if unfound > 10 else 'Some' if unfound > 5 else 'Few' if unfound > 0 else 'None'}")
        
        # Search statistics
        success_rate = int((room.db.successful_searches / room.db.total_searches * 100) 
                          if room.db.total_searches > 0 else 0)
        self.caller.msg(f"|wSearch success rate:|n {success_rate}%")
        
        # Personal search history
        if hasattr(self.caller.db, "search_count"):
            self.caller.msg(f"\n|wYour searches here:|n {self.caller.db.search_count}")
            
        # Cooldown status
        if hasattr(self.caller.db, "last_search_time"):
            elapsed = time.time() - self.caller.db.last_search_time
            if elapsed < CmdSearch.cooldown_duration:
                remaining = int(CmdSearch.cooldown_duration - elapsed)
                self.caller.msg(f"|wSearch cooldown:|n {remaining} seconds remaining")
            else:
                self.caller.msg("|wSearch cooldown:|n Ready to search!")


class ScrapHeapCmdSet(CmdSet):
    """Commands available in scrap heap rooms."""
    
    def at_cmdset_creation(self):
        self.add(CmdSearch())
        self.add(CmdHeapStatus())