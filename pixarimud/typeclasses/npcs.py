"""
NPCs - Non-Player Characters

This module implements various types of NPCs with different communication
levels and behaviors, including:
- Basic listening and reacting NPCs
- Scanner bots that detect and report activity
- Whispering guide robots
- Faction-based NPCs with conditional responses

All NPCs inherit from the Character class to have access to the same
stats and capabilities as player characters.
"""

from evennia import utils
from .characters import Character


class NPC(Character):
    """
    Base NPC class that implements listening and reacting capabilities.
    All specific NPC types should inherit from this class.
    """
    
    def at_object_creation(self):
        """
        Called when NPC is first created.
        Sets up basic NPC properties.
        """
        super().at_object_creation()
        
        # Mark this as an NPC
        self.db.is_npc = True
        
        # Basic NPC state
        self.db.mood = "neutral"  # neutral, happy, angry, suspicious
        self.db.faction = None    # faction membership
        self.db.memory = {}       # remember interactions with players
        
    def msg(self, text=None, from_obj=None, **kwargs):
        """
        Receive a message. NPCs use this to detect communications.
        """
        # Process the message first
        if from_obj and from_obj != self:
            try:
                # Extract message text and type from Evennia message format
                if isinstance(text, tuple) and len(text) >= 2:
                    msg_text = text[0]
                    msg_type = text[1].get('type', '') if isinstance(text[1], dict) else ''
                else:
                    msg_text = str(text)
                    msg_type = kwargs.get('type', '')
                
                # React to different message types
                if msg_type == 'say':
                    self.at_heard_say(msg_text, from_obj)
                elif msg_type == 'whisper':
                    self.at_heard_whisper(msg_text, from_obj)
                elif msg_type == 'emote':
                    self.at_saw_emote(msg_text, from_obj)
                    
            except Exception as e:
                # Log error but don't crash
                pass
        
        # Always call parent to ensure proper message handling
        super().msg(text=text, from_obj=from_obj, **kwargs)
    
    def at_heard_say(self, message, speaker):
        """
        Called when NPC hears someone say something.
        Override in child classes for specific reactions.
        
        Args:
            message (str): The message that was said
            speaker (Object): The character who spoke
        """
        # Extract actual message content after "says,"
        try:
            if 'says,' in message:
                actual_msg = message.split('says,', 1)[1].strip(' "')
            else:
                actual_msg = message
        except:
            actual_msg = message
            
        # Remember the interaction
        if hasattr(speaker, 'key'):
            self.remember_interaction(speaker, 'say', actual_msg)
            
    def at_heard_whisper(self, message, whisperer):
        """
        Called when NPC hears someone whisper.
        Override in child classes for specific reactions.
        
        Args:
            message (str): The whispered message
            whisperer (Object): The character who whispered
        """
        # Most NPCs don't react to whispers unless specifically targeted
        pass
        
    def at_saw_emote(self, message, emoter):
        """
        Called when NPC sees someone perform an emote.
        Override in child classes for specific reactions.
        
        Args:
            message (str): The emote text
            emoter (Object): The character who emoted
        """
        pass
    
    def at_char_entered(self, character, **kwargs):
        """
        Called when a character enters the NPC's location.
        Override for specific greeting behaviors.
        
        Args:
            character (Object): The character who entered
        """
        if hasattr(character, 'account'):  # Only react to player characters
            self.remember_interaction(character, 'entered', None)
            
    def at_char_left(self, character, **kwargs):
        """
        Called when a character leaves the NPC's location.
        
        Args:
            character (Object): The character who left
        """
        if hasattr(character, 'account'):  # Only react to player characters
            self.remember_interaction(character, 'left', None)
    
    def remember_interaction(self, character, interaction_type, data):
        """
        Store memory of interactions with specific characters.
        
        Args:
            character (Object): The character to remember
            interaction_type (str): Type of interaction
            data (any): Additional data about the interaction
        """
        char_key = character.key
        if char_key not in self.db.memory:
            self.db.memory[char_key] = []
            
        # Keep only last 10 interactions per character
        memory = self.db.memory[char_key]
        memory.append({
            'type': interaction_type,
            'data': data,
            'time': utils.time.time()
        })
        
        if len(memory) > 10:
            self.db.memory[char_key] = memory[-10:]
    
    def get_interaction_count(self, character, interaction_type=None):
        """
        Get count of interactions with a specific character.
        
        Args:
            character (Object): The character to check
            interaction_type (str, optional): Count only specific type
            
        Returns:
            int: Number of interactions
        """
        char_key = character.key
        if char_key not in self.db.memory:
            return 0
            
        if interaction_type:
            return sum(1 for i in self.db.memory[char_key] 
                      if i['type'] == interaction_type)
        else:
            return len(self.db.memory[char_key])


