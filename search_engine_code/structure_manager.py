import sys
import csv
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
        max_count = 100
        builder = StructureBuilder()
        dbManager = DbManager()
        redisManager = RedisManager()
        with open("../data/wikipedia_text_files.csv") as csvfile:
            csv_content = csv.reader(csvfile, delimiter=',')        
            for row in csv_content:
                count += 1
                if (count == 1):
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
                    dbManager.insert_many_in_documents(sub_list)
                    # create the index structure
                    index_structure = builder.create_inverted_index(sub_list)
                    # save the index structure and update the terms if necessary
                    dbManager.save_many_in_index(index_structure)
                    redisManager.save_many_in_index(index_structure)
                    count = 0
                    sub_list = []
                    #pprint(index.tail(20))
                    break

