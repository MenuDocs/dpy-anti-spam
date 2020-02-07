import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)

r.set('foo', 'bar', px=10000) #px being timeout in milliseconds

print(r.get('foo'))

time.sleep(15)

print(r.get('foo'))
