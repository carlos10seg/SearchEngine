import sys
import csv
import multiprocessing
import datetime
from pprint import pprint
from document import Document
from structure_builder import StructureBuilder
from db_manager import DbManager
from redis_manager import RedisManager

csv.field_size_limit(sys.maxsize)

class StructureManager:

    def build_index_and_doc_collection_from_csv(self):
        count = -1
        docsCount = 1662757
        batchSize = 10
        loops = (int)(docsCount / batchSize) + 1 # 1662.757 + 1
        print("start time: %s" % (datetime.datetime.now())) 
        builder = StructureBuilder()
        redisManager = RedisManager()
        sub_list = []
        from_list = 11 #1
        to_list = 20 #100000
        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')
            for row in csv_content:                
                 #or count < from_list): 
                count += 1
                if (count == 0 or count < from_list):  #skip the headers or the previous processed documents                    
                    continue
                doc_id = row[2]
                doc_content = row[0]
                
                #if (doc_content[0] == '"' and doc_content[-1] == '"'):
                #    doc_content = doc_content[1:-1]
                # add the document to the collection in redis
                redisManager.setValueInHashSet(redisManager.collection_documents, doc_id, doc_content)
                # add to the sublist waiting to save the list in a batch operation
                sub_list.append({'id': doc_id, 'content': doc_content})
                if count % batchSize == 0: # every 1000 documents send the work to process pool
                    with multiprocessing.Pool(processes=max(multiprocessing.cpu_count()-1, 1)) as pool:
                        # create the index structure
                        index_structures = pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                        redisManager.save_many_in_index(index_structures)
                    print("%d : %d : %s" % (loops, count, datetime.datetime.now()))
                    sub_list = [] # empty the list for the next ones.
                    loops -= 1
                if loops <= 1:
                    with multiprocessing.Pool() as pool:
                        # create the index structure
                        index_structures = pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                        redisManager.save_many_in_index(index_structures)
                    print("%d : reminder: %s" % (count ,datetime.datetime.now()))
                
                # temp => sample testing
                if count == to_list:
                    break

        print("saved in redis: %s" % (datetime.datetime.now())) 

    def build_index_from_csv(self):
        count = 0
        docsCount = 1662757
        batchSize = 1000
        loops = (int)(docsCount / batchSize) + 1 # 1662.757 + 1
        #remainder = docsCount % batchSize
        print("start time: %s" % (datetime.datetime.now())) 
        builder = StructureBuilder()
        redisManager = RedisManager()
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
        redisManager.save_array_many_in_index(index_structures)
        print("saved in redis: %s" % (datetime.datetime.now())) 
        
    def build_documents_collection_from_csv(self):
        count = 0 # 1662757
        print("start time: %s" % (datetime.datetime.now())) 
        dbManager = DbManager()
        redisManager = RedisManager()
        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')        
            for row in csv_content:
                count += 1
                if (count == 1): # skip the headers
                    continue
                #dbManager.insert_document({'id': row[2], 'content': row[0]})
                redisManager.setValueInHashSet(redisManager.collection_documents, row[2], row[0])
                if count % 1000 == 0:
                    print("%d : time: %s" % (count ,datetime.datetime.now()))
                
                # temp => sample testing
                if count >= 10000:
                    break
        
        print("end time: %s" % (datetime.datetime.now()))
 
    def build_all_structure(self):
        #self.build_documents_collection_from_csv()
        #self.build_index_from_csv()
        self.build_index_and_doc_collection_from_csv()

    def build_index_from_csv_old(self):
        x = 0
        sub_list = []
        count = 0 # 1662757
        max_count = 101 # always end in 1 because the first line is the header
        builder = StructureBuilder()
        dbManager = DbManager()
        redisManager = RedisManager()
        index_structures = []
        end_count = 0
        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')        
            for row in csv_content:
                count += 1
                if (count == 1): # skip the headers
                    continue
                # if (x < 5):
                #     print(row)
                #     #print(row[1])
                #     #print(row[0],row[1],row[2],)
                # else:
                #     break
                # x += 1

                # create a document with id and content and append it to the list
                #sub_list.append(Document(row[2], row[0]))
                sub_list.append({'id': row[2], 'content': row[0]})
                #print(row[0])
                if (count == max_count):
                    # save the documents
                    #dbManager.insert_many_in_documents(sub_list)
                    with multiprocessing.Pool() as pool:
                        # create the index structure
                        index_structures += pool.map(builder.get_stemmed_terms_frequencies_from_doc, sub_list)
                        # save the index structure and update the terms if necessary
                        #dbManager.save_many_in_index(index_structure)
                    # create the index structure
                    #index_structure = builder.get_stemmed_terms_frequencies(sub_list)
                    # save the index structure and update the terms if necessary
                    #dbManager.save_many_in_index(index_structure)
                    #redisManager.save_many_in_index(index_structure)
                        count = 0
                        sub_list = []   
                        end_count += 1
                        if (end_count > 3):
                            break
            # print(len(index_structure))
            # print('--------')
            # print(index_structure[0].Terms)
            # print('--------')
            # print(index_structure[0].Frequencies)
            
            redisManager.save_array_many_in_index(index_structures)
            #dbManager.save_array_many_in_index(index_structures)
