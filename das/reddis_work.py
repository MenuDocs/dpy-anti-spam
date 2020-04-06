import redis
import pickle

"""
This file will handle the class relating to redis

Every return statement will be a tuple layed out as follows:
(Status code, Actual value returned)
"""

class Redis:
    # Variable for tracking
    current_instance_count = 0

    def __init__(self, autoDeletionPeriodMS, *, host='localhost', port=6379, db=0):
        """
        This init will set the relevant variables ready to connect later
        This will not connect now.

        Params:
         - autoDeletionPeriodMS (int) : Time in milliseconds to auto delete keys after
        Optional Params:
         - host (str) : The redis host to connect to
         - port (int) : The redis port to connect on
         - db (int) : The redis db to connect to
        """
        self.auto_deleteion_period_ms = autoDeletionPeriodMS
        self.host = host
        self.port = port
        self.db = db
        self.r = None
        Redis.add_instance_count()

    # Class methods
    @classmethod
    def number_of_instances(cls):
        # Returns the current instance count
        return cls.current_instance_count

    @classmethod
    def add_instance_count(cls):
        # Increments current class instance count
        cls.current_instance_count += 1

    # Functions
    def connect(self):
        """
        Connects to a redis instance
        Returns a tuple response with an http response code and message
        """
        try:
            self.r = redis.Redis(host=self.host, port=self.port, db=self.db)
            return (201, "Connection successful")
        except Exception as e:
            return (500, e)

    def get_all_keys(self):
        """
        Query all current keys and return a list of all keys

        Returns:
         All current keys
        """
        try:
            current_keys = self.r.keys()
            return (200, current_keys)
        except Exception as e:
            return(500, e)

    def view_key(self, key):
        """
        Checks to see if a key is in storage and then returns the relevant
        information depending on what it finds

        Params:
         - key (str) : The key to attempt to get

        Returns:
         The key's value or 404.
         500 if an error occurs
        """
        try:
            value = self.r.get(key)
            if value:
                return (200, value)
            return (404, "Key not found")
        except Exception as e:
            return(500, e)


    def set(self, key, value):
        """
        Used to set a key to a value in cache

        Params:
         - key () : The key to store value under
         - value () : What to store where

        Returns:
         200 for success.
         500 if an error occurs
        """
        try:
            self.r.set(key, value, px=self.auto_deleteion_period_ms)
            return (200, f"Set {key} to: {value}")
        except Exception as e:
            return(500, e)

    def get(self, key):
        """
        Since redis works with a like get-set mindset i thought id
        add the functionallity for it here by pointing this to view_key
        """
        return self.view_key(key)

    def getset(self, key, value):
        """
        Essentially both the get and set functions in one function. Some logic required
        to check whether or not something exists so this will return tuples within
        tuples with the format ((get, set), (get, set))

        Also, we cannot use the built in reddis getset() method due to not being able
        to set the px timeout, so two calls are used

        Params:
         - key () : The key to store value under / and check for item existing
         - value () : What to store where

        Returns:
         the item it found
         200 for success.
         500 if an error occurs
        """
        try:
            getResult = self.get(key)
            setResult = self.set(key, value)
            return ((getResult[0], setResult[0]), (getResult[1], setResult[1]))
        except Exception as e:
            return ((500, 500), (e, e))

    def delete_key(self, key):
        """
        Used to remove a singular key from cache

        Params:
         - key () : The key to delete

        Returns:
         Status codes depending on outcome
        """
        try:
            check = self.r.delete(key)
            if check:
                return (200, "Key deleted")
            return (404, "Key not found")
        except Exception as e:
            return(500, e)

    def delete(self, key):
        """
        Assuming simple naming means this exists as a pointer to the
        function delete_key
        """
        return self.delete_key(key)

    def get_object(self, key):
        """
        This is essentially the get() method however it provides
        added support for storing python class's/objects

        Params:
         - key () : The key to get

        Returns:
         The python object if found, plus a status code
        """
        try:
            check = self.get(key)
            if check[0] == 200:
                return (200, pickle.loads(check[1]))
            return (404, "Key not found")
        except Exception as e:
            return(500, e)

    def set_object(self, key, value):
        """
        This is essentially the get() method however it provides
        added support for storing python class's/objects

        Params:
         - key () : The key to set
         - value (Class/Object) : The value to store in cache

        Returns:
         A status code
        """
        try:
            check = self.set(key, pickle.dumps(value))
            return check
            if check:
                return (200, f"Set {key} to: {value}")
            return (404, "Key not found")
        except Exception as e:
            return(500, e)

    def getset_object(self, key, value):
        """
        Essentially both the get and set functions in one function. Some logic required
        to check whether or not something exists so this will return tuples within
        tuples with the format ((get, set), (get, set))

        This getset method supports storing of python class's/objects

        Also, we cannot use the built in reddis getset() method due to not being able
        to set the px timeout, so two calls are used

        Params:
         - key () : The key to store value under / and check for item existing
         - value () : What to store where

        Returns:
         the item it found
         200 for success.
         500 if an error occurs
        """
        try:
            getResult = self.get_object(key)
            setResult = self.set_object(key, value)
            return ((getResult[0], setResult[0]), (getResult[1], setResult[1]))
        except Exception as e:
            return ((500, 500), (e, e))
