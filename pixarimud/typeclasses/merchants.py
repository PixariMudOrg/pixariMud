"""
Merchant NPCs and shop system for pixariMud.
"""

from evennia import utils
from evennia.objects.objects import DefaultObject
from evennia.utils.evmenu import EvMenu


class NPCMerchant(DefaultObject):
    """
    An NPC merchant that can sell items to players.
    
    The merchant's inventory is stored as objects in their contents.
    Items for sale should have a 'gold_value' attribute set.
    """
    
    def at_object_creation(self):
        """Called when merchant is first created."""
        super().at_object_creation()
        self.db.shopname = "a humble shop"
        self.db.currency_name = "gold"
        # Add merchant command set
        self.cmdset.add_default(MerchantCmdSet, persistent=True)
        
    def open_shop(self, shopper):
        """
        Open the shop interface for a customer.
        
        Args:
            shopper: The character shopping
        """
        # Filter for items that are for sale (have a gold_value)
        wares = [item for item in self.contents if item.db.gold_value]
        
        if not wares:
            shopper.msg(f"{self.name} says: 'Sorry, I have nothing to sell right now.'")
            return
            
        # Start the shop menu
        EvMenu(
            shopper,
            {
                "shopfront": shopfront,
                "inspect_and_buy": inspect_and_buy,
                "sell_items": sell_items,
            },
            startnode="shopfront",
            shopname=self.db.shopname,
            shopkeeper=self,
            wares=wares,
        )
        
    def return_appearance(self, looker):
        """
        Format the merchant's appearance.
        """
        text = super().return_appearance(looker)
        
        # Show shop status
        if hasattr(self, 'contents'):
            wares = [item for item in self.contents if item.db.gold_value]
            if wares:
                text += f"\n{self.name} appears to be selling items. Use 'shop' to browse."
            else:
                text += f"\n{self.name} doesn't seem to have anything for sale."
                
        return text


# Menu node functions for the shop interface

def shopfront(caller, raw_string, **kwargs):
    """
    Main shop menu - display available items.
    """
    shopkeeper = kwargs.get("shopkeeper")
    shopname = kwargs.get("shopname", "Shop")
    wares = kwargs.get("wares", [])
    
    text = f"|c{shopname}|n\n"
    text += f"{shopkeeper.name} says: 'Welcome! Take a look at my wares.'\n\n"
    
    if not wares:
        text += "The shop appears to be empty."
    else:
        text += "|wAvailable items:|n\n"
        for i, item in enumerate(wares):
            price = item.db.gold_value or 0
            text += f"  {i+1}) {item.name} - {price} {shopkeeper.db.currency_name}\n"
    
    text += "\n|wYour gold:|n {}\n".format(caller.db.gold or 0)
    text += "\nEnter a number to inspect an item, 'sell' to sell items, or 'quit' to leave."
    
    options = []
    
    # Add numbered options for each item
    for i, item in enumerate(wares):
        options.append({
            "key": str(i+1),
            "desc": f"Inspect {item.name}",
            "goto": ("inspect_and_buy", {"selected_item": item}),
        })
    
    # Add sell option
    options.append({
        "key": "sell",
        "desc": "Sell your items",
        "goto": "sell_items",
    })
    
    # Add quit option
    options.append({
        "key": ("quit", "q", "exit"),
        "desc": "Leave the shop",
        "goto": "exit_shop",
    })
    
    return text, options


def inspect_and_buy(caller, raw_string, **kwargs):
    """
    Inspect a specific item and optionally buy it.
    """
    shopkeeper = kwargs.get("shopkeeper")
    selected_item = kwargs.get("selected_item")
    
    if not selected_item:
        return "shopfront"
    
    price = selected_item.db.gold_value or 0
    player_gold = caller.db.gold or 0
    
    text = f"|c{selected_item.name}|n\n"
    text += f"{selected_item.db.desc or 'No description available.'}\n\n"
    text += f"|wPrice:|n {price} {shopkeeper.db.currency_name}\n"
    text += f"|wYour gold:|n {player_gold}\n\n"
    
    options = []
    
    if player_gold >= price:
        options.append({
            "key": ("buy", "b"),
            "desc": f"Buy {selected_item.name}",
            "exec": lambda caller: buy_item(caller, shopkeeper, selected_item, price),
            "goto": "shopfront",
        })
    else:
        text += "|rYou don't have enough gold to buy this item.|n\n"
    
    options.append({
        "key": ("back", "return"),
        "desc": "Back to shop",
        "goto": "shopfront",
    })
    
    return text, options


