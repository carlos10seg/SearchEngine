from pymongo import MongoClient

class DbManager:
    def __init__(self):
        client = MongoClient(host='10.5.0.6', port=27017)
        self.collection_documents_table_name = "collection_documents_sample"
        self.max_freq_doc_table_name = "max_freq_doc_sample"
        self.inverted_index_table_name = "inverted_index_sample"
        self.db = client.searchengine
        self.collection_documents = self.db[self.collection_documents_table_name]
        self.max_freq_doc = self.db[self.max_freq_doc_table_name]
        self.inverted_index = self.db[self.inverted_index_table_name]
        
    def rebuild_structure(self):
        self.db.drop_collection(self.collection_documents_table_name)
        self.db.drop_collection(self.max_freq_doc_table_name)
        self.db.drop_collection(self.inverted_index_table_name)
        self.collection_documents.create_index("id", unique=True)
        self.max_freq_doc.create_index("doc_id", unique=True)
        self.inverted_index.create_index("term", unique=True)
    
    def insert_many_in_documents(self, list):
        self.collection_documents.insert_many(list)

    def insert_document(self, doc):
        self.collection_documents.insert_one(doc)

    def get_document(self, doc_id):
        doc = self.collection_documents.find_one({'id': int(doc_id)}, {'content':1, "_id": False})
        return doc['content'] if doc != None else None

    def insert_many_in_index(self, list):
        self.inverted_index.insert_many(list)

    def update_index_term(self, term, frequency):
        self.inverted_index.update_one({'term': term}, {'$set': {'frequency': frequency}})

    def insert_index_term(self, term, frequency):
        self.inverted_index.insert_one({'term': term, 'frequency': frequency})
    
    def get_index_term(self, term):
        freq = self.inverted_index.find_one({'term': term}, {'frequency':1, "_id": False})
        return freq['frequency'] if freq != None else None

    def insert_max_freq_doc(self, doc_id, max_freq):
        self.max_freq_doc.insert_one({'doc_id': int(doc_id), 'max_freq': int(max_freq)})

    def get_max_freq_doc(self, doc_id):
        max_freq = self.max_freq_doc.find_one({'doc_id': int(doc_id)}, {'max_freq':1, "_id": False})
        return max_freq['max_freq'] if max_freq != None else None

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