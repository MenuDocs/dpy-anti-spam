import redis

"""
This file will handle the class relating to redis

Every return statement will be a tuple layed out as follows:
(Status code, Actual value returned)
"""

class Redis:
    # Variable for tracking
    current_instance_count = 0

    def __init__(self, *, host='localhost', port=6379, db=0):
        """
        This init will set the relevant variables ready to connect later
        This will not connect now.

        Optional Params:
         - host (str) : The redis host to connect to
         - port (int) : The redis port to connect on
         - db (int) : The redis db to connect to
        """
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
         The key's value or 404
        """
        try:
            value = self.r.get(key)
            if value:
                return (200, value)
            return (404, "Key not found.")
        except Exception as e:
            return(500, e)


# Just some testing
r = Redis()
r.connect()
x = r.get_all_keys()[1]
print(x)
print(r.view_key(x[1]))
