import redis

class RedisManager:
    # collections: inverted_index | collection_documents
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        self.inverted_index = '__inv_index__'
        self.collection_documents = '__col_docs__'
        self.max_freq_doc = '__max_freq_doc__'
        
    def setValue(self, key, value):
        self.r.set(key, value)
    
    def getValue(self, key):
        return self.r.get(key)
    
    def appendValue(self, key, value):
        self.r.append(key, value)

    def getValueFromHashSet(self, collection, key):
        return self.r.hget(collection, key)

    def setValueInHashSet(self, collection, key, value):
        self.r.hset(collection, key, value)
    
    def setValuesInHashSet(self, collection, valuesDictionary):
        self.r.hmset(collection, valuesDictionary)
    
    def save_many_in_index(self, index_structures):
        for index_structure in index_structures:
            self.setValueInHashSet(self.max_freq_doc, index_structure.doc_id, index_structure.get_max_freq())
            for i in range(len(index_structure.Terms)):
                term = index_structure.Terms[i]
                frequency = index_structure.Frequencies[i] + ','
                self.appendValue(term, frequency)
    
    def save_array_many_in_index(self, index_structures):
        dict_to_save = {}
        for index_structure in index_structures:
            for i in range(len(index_structure.Terms)):                
                term = index_structure.Terms[i]
                frequency = index_structure.Frequencies[i] + ','
                if term in dict_to_save:
                    dict_to_save[term] += frequency
                else:
                    dict_to_save[term] = frequency
        for i in sorted(dict_to_save):
            self.setValueInHashSet(self.inverted_index, i, dict_to_save[i])

    def remove_all(self):
        self.r.flushdb()