import re
import datetime
import operator
import sys
import csv
from structure_builder import StructureBuilder
from engine import Engine
from redis_manager import RedisManager
from pickle_manager import PickleManager
from db_manager import DbManager
from controller import Controller
from suggestion_manager import SuggestionManager

pickleManager = PickleManager()
my_data = pickleManager.loadData("data_10k.pkl")
for k, v in my_data.items():
    print(k + ' : ' + v)


# dbManager = DbManager()
# doc = dbManager.get_document(1121030)
# strBuilder = StructureBuilder()
# index_structure = strBuilder.get_stemmed_terms_frequencies_from_doc({'content': doc, 'id': 1})
# print(index_structure.get_max_freq())


#suggestionManager = SuggestionManager()
# print("loading logs")
# suggestionManager.load_logs()
# print("getting suggestions")
#print(suggestionManager.get_suggestions("worcester telegram"))
# print(suggestionManager.get_suggestions("texas"))
# print(suggestionManager.get_suggestions("boise"))


#controller = Controller()
#controller.build_structure()

# ## Test the ranking
# query = 'A killer performance in Spanish'
# engine = Engine()
# docs = engine.get_ranked_docs_with_snippets(query)
# for doc in docs:
#     print(doc)

# csv.field_size_limit(sys.maxsize)
# count = 0
# with open("../data/wikipedia_text_files.csv") as csvfile:
#     csv_content = csv.reader(csvfile, delimiter=',')
#     for row in csv_content:
#             #or count < from_list): 
#         count += 1
# print(count)

# my_dict = {}
# for i in range(10000000):
#     my_dict[i] = "test :" + str(1)
# sorted_dict = sorted(my_dict.items(), key=operator.itemgetter(1), reverse=True)
# print(len(sorted_dict))
# print(sorted_dict[0])

# corpus = [
#     {"id": 5, "content": "Vicente Pascual Pastor\n\nVicente Pascual Pastor (Alcoy, june 3, 1865 - Alcoy, february 2, 1941) was a spanish architect, one of the main architects of the Art Nouveau in Alcoy and the Valencian Art Nouveau.\n\nVicente Pascual Pastor was formed in the Barcelona School of Architecture and again in his natal city, in 1891 he becomes municipal architect of Alcoy. He alternates this work with the teaching in the School of Arts and Alcoy's Trades, of which he will be the director in 1903. \n\nBetween 1909 and 1913 he becomes mayor of the Alcoy town hall. As a mayor he stimulated the construction of houses for workers in modern and healthy conditions. Inside the social and industrial life of the city, he was present in Alcoy's Savings Bank and in the institution Alcoy's Industrial Circle. He married in 1916 with Elena Perez, who had descent.\n\nThe art nouveau style of Vicente Pascual will have a few exuberant characteristics and a direct influence of the french and belgian art nouveau. \n\nThe great majority of the projects realized by Vicente Pascual were built in Alcoy, being more than 60 the works that he realized along his life. He realized also some interesting works in Bocairent (Valencia) and Banyeres de Mariola (Alicante).\n\nRelation of works by chronological order:"},
#     {"id": 1, "content": "test 1"},
#     {"id": 2, "content": "test 2"},
#     {"id": 3, "content": "test 3"}
#     ]

#pickleManager = PickleManager()
# pickleManager.storeData(corpus, "test1")
# print("time: %s" % (datetime.datetime.now()))
# my_data = pickleManager.loadData("data_1000")
# for k, v in my_data.items():
#     print(k + ' : ' + v)
# print("time: %s" % (datetime.datetime.now())) 

# dbManager = DbManager()
# full_index = pickleManager.merge_index_structures()
# print("saving full index: %s" % (datetime.datetime.now())) 
# dbManager.save_full_index(full_index)
# print("full index saved: %s" % (datetime.datetime.now())) 

#pickleManager.remove_all_files()

## Test the frequencies and max freq
# builder = StructureBuilder()
# index = builder.get_stemmed_terms_frequencies_from_doc(doc)
# print(index.Terms)
# print(index.Frequencies)
# print(index.get_max_freq())


## Test the sentences split in the doc
# redisManager = RedisManager()
# doc = redisManager.getValueFromHashSet(redisManager.collection_documents, 318)
# print(doc)
# # # doc = doc.replace('\n', '.')
# # doc = doc.replace('<br>', '.')
# for d in doc.split('\n'):
#     if (d != ''):
#         print(d)
# print('-------------------------')
# # print(doc.split('. '))

# regex = r"[^\.\!\?]*[\.\!\?]"
# doc_lines = doc.split('\n')
# for doc_line in doc_lines:
#     r1 = re.findall(regex, doc_line)
#     #if doc_line.count(". ") > 0:
#     if len(r1) > 0:
#         #doc_sentences = doc_line.split('. ')
#         for doc_sentence in r1:
#             print(doc_sentence)
#     else:
#         if doc_line != "":
#             print(doc_line)


# # regex = r"[^\.\!\?]*[\.\!\?]"
# # r1 = re.findall(regex, doc)
# # print(r1)