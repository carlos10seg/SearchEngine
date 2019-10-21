import sys
import csv
import multiprocessing
import datetime
from pprint import pprint
from document import Document
from structure_builder import StructureBuilder
from db_manager import DbManager
from pickle_manager import PickleManager

csv.field_size_limit(sys.maxsize)

class StructureManager:

    def build_index_and_doc_collection_from_csv(self):
        count = -1
        docsCount = 1042755 #1662756 => 1662757 - 1 (header)
        batchSize = 10000 #10000
        loops = (int)(docsCount / batchSize) + 1 # 1662.757 + 1        
        builder = StructureBuilder()
        dbManager = DbManager()
        pickleManager = PickleManager()
        sub_list = []
        from_list = 620001 #1
        to_list = 1662756 #1662756 #1650000 #100000
        # drop and create the collections in mongo
        #dbManager.rebuild_structure()
        # delete all pickle files
        #pickleManager.remove_all_files()

        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')
            for row in csv_content:
                 #or count < from_list): 
                count += 1
                if (count == 0 or count < from_list):  #skip the headers or the previous processed documents                    
                    continue
                doc_id = int(row[2])
                doc_content = row[0]

                dbManager.insert_document({'id': doc_id, 'content': doc_content})                
                # add to the sublist waiting to save the list in a batch operation
                sub_list.append({'id': doc_id, 'content': doc_content})
                if count % batchSize == 0: # every batchSize documents send the work to process pool
                    with multiprocessing.Pool(processes=max(multiprocessing.cpu_count()-1, 1)) as pool:
                        # create the index structure
                        index_structures = pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                        pickleManager.save_index_and_max_freq(index_structures, str(count))

                    print("%d : %d : %s" % (loops, count, datetime.datetime.now()))
                    sub_list = [] # empty the list for the next ones.
                    loops -= 1
                if loops <= 1 and count == to_list and len(sub_list) > 0:
                    with multiprocessing.Pool() as pool:
                        # create the index structure
                        index_structures = pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                        pickleManager.save_index_and_max_freq(index_structures, str(count))
                    print("%d : %d : reminder: %s" % (loops, count ,datetime.datetime.now()))
                
                if count == to_list:
                    break

        print("Saved docs and max_freq in mongo. Saved index structures in pickles: %s" % (datetime.datetime.now())) 

    def build_index_from_pickles(self):
        dbManager = DbManager()
        pickleManager = PickleManager()
        print("merging pickles: %s" % (datetime.datetime.now())) 
        full_index = pickleManager.merge_index_structures()
        print("saving full index: %s" % (datetime.datetime.now())) 
        dbManager.save_full_index(full_index)
        print("full index saved: %s" % (datetime.datetime.now())) 
 
    def build_all_structure(self):
        print("start time: %s" % (datetime.datetime.now()))
        self.build_index_and_doc_collection_from_csv()
        self.build_index_from_pickles()
        print("end time: %s" % (datetime.datetime.now())) 

    def build_index_from_csv(self):
        count = 0
        docsCount = 1662757
        batchSize = 1000
        loops = (int)(docsCount / batchSize) + 1 # 1662.757 + 1
        #remainder = docsCount % batchSize
        print("start time: %s" % (datetime.datetime.now())) 
        builder = StructureBuilder()
        #redisManager = RedisManager()
        index_structures = []        
        sub_list = []
        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')
            #pool = multiprocessing.Pool()
            for row in csv_content:
                count += 1
                if (count == 1): # skip the headers
                    continue               
                sub_list.append({'id': row[2], 'content': row[0]})
                if count % batchSize == 0: # every 1000 documents send the work to process pool
                    with multiprocessing.Pool() as pool:
                        # create the index structure
                        index_structures += pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                    #index_structures += builder.get_stemmed_terms_frequencies_from_doc(sub_list) 
                    print("%d : %d : %s" % (loops, count, datetime.datetime.now()))
                    sub_list = [] # empty the list for the next ones.
                    loops -= 1
                if loops <= 1:
                    with multiprocessing.Pool() as pool:
                        # create the index structure
                        index_structures += pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                    print("%d : reminder: %s" % (count ,datetime.datetime.now()))
                
                # temp => sample testing
                if count >= 10000:
                    break

        print("finish to build structure in memory: %s" % (datetime.datetime.now()))         
        #redisManager.save_array_many_in_index(index_structures)
        print("saved in redis: %s" % (datetime.datetime.now())) 
        
    def build_documents_collection_from_csv(self):
        count = 0 # 1662757
        print("start time: %s" % (datetime.datetime.now())) 
        dbManager = DbManager()
        #redisManager = RedisManager()
        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')        
            for row in csv_content:
                count += 1
                if (count == 1): # skip the headers
                    continue
                #dbManager.insert_document({'id': row[2], 'content': row[0]})
                #redisManager.setValueInHashSet(redisManager.collection_documents, row[2], row[0])
                if count % 1000 == 0:
                    print("%d : time: %s" % (count ,datetime.datetime.now()))
                
                # temp => sample testing
                if count >= 10000:
                    break
        
        print("end time: %s" % (datetime.datetime.now()))