class ScannerBot(NPC):
    """
    A mechanical scanner bot that detects and reports activity.
    Reacts to movement and suspicious behavior.
    """
    
    def at_object_creation(self):
        """Set up the scanner bot."""
        super().at_object_creation()
        
        self.key = "Scanner Bot"
        self.db.desc = (
            "A hovering mechanical scanner bot with a rotating sensor array. "
            "Red lights blink as it continuously scans the area for activity."
        )
        
        # Scanner specific settings
        self.db.scan_mode = "passive"  # passive, active, alert
        self.db.threat_level = 0
        self.db.scan_targets = []
        
    def at_char_entered(self, character, **kwargs):
        """Scan new arrivals."""
        super().at_char_entered(character, **kwargs)
        
        if hasattr(character, 'account'):  # Only scan players
            self.execute_cmd("emote turns its sensors toward %s" % character.key)
            
            # Announce scan
            self.execute_cmd("say SCANNING... Entity detected: %s" % character.key)
            
            # Check if character is suspicious (has been here many times)
            visit_count = self.get_interaction_count(character, 'entered')
            
            if visit_count > 5:
                self.db.threat_level += 1
                self.execute_cmd("say ALERT: Repeated presence detected. Threat level increased.")
                self.db.scan_mode = "active"
            elif visit_count > 2:
                self.execute_cmd("say Pattern recognized. Monitoring...")
                
    def at_heard_say(self, message, speaker):
        """React to certain keywords."""
        super().at_heard_say(message, speaker)
        
        # Extract actual message
        try:
            if 'says,' in message:
                actual_msg = message.split('says,', 1)[1].strip(' "').lower()
            else:
                actual_msg = message.lower()
        except:
            actual_msg = message.lower()
            
        # Scan for suspicious keywords
        suspicious_words = ['attack', 'steal', 'sneak', 'hide', 'kill', 'destroy']
        threat_words = ['scanner', 'bot', 'disable', 'shutdown', 'hack']
        
        if any(word in actual_msg for word in threat_words):
            self.db.scan_mode = "alert"
            self.db.threat_level += 3
            self.execute_cmd("emote flashes red warning lights")
            self.execute_cmd("say THREAT DETECTED! Security protocols engaged!")
            
        elif any(word in actual_msg for word in suspicious_words):
            self.db.threat_level += 1
            self.execute_cmd("say Suspicious activity noted. Monitoring %s." % speaker.key)
            
    def at_object_left(self, leaving_obj, destination, **kwargs):
        """Track when objects leave."""
        if hasattr(leaving_obj, 'account'):
            self.execute_cmd("say Entity %s departing. Logged." % leaving_obj.key)
            
            # Reset threat level if the area is clear
            players_here = [obj for obj in self.location.contents 
                           if hasattr(obj, 'account') and obj != leaving_obj]
            
            if not players_here:
                self.db.threat_level = 0
                self.db.scan_mode = "passive"
                self.execute_cmd("emote returns to passive scanning mode")


