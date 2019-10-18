from pymongo import MongoClient

class DbManager:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.searchengine
        self.collection_documents = self.db['collection_documents']        
        self.max_freq_doc = self.db['max_freq_doc']
        self.inverted_index = self.db['inverted_index']
        
    def rebuild_structure(self):
        self.db.drop_collection("collection_documents")
        self.db.drop_collection("max_freq_doc")
        self.db.drop_collection("inverted_index")
        self.collection_documents.create_index("id", unique=True)
        self.max_freq_doc.create_index("doc_id", unique=True)
        self.inverted_index.create_index("term", unique=True)
    
    def insert_many_in_documents(self, list):
        self.collection_documents.insert_many(list)

    def insert_document(self, doc):
        self.collection_documents.insert_one(doc)

    def get_document(self, doc_id):
        return self.collection_documents.find_one({'id': doc_id}, {'content':1, "_id": False})['content']

    def insert_many_in_index(self, list):
        self.inverted_index.insert_many(list)

    def update_index_term(self, term, frequency):
        self.inverted_index.update_one({'term': term}, {'$set': {'frequency': frequency}})

    def insert_index_term(self, term, frequency):
        self.inverted_index.insert_one({'term': term, 'frequency': frequency})
    
    def get_index_term(self, term):
        return self.inverted_index.find_one({'term': term}, {'frequency':1, "_id": False})['frequency']

    def insert_max_freq_doc(self, doc_id, max_freq):
        self.max_freq_doc.insert_one({'doc_id': int(doc_id), 'max_freq': int(max_freq)})

    def get_max_freq_doc(self, doc_id):
        return self.max_freq_doc.find_one({'doc_id': doc_id}, {'max_freq':1, "_id": False})['max_freq']

    # def save_many_in_index(self, index_structure):
    #     for i in range(len(index_structure.Terms)):
    #         term = index_structure.Terms[i]
    #         frequency = index_structure.Frequencies[i]
    #         item_from_db = self.get_index_term(term)
    #         if (item_from_db == None):
    #             self.insert_index_term(term, frequency)
    #         else:
    #             new_frequency = item_from_db['frequency'] + ',' + frequency
    #             self.update_index_term(term, new_frequency)

    def save_many_in_index(self, index_structures):
        for index_structure in index_structures:
            self.insert_max_freq_doc(index_structure.doc_id, index_structure.get_max_freq())
            for i in range(len(index_structure.Terms)):
                term = index_structure.Terms[i]
                frequency = index_structure.Frequencies[i]
                item_from_db = self.get_index_term(term)
                if (item_from_db == None):
                    self.insert_index_term(term, frequency)
                else:
                    new_frequency = item_from_db['frequency'] + ',' + frequency
                    self.update_index_term(term, new_frequency)

    def save_full_index(self, full_index_structure):
        for item in full_index_structure: # 0 => term | 1 => frequency
            self.insert_index_term(item[0], item[1])

        # dict_to_save = {}
        # for index_structure in index_structures:
        #     for i in range(len(index_structure.Terms)):
        #         term = index_structure.Terms[i]
        #         frequency = index_structure.Frequencies[i]
        #         dict_to_save[term] = frequency

        # for term in sorted(dict_to_save):
        #     frequency = dict_to_save[term]
        #     item_from_db = self.get_index_term(term)
        #     if (item_from_db == None):
        #         self.insert_index_term(term, frequency)
        #     else:
        #         new_frequency = item_from_db['frequency'] + ',' + frequency
        #         self.update_index_term(term, new_frequency)

'''

manager = DbManager()
manager.insert_index_term('term 1', "1")
term = manager.get_index_term('term 1')
print(term)
manager.update_index_term(term['term'], term['frequency'])


db = client.searchengine
collection_documents = db['collection_documents']
inverted_index = db['inverted_index']
doc1 = {'id': 1, 'title': 'test', 'content': 'test content'}

# add doc
doc_id = collection_documents.insert_one(doc1).inserted_id
pprint.pprint(doc_id)

# Querying
found_doc = collection_documents.find_one({'doc_id': doc_id})
pprint.pprint(found_doc)

# bulk insert
new_docs = [
    {'id': 1, 'title': 'test', 'content': 'test content'},
    {'id': 2, 'title': 'test 2', 'content': 'test content 2'},
    {'id': 3, 'title': 'a test 3', 'content': 'test content 2'}
]
result = collection_documents.insert_many(new_docs)
pprint.pprint(result.inserted_ids)

# Querying for More Than One Document
for doc in collection_documents.find():
    pprint.pprint(doc)

# Counting
pprint.pprint(collection_documents.count_documents({}))

# Range Queries
for doc in collection_documents.find({'id': {'&gt': 1}}).sort('title'):
    pprint.pprint(doc)

# Delete
collection_documents.delete_one({'title': 'test'})

collection_documents.update_one({'title': 'test 2'}, {'$set': {'content': 'updated content'}})
'''