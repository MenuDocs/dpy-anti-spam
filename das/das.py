import reddis_work

"""
Decided to redo the whole thing and base it on a class
so that this can be distributed as a package
"""

class Das:
    # Anti Spam Class

    def __init__(self):
        # Init boi, currently gets nothing passed
        self.initialized = False

    def initialize(self):
        """
        Before being able to use the class instance, this
        needs to be called to setup all required class's etc
        """
        if not self.initialized:
            return "This instance has already been initialized for usage"

        # Do stuff here

class Guild:
    # Guild class to hold relevant users

    def __init__(self, guildName, guildId, guildOwnerId):
        """
        Init to setup class for usage

        Params:
         - guildName (Str) : The name of the guild
         - guildId (Int) : The guilds id
         - guildOwnerId (Int) : The guild owners id
        """
        self.guild_name = guildName
        self.guild_id = guildId
        self.guild_owner_id = guildOwnerId

class User:
    # User class to store relevant things

    def __init__(self, userName, userId):
        """
        Init to setup class for usage

        Params:
         - userName (Str) : The name of the user
         - userId (Int) : The users id
        """
        self.name = userName
        self.id = userId