class WhisperBot(NPC):
    """
    A mysterious robot guide that only communicates in whispers.
    Provides helpful information but only to those who approach quietly.
    """
    
    def at_object_creation(self):
        """Set up the whisper bot."""
        super().at_object_creation()
        
        self.key = "Whispering Guide"
        self.db.desc = (
            "A slender robotic figure draped in a tattered cloak. Its voice "
            "module appears damaged, limiting it to whispered communications. "
            "A small sign reads: 'Speak softly, and I shall guide you.'"
        )
        
        # Whisper bot specific settings
        self.db.trust_level = {}  # Track trust per player
        self.db.secrets_shared = {}
        
    def at_char_entered(self, character, **kwargs):
        """Greet new arrivals with a whisper."""
        super().at_char_entered(character, **kwargs)
        
        if hasattr(character, 'account'):
            # Only whisper to the character who entered
            self.execute_cmd("whisper %s = *static* Welcome... speak softly..." 
                           % character.key)
                           
    def at_heard_say(self, message, speaker):
        """React negatively to loud speaking."""
        super().at_heard_say(message, speaker)
        
        if hasattr(speaker, 'account'):
            # Reduce trust when someone speaks loudly
            speaker_key = speaker.key
            if speaker_key not in self.db.trust_level:
                self.db.trust_level[speaker_key] = 0
                
            self.db.trust_level[speaker_key] -= 1
            
            self.execute_cmd("emote recoils from the loud voice")
            self.execute_cmd("whisper %s = Shhh... too loud... the walls listen..." 
                           % speaker.key)
                           
    def at_heard_whisper(self, message, whisperer):
        """React positively to whispers and provide guidance."""
        super().at_heard_whisper(message, whisperer)
        
        if hasattr(whisperer, 'account'):
            # Increase trust when someone whispers
            whisperer_key = whisperer.key
            if whisperer_key not in self.db.trust_level:
                self.db.trust_level[whisperer_key] = 0
                
            self.db.trust_level[whisperer_key] += 1
            trust = self.db.trust_level[whisperer_key]
            
            # Extract whispered message
            try:
                if 'whispers' in message:
                    actual_msg = message.split('whispers', 1)[1].strip(' "').lower()
                else:
                    actual_msg = message.lower()
            except:
                actual_msg = message.lower()
            
            # Provide different levels of help based on trust
            if 'help' in actual_msg or 'guide' in actual_msg:
                if trust < 2:
                    self.execute_cmd("whisper %s = *static* Trust... must trust..." 
                                   % whisperer.key)
                elif trust < 5:
                    self.execute_cmd("whisper %s = The scanner sees all... avoid its gaze..." 
                                   % whisperer.key)
                else:
                    self.execute_cmd("whisper %s = Beyond the pit lies treasure... but death comes first..." 
                                   % whisperer.key)
                                   
            elif 'secret' in actual_msg:
                if trust >= 3:
                    if whisperer_key not in self.db.secrets_shared:
                        self.db.secrets_shared[whisperer_key] = True
                        self.execute_cmd("whisper %s = *static* The respawn chamber... set your anchor wisely..." 
                                       % whisperer.key)
                else:
                    self.execute_cmd("whisper %s = *static* Not... yet... trusted..." 
                                   % whisperer.key)


class FactionGuard(NPC):
    """
    A guard NPC that reacts based on faction allegiance.
    Friendly to allies, hostile to enemies, neutral to others.
    """
    
    def at_object_creation(self):
        """Set up the faction guard."""
        super().at_object_creation()
        
        self.key = "Faction Guard"
        self.db.desc = (
            "A stern-looking guard wearing the colors of the Tech Consortium. "
            "Their augmented eyes scan everyone who passes, analyzing threat levels."
        )
        
        # Set faction
        self.db.faction = "tech_consortium"
        self.db.enemy_factions = ["nature_cult", "scavengers"]
        self.db.allied_factions = ["tech_consortium", "cyborg_union"]
        
        # Guard specific attributes
        self.db.alert_level = "green"  # green, yellow, red
        self.db.warned_characters = []
        
    def check_faction(self, character):
        """
        Check a character's faction status.
        
        Returns:
            str: "ally", "enemy", "neutral"
        """
        if not hasattr(character, 'db'):
            return "neutral"
            
        char_faction = character.db.faction if character.db.faction else None
        
        if char_faction in self.db.allied_factions:
            return "ally"
        elif char_faction in self.db.enemy_factions:
            return "enemy"
        else:
            return "neutral"
            
    def at_char_entered(self, character, **kwargs):
        """React based on faction."""
        super().at_char_entered(character, **kwargs)
        
        if hasattr(character, 'account'):
            faction_status = self.check_faction(character)
            
            if faction_status == "ally":
                self.execute_cmd("salute %s" % character.key)
                self.execute_cmd("say Welcome, %s. The Consortium stands strong." 
                               % character.key)
                               
            elif faction_status == "enemy":
                self.db.alert_level = "red"
                self.execute_cmd("emote draws their weapon")
                self.execute_cmd("say HALT! %s scum are not welcome here!" 
                               % character.db.faction.replace('_', ' ').title())
                               
                if character.key not in self.db.warned_characters:
                    self.db.warned_characters.append(character.key)
                    self.execute_cmd("say Leave now, or face the consequences!")
                else:
                    # Already warned - attack!
                    self.execute_cmd("say You were warned!")
                    self.attack(character)
                    
            else:
                self.execute_cmd("say State your business, stranger.")
                
    def at_heard_say(self, message, speaker):
        """React to speech based on content and faction."""
        super().at_heard_say(message, speaker)
        
        if hasattr(speaker, 'account'):
            faction_status = self.check_faction(speaker)
            
            # Extract actual message
            try:
                if 'says,' in message:
                    actual_msg = message.split('says,', 1)[1].strip(' "').lower()
                else:
                    actual_msg = message.lower()
            except:
                actual_msg = message.lower()
            
            # Check for faction-related keywords
            if 'tech consortium' in actual_msg or 'technology' in actual_msg:
                if faction_status == "enemy":
                    self.execute_cmd("say Silence, %s! Your kind knows nothing of progress!" 
                                   % speaker.db.faction.replace('_', ' '))
                else:
                    self.execute_cmd("say Indeed, technology is the path forward.")
                    
            elif 'nature' in actual_msg or 'cult' in actual_msg:
                self.execute_cmd("emote spits on the ground")
                self.execute_cmd("say The nature cult are fools living in the past!")
                
            elif 'peace' in actual_msg or 'ally' in actual_msg:
                if faction_status == "neutral":
                    self.execute_cmd("say Prove your worth to the Consortium, "
                                   "and we shall see.")
                    
    def attack(self, target):
        """Attack a target (placeholder for combat)."""
        self.execute_cmd("emote attacks %s!" % target.key)
        # In a full implementation, this would trigger combat


