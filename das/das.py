from reddis_work import Redis

"""
Decided to redo the whole thing and base it on a class
so that this can be distributed as a package

Every public return statement should be a tuple layed out as follows:
(Status code, Actual value returned)
"""

class Das:
    # Anti Spam Class

    def __init__(self):
        # Init boi, currently gets nothing passed
        self.initialized = False # A check for usage checks
        self.guild_dict = {} # A dict for storing guild class instances

    def initialize(self):
        """
        Before being able to use the class instance, this
        needs to be called to setup all required class's etc
        """
        if self.is_initialized():
            return "This instance has already been initialized for usage"

        try:
            self.r = Redis(9000)
            self.r.connect()
            self.initialized = True
            return (200, "Initialization complete, Das is now ready for usage")
        except Exception as e:
            raise (500, e)

    def is_initialized(self):
        # Simply returns the state of initialization for this instance
        return self.initialized

    def create_guild(self, guildName, guildId, guildOwnerId):
        """
        A helper method to create and store a new
        guild class instance in our guilds dictionary

        Params:
         - guildName (Str) : The name of the guild
         - guildId (Int) : The guild id
         - guildOwnerId (Int) : The guild owners id
        """
        if not self.is_initialized():
            return (403, "Das instance has not be initialized yet")

        try:
            if self.guild_exists(int(guildId)):
                return (409, "Guild already exists")
            guild = Guild(guildName, guildId, guildOwnerId)
            self.guild_dict[guildId] = guild
            return (200, "New guild created")
        except Exception as e:
            return (500, e)

    def guild_exists(self, gid):
        """
        Simple check to see if a guild class already
        exists in our dictionary

        Params:
         - gid (int) : Guild id to check
        """
        if not self.is_initialized():
            return (403, "Das instance has not be initialized yet")

        return int(gid) in self.guild_dict

    def get_guild_instance(self, gid):
        """
        Returns the class instance for gid

        Params:
         - gid (int) : The user id to get
        """
        if not self.is_initialized():
            return (403, "Das instance has not be initialized yet")

        try:
            if not self.guild_exists(int(gid)):
                return (404, "Guild does not exist")
            return self.guild_dict[int(gid)]
        except Exception as e:
            return (500, e)

    def create_new_user_in_guild(self, *, guildId, userName, userId):
        """
        Used as an upper class method that will dive into the
        relevant class instances and create a new user for a guild

        Params:
         - guildId (int) : The guild to add the user to
         - userName (str) : The user's name
         - userId (int) : The user's Id
        """
        if not self.is_initialized():
            return (403, "Das instance has not be initialized yet")

        if not self.guild_exists(guildId):
            return (404, "Guild not found")
        g = self.get_guild_instance(guildId)

        if g.user_exists(userId):
            return (409, "User already exists")

        return g.create_new_user(userName, userId)

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
        self.guild_name = str(guildName)
        self.guild_id = int(guildId)
        self.guild_owner_id = int(guildOwnerId)

        self.user_dict = {}

    def user_exists(self, uid):
        """
        Simple check to see if a user class already
        exists in our dictionary

        Params:
         - uid (int) : User id to check
        """
        return int(uid) in self.user_dict

    def create_new_user(self, userName, userId):
        """
        A helper method to create and store a new
        user class instance in our guilds dictionary

        Params:
         - userName (Str) : The name of the user
         - userId (Int) : The users id
        """
        try:
            if self.user_exists(int(userId)):
                return (409, "User already exists")
            user = User(userName, userId)
            self.user_dict[userId] = user
            return (200, "New user created")
        except Exception as e:
            return (500, e)

    def get_user_info(self, uid):
        """
        Used to return a user's info

        Params:
         - userId (Int) : The users id
        """
        try:
            if not self.user_exists(int(uid)):
                return (404, "User does not exist to this guild")
            return self.user_dict[int(uid)].info()
        except Exception as e:
            return (500, e)

    def show_all_users(self):
        """
        Return the name and id of all user instances known
        to this guild
        """
        try:
            returnValue = {}
            for user in self.user_dict:
                info = self.get_user_info(user)
                if info[0] == 200:
                    returnValue[info[1]['id']] = info[1]['name']
            return (200, returnValue)
        except Exception as e:
            return (500, e)

    def get_user_instance(self, uid):
        """
        Returns the class instance for uid

        Params:
         - uid (int) : The user id to get
        """
        try:
            if not self.user_exists(int(uid)):
                return (404, "User does not exist to this guild")
            return self.user_dict[int(uid)]
        except Exception as e:
            return (500, e)

class User:
    # User class to store relevant things

    def __init__(self, userName, userId):
        """
        Init to setup class for usage

        Params:
         - userName (Str) : The name of the user
         - userId (Int) : The users id
        """
        self.name = str(userName) # Might change
        self.id = int(userId) # Should never change

    def set_name(self, name):
        """
        Change the users internal name

        Params:
         - name (str) = name
        """
        try:
            self.name = str(name)
            return (200, f"Changed instance user name to: {self.name}")
        except Exception as e:
            return (500, e)

    def info(self):
        """
        Returns the instances user info in a dictionary
        """
        return (200, {"name": self.name, "id": self.id})

das = Das()
print(das.initialize())

print(das.create_new_user_in_guild(guildId=12345, userName="test user", userId=1))
print(das.create_guild("Test Guild", 12345, 1))
print(das.create_new_user_in_guild(guildId=12345, userName="test user", userId=1))
print(das.create_new_user_in_guild(guildId=12345, userName="test user", userId=1))
