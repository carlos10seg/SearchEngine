import redis

#r.set('foo', 'bar')
#print(r.get('foo'))

class RedisManager:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        
    def setValue(self, key, value):
        self.r.set(key, value)
    
    def getValue(self, key):
        return self.r.get(key)
    
    def appendValue(self, key, value):
        self.r.append(key, value)
    
    def save_many_in_index(self, index_structure):
        for i in range(len(index_structure.Terms)):
            term = index_structure.Terms[i]
            frequency = index_structure.Frequencies[i] + ','
            self.appendValue(term, frequency)
    
    def remove_all(self):
        self.r.flushdb()