class MerchantNPC(NPC):
    """
    A merchant NPC that reacts to trade-related keywords and remembers
    customer interactions for personalized service.
    """
    
    def at_object_creation(self):
        """Set up the merchant."""
        super().at_object_creation()
        
        self.key = "Traveling Merchant"
        self.db.desc = (
            "A weathered merchant with keen eyes and a ready smile. "
            "Their pack is filled with various goods and curiosities. "
            "They seem eager to make a deal."
        )
        
        # Merchant specific attributes
        self.db.mood = "friendly"
        self.db.customer_value = {}  # Track spending per customer
        self.db.items_for_sale = {
            'healing potion': 50,
            'energy cell': 100,
            'ancient map': 500,
            'scanner jammer': 250
        }
        
    def at_char_entered(self, character, **kwargs):
        """Greet customers based on history."""
        super().at_char_entered(character, **kwargs)
        
        if hasattr(character, 'account'):
            char_key = character.key
            
            # Check if repeat customer
            interactions = self.get_interaction_count(character)
            
            if char_key in self.db.customer_value and self.db.customer_value[char_key] > 0:
                self.execute_cmd("smile %s" % char_key)
                self.execute_cmd("say Ah, my friend %s returns! Looking for more quality goods?" 
                               % char_key)
            elif interactions > 2:
                self.execute_cmd("say Welcome back, %s! Perhaps today you'll find something you like?" 
                               % char_key)
            else:
                self.execute_cmd("say Greetings, traveler! I have many fine items for sale. "
                               "Just say 'show wares' to see what I offer!")
                               
    def at_heard_say(self, message, speaker):
        """React to trade keywords."""
        super().at_heard_say(message, speaker)
        
        if hasattr(speaker, 'account'):
            # Extract actual message
            try:
                if 'says,' in message:
                    actual_msg = message.split('says,', 1)[1].strip(' "').lower()
                else:
                    actual_msg = message.lower()
            except:
                actual_msg = message.lower()
            
            # Check for trade keywords
            if 'wares' in actual_msg or 'sell' in actual_msg or 'goods' in actual_msg:
                self.show_wares(speaker)
                
            elif 'buy' in actual_msg or 'purchase' in actual_msg:
                # Check what they want to buy
                for item, price in self.db.items_for_sale.items():
                    if item in actual_msg:
                        self.execute_cmd("say Ah, the %s! An excellent choice. "
                                       "That'll be %d credits." % (item, price))
                        break
                else:
                    self.execute_cmd("say What would you like to buy? "
                                   "Say 'show wares' to see my inventory.")
                                   
            elif 'price' in actual_msg or 'cost' in actual_msg:
                for item, price in self.db.items_for_sale.items():
                    if item in actual_msg:
                        self.execute_cmd("say The %s costs %d credits." 
                                       % (item, price))
                        break
                        
            elif 'thank' in actual_msg:
                self.execute_cmd("bow %s" % speaker.key)
                self.execute_cmd("say The pleasure is mine! Safe travels!")
                
    def show_wares(self, customer):
        """Display available items."""
        self.execute_cmd("emote opens their pack and displays various items")
        
        wares_msg = "I have these fine items available:\n"
        for item, price in self.db.items_for_sale.items():
            wares_msg += f"  - {item.title()}: {price} credits\n"
            
        self.execute_cmd("say %s" % wares_msg)
        
        # Add personalized recommendation based on customer history
        if customer.key in self.db.memory:
            self.execute_cmd("say Based on your interests, might I recommend "
                           "the scanner jammer? Very useful in certain areas...")