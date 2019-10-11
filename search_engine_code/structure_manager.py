import sys
import csv
import multiprocessing
from pprint import pprint
from document import Document
from structure_builder import StructureBuilder
from db_manager import DbManager
from redis_manager import RedisManager

csv.field_size_limit(sys.maxsize)

class StructureManager:
    def build_index_from_csv(self):
        x = 0
        sub_list = []
        count = 0 # 1662757
        max_count = 11 # always end in 1 because the first line is the header
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
