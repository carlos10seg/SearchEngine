from structure_builder import StructureBuilder
from engine import Engine
from redis_manager import RedisManager
import re

# ## Test the frequencies and max freq
# corpus = [{"id": 5, "content": "Vicente Pascual Pastor\n\nVicente Pascual Pastor (Alcoy, june 3, 1865 - Alcoy, february 2, 1941) was a spanish architect, one of the main architects of the Art Nouveau in Alcoy and the Valencian Art Nouveau.\n\nVicente Pascual Pastor was formed in the Barcelona School of Architecture and again in his natal city, in 1891 he becomes municipal architect of Alcoy. He alternates this work with the teaching in the School of Arts and Alcoy's Trades, of which he will be the director in 1903. \n\nBetween 1909 and 1913 he becomes mayor of the Alcoy town hall. As a mayor he stimulated the construction of houses for workers in modern and healthy conditions. Inside the social and industrial life of the city, he was present in Alcoy's Savings Bank and in the institution Alcoy's Industrial Circle. He married in 1916 with Elena Perez, who had descent.\n\nThe art nouveau style of Vicente Pascual will have a few exuberant characteristics and a direct influence of the french and belgian art nouveau. \n\nThe great majority of the projects realized by Vicente Pascual were built in Alcoy, being more than 60 the works that he realized along his life. He realized also some interesting works in Bocairent (Valencia) and Banyeres de Mariola (Alicante).\n\nRelation of works by chronological order:"}]
# builder = StructureBuilder()
# index = builder.get_stemmed_terms_frequencies(corpus)
# print(index.Frequencies)
# print(index.get_max_freq())

# ## Test the ranking
query = 'A killer performance in Spanish'
engine = Engine()
docs = engine.get_ranked_docs_with_snippets(query)
for doc in docs[0:6]:
    print(doc)

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