def sell_items(caller, raw_string, **kwargs):
    """
    Menu for selling items to the merchant.
    """
    shopkeeper = kwargs.get("shopkeeper")
    
    # Get sellable items from player's inventory
    sellable = [item for item in caller.contents if item.db.gold_value and item.db.sellable != False]
    
    text = f"|cSell Items|n\n"
    
    if not sellable:
        text += "You don't have any items that can be sold.\n"
    else:
        text += "Items you can sell:\n"
        for i, item in enumerate(sellable):
            sell_price = int(item.db.gold_value * 0.5)  # Merchants buy at 50% value
            text += f"  {i+1}) {item.name} - {sell_price} {shopkeeper.db.currency_name}\n"
    
    text += f"\n|wYour gold:|n {caller.db.gold or 0}\n"
    text += "\nEnter a number to sell an item, or 'back' to return."
    
    options = []
    
    # Add numbered options for each sellable item
    for i, item in enumerate(sellable):
        sell_price = int(item.db.gold_value * 0.5)
        options.append({
            "key": str(i+1),
            "desc": f"Sell {item.name}",
            "exec": lambda caller, item=item, price=sell_price: sell_item(caller, shopkeeper, item, price),
            "goto": "sell_items",  # Stay in sell menu
        })
    
    options.append({
        "key": ("back", "return"),
        "desc": "Back to shop",
        "goto": "shopfront",
    })
    
    return text, options


def exit_shop(caller):
    """Exit the shop menu."""
    caller.msg("You leave the shop.")
    return None


# Helper functions for buying and selling

def buy_item(buyer, shopkeeper, item, price):
    """
    Handle the purchase transaction.
    """
    # Check gold again
    if (buyer.db.gold or 0) < price:
        buyer.msg("|rYou don't have enough gold!|n")
        return
    
    # Deduct gold
    buyer.db.gold = (buyer.db.gold or 0) - price
    
    # Move item to buyer
    item.move_to(buyer, quiet=True)
    
    # Add gold to shopkeeper
    shopkeeper.db.gold = (shopkeeper.db.gold or 0) + price
    
    buyer.msg(f"|gYou bought {item.name} for {price} gold.|n")
    

def sell_item(seller, shopkeeper, item, price):
    """
    Handle selling an item to the merchant.
    """
    # Move item to shopkeeper
    item.move_to(shopkeeper, quiet=True)
    
    # Add gold to seller
    seller.db.gold = (seller.db.gold or 0) + price
    
    # Deduct gold from shopkeeper (optional - unlimited gold)
    # shopkeeper.db.gold = (shopkeeper.db.gold or 0) - price
    
    seller.msg(f"|gYou sold {item.name} for {price} gold.|n")


# Command set for merchants

from evennia.commands.command import Command
from evennia.commands.cmdset import CmdSet


class CmdShop(Command):
    """
    Browse a merchant's wares.
    
    Usage:
        shop
        buy
        
    Open the shop interface when near a merchant.
    """
    
    key = "shop"
    aliases = ["buy", "browse"]
    
    def func(self):
        """Execute the command."""
        # Look for a merchant in the room
        merchants = [obj for obj in self.caller.location.contents 
                    if obj.typeclass_path == "typeclasses.merchants.NPCMerchant"]
        
        if not merchants:
            self.caller.msg("There is no merchant here.")
            return
            
        if len(merchants) > 1:
            self.caller.msg("There are multiple merchants here. Approaching the first one.")
            
        # Open shop with first merchant found
        merchants[0].open_shop(self.caller)


class MerchantCmdSet(CmdSet):
    """
    Command set for merchants - makes the shop command available
    when a merchant is in the room.
    """
    
    def at_cmdset_creation(self):
        """Add commands."""
        self.add(CmdShop)