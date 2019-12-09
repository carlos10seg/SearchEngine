import pickle
import os
import operator
from db_manager import DbManager

class PickleManager:

    def __init__(self):
        self.directory_path = "files/"

    def storeData(self, data, file_name):
        # Its important to use binary mode
        if not file_name.count(".pickle"):
            file_name += ".pickle"
        data_file = open(self.directory_path + file_name, 'ab') 
      
        # source, destination 
        pickle.dump(data, data_file)
        data_file.close()
    
    def loadData(self, file_name):        
        # for reading also binary mode is important
        data_file = open(self.directory_path + file_name, 'rb')      
        db = pickle.load(data_file)
        data_file.close()
        return db

    def remove_all_files(self):
        if os.path.exists(self.directory_path):
            for file_name in os.listdir(self.directory_path):
                os.remove(self.directory_path + file_name)
        else:
            os.makedirs(self.directory_path)

    def save_index_and_max_freq(self, index_structures, file_name):
        dbManager = DbManager()
        index = {}
        max_freqs = {}
        for index_structure in index_structures:
            dbManager.insert_max_freq_doc(index_structure.doc_id, index_structure.get_max_freq())
            for i in range(len(index_structure.Terms)):
                term = index_structure.Terms[i]
                frequency = index_structure.Frequencies[i]
                if term in index:
                    index[term] = index[term] + "," + str(frequency)
                else:
                    index[term] = str(frequency)
        self.storeData(index, "data_" + file_name)

    def merge_index_structures(self):
        full_index = {}
        for file_name in os.listdir(self.directory_path):
            if file_name.count(".pickle"):
                index_structure = self.loadData(file_name)
                for term, frequency in index_structure.items():
                    if term in full_index:
                        full_index[term] = full_index[term] + "," + str(frequency)
                    else:
                        full_index[term] = str(frequency)
        
        sorted_full_index = sorted(full_index.items(), key=operator.itemgetter(0))
        self.storeData(sorted_full_index, "full")
        return sorted_full_index
  