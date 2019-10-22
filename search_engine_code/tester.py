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


# dbManager = DbManager()
# doc = dbManager.get_document(1121030)
# strBuilder = StructureBuilder()
# index_structure = strBuilder.get_stemmed_terms_frequencies_from_doc({'content': doc, 'id': 1})
# print(index_structure.get_max_freq())


suggestionManager = SuggestionManager()
# print("loading logs")
# suggestionManager.load_logs()
# print("getting suggestions")
print(suggestionManager.get_suggestions("worcester telegram"))
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
# doc = {"id": 11, "content": "Sadie Crawford\n\nSadie Crawford (1885-1965), also known as Sadie Johnson and Sadie Mozee, was a British-American performer of the early jazz era, one of the few white female performers of her day to have enjoyed an international career.\n\nBased for the last 35 years of her life in Washington, D.C., United States, she was born Louisa Harriet Marshall in Tooting, London on 27 December 1885. The youngest of the seven children of Francis Thomas Marshall and his wife Ellen Maria, she maintained a close bond with her siblings and their families throughout her life. The household in which she grew up was a somewhat unconventional one: her father, a removal-man, died just before her seventh birthday, and shortly afterwards her mother Ellen began a relationship with a man some 20 years her junior, Louis Slade, with whom in 1892 she went on to have one further child. Ellen and Louis finally married in 1905, four years before Ellen’s death. Most of Louisa’s siblings lived their adult lives in south London. Throughout her life she remained particularly close to her eldest sister Mrs Rhoda Matilda Newbon, who was mother to 13 children.\n\nSadie took to the stage in London in her mid teens, and it is clear that early on she developed a taste for black popular culture, and music in particular. She would marry twice; both her husbands were black Americans. Numerous photographs suggest that she went out of her way to present herself as a 'black', 'coloured' or 'creole' woman, presumably feeling this would give her greater appeal as a performer, and several newspaper articles also suggest that her origins were more exotic than they really were. Throughout her career she seems to have used professionally the forename Sadie, although the origins of this stage name are not known.\n\nVarious sources allow us to piece together Sadie’s career. Not least among these is a short account of her life that she herself wrote in 1960 in her mid 70s. From this we learn that she left school at 11 (working initially as a domestic servant) and within a few years was employed as a dancer at London’s Empire Theatre. Her first big break came with an invitation from the American entertainer Laura Hampton (née Bowman) to join her review troupe, following which she was signed up for a European tour of the show 'A Trip to Coontown'. \nSadie met her first husband, saxophonist Adolph Crawford, in 1906 and was soon working with him as a vaudeville music hall double act, although at this time she was using the name Sadie Johnson. In the years leading up to the First World War the duo can be found performing in Russia, Bucharest, the Balkan States and Scandinavia, as well as Berlin and Paris, and in the war years all corners of the United Kingdom.\n\nSadie and Adolph finally married in Southwark in June 1918, just as the jazz craze was sweeping across Europe. Their international careers started to take off in earnest at this time, with invitations to tour the world pouring in. In the post-war years they can be found as far afield as New Zealand, Australia, Argentina, Uruguay and Brazil, in addition to Austria, Hungary, Estonia, Lithuania and Latvia. Paris, very much the European capital of jazz with so many resident and ad hoc bands and orchestras, became an important base for the duo.\n\nIt was in Paris in the early 1920s that the few recordings to feature them (as part of Gordon Stretton’s ‘Orchestre Syncopated Six’) were made by Pathé; it was also at the American Hospital of Paris, Neuilly-sur-Seine, that Adolph Crawford died in 1929.\n\nWithin a few months of Adolph's death Sadie sailed to New York City with Lew Leslie's ‘Blackbirds’ and it was in the United States that she thereafter settled. After suffering a nervous breakdown she was advised to go to Saratoga Springs to recuperate and it was there she met her second husband Frank Mozee (a chauffeur, some 16 years younger than she was), whom she married in 1930, when she would have been 44. Sadie and Frank made their home in Washington D.C. and it seems that her second marriage effectively marked the end of her stage career. From America she regularly visited her family back in Tooting (in the early years by boat but latterly by plane), staying at the Regent Palace Hotel in central London. Although she had no children of her own, Sadie was ‘foster mother’ to a daughter, Lillian Brown.\nSadie Mozee died at Washington’s District of Columbia General Hospital on 18 December 1965, a few days short of her 80th birthday, the Washington \"Evening Star\" revealing in her obituary notice that her death occurred ‘after a long illness’. The article also states that she was a member of St Martin’s Catholic Church and that she is buried in Washington's Mount Olivet Cemetery. Her husband Frank died in Washington D.C. in 1981."}
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