"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia.commands.command import Command as BaseCommand

# from evennia import default_cmds


class Command(BaseCommand):
    """
    Base command (you may see this if a child command had no help text defined)

    Note that the class's `__doc__` string is used by Evennia to create the
    automatic help entry for the command, so make sure to document consistently
    here. Without setting one, the parent's docstring will show (like now).

    """

    # Each Command class implements the following methods, called in this order
    # (only func() is actually required):
    #
    #     - at_pre_cmd(): If this returns anything truthy, execution is aborted.
    #     - parse(): Should perform any extra parsing needed on self.args
    #         and store the result on self.
    #     - func(): Performs the actual work.
    #     - at_post_cmd(): Extra actions, often things done after
    #         every command, like prompts.
    #
    pass


class CmdHit(Command):
    """
    Hit a target to deal damage or train combat.
    
    Usage:
        hit <target>
        
    Attack a combat dummy to gain experience, or hit other targets
    for combat practice.
    """
    
    key = "hit"
    aliases = ["attack", "strike"]
    help_category = "Combat"

    def func(self):
        """Execute the hit command."""
        if not self.args:
            self.caller.msg("Hit what?")
            return
            
        target = self.caller.search(self.args)
        if not target:
            return
            
        # Check if target is in the same location
        if target.location != self.caller.location:
            self.caller.msg("You don't see that here.")
            return
            
        # Check if target has a hit method (for special objects)
        if hasattr(target, 'get_hit'):
            target.get_hit(self.caller)
        else:
            self.caller.msg(f"You can't hit {target.key}.")


class CmdJump(Command):
    """
    Jump into something.
    
    Usage:
        jump <target>
        jump in <target>
        
    Jump into dangerous places like bottomless pits.
    Use with caution!
    """
    
    key = "jump"
    aliases = ["leap"]
    help_category = "Movement"

    def func(self):
        """Execute the jump command."""
        if not self.args:
            self.caller.msg("Jump where?")
            return
            
        # Handle "jump in pit" or "jump pit"
        args = self.args.strip()
        if args.startswith("in "):
            args = args[3:]
            
        target = self.caller.search(args)
        if not target:
            return
            
        # Check if target is in the same location
        if target.location != self.caller.location:
            self.caller.msg("You don't see that here.")
            return
            
        # Check if target has a jump_into method (for special objects)
        if hasattr(target, 'jump_into'):
            target.jump_into(self.caller)
        else:
            self.caller.msg(f"You can't jump into {target.key}.")


class CmdStats(Command):
    """
    Display your character statistics.
    
    Usage:
        stats
        
    Shows your current health, level, experience, and other
    character information.
    """
    
    key = "stats"
    aliases = ["score", "status"]
    help_category = "General"

    def func(self):
        """Display character stats."""
        char = self.caller
        
        stats_display = f"""
|w=== Character Statistics ===|n
|wName:|n {char.key}
|wLevel:|n {char.level}
|wHealth:|n |{'g' if char.db.health > 20 else 'r'}{char.db.health}|n / {char.db.max_health}
|wExperience:|n {char.db.experience}
|wNext Level:|n {((char.level * 100) - char.db.experience)} XP needed
"""
        
        char.msg(stats_display)


class CmdSetRespawn(Command):
    """
    Set your respawn location.
    
    Usage:
        setrespawn
        
    Sets your current location as your respawn point.
    When you die, you will return here.
    """
    
    key = "setrespawn"
    aliases = ["respawn"]
    help_category = "General"

    def func(self):
        """Set respawn location."""
        char = self.caller
        char.set_respawn_location(char.location)


class CmdHeal(Command):
    """
    Heal yourself (for testing purposes).
    
    Usage:
        heal [amount]
        
    Restore your health. If no amount is specified,
    heal to full health.
    """
    
    key = "heal"
    help_category = "Combat"

    def func(self):
        """Heal the character."""
        char = self.caller
        
        if self.args:
            try:
                amount = int(self.args)
                char.heal(amount)
            except ValueError:
                char.msg("Heal amount must be a number.")
        else:
            # Full heal
            old_health = char.db.health
            char.db.health = char.db.max_health
            heal_amount = char.db.health - old_health
            if heal_amount > 0:
                char.msg(f"|gYou heal for {heal_amount} health! ({char.db.health}/{char.db.max_health})|n")
            else:
                char.msg("You are already at full health.")


class CmdSuicide(Command):
    """
    Kill your character (for testing death mechanics).
    
    Usage:
        suicide
        
    This will immediately kill your character to test
    the death and respawn system.
    """
    
    key = "suicide"
    help_category = "Combat"

    def func(self):
        """Kill the character."""
        char = self.caller
        char.msg("|rYou take your own life...|n")
        char.db.health = 0
        char.die()


# -------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super().has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None
