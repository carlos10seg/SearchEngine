import operator
import math
import re
from structure_builder import StructureBuilder
from redis_manager import RedisManager
from db_manager import DbManager

class Engine:    
    
    def __init__(self):
        self.q_terms_freqs = {}
        self.docs_count = 1662757

    def get_q_doc_freq(self, q_term, doc_id):
        for doc_with_freq in self.q_terms_freqs[q_term]:
            doc_freq = doc_with_freq.split(':') # 0-index is docId | 1-index is the doc frequency
            docId = doc_freq[0]
            docFreq = doc_freq[1]
            if docId == docId:
                return docFreq

    def calc_tf_idf(self, freq, max_freq_doc, N_documents, ni):
        return (int(freq)/int(max_freq_doc)) * math.log2(N_documents/ni)

    # 𝑇𝐹(𝑤,𝑑)= 𝑓𝑟𝑒𝑞(𝑤,𝑑) / 𝑚𝑎𝑥𝑑 
    # w is a non-stop, stemmed/lemmatized word in q
    # freq(w, d) is the number of times w appears in d
    # maxd is the number of times the most frequently-occurred term appears in d (which is constant for each document)
    # ------
    # 𝐼𝐷𝐹(𝑤)=𝑙𝑜𝑔2 𝑁 / 𝑛𝑤
    # N is the number of documents in DC
    # nw is the number of documents in DC in which w appears at least once.
    def rank(self, doc_ids, q_terms):
        """
        docs => array, every 
            doc => should have an array of terms
                [term] => must have frequency
                
        Calculate Relevance Score
        1) Calculate TF
        I need for each document the list of words (non-stop, stemmed/lemmatized) and their frequencies
        I need the frequency of the most frequently-occurred term of each document (constant per document)
        2) Calculate IDF
        I need the number of documents in DC (constant)
        I need the number of documents in DC in which w appears at least once.
        """
        redisManager = RedisManager()
        dbManager = DbManager()
        builder = StructureBuilder()
        docs_relevant_scores = {}

        for doc_id in doc_ids:
            #relevant_score = 0
            tf_idf_sum = 0
            #denom_di_sum = 0
            #denom_qi_sum = 0
            for q_term in q_terms:
                q_doc_freq = self.get_q_doc_freq(q_term, doc_id)
                #max_freq_doc = redisManager.getValueFromHashSet(redisManager.max_freq_doc, doc_id)
                max_freq_doc = dbManager.get_max_freq_doc(doc_id)
                # number of documents in DC in which q_term appears at least once.
                n_docs_q_term = len(self.q_terms_freqs[q_term])

                tf_idf_doc = self.calc_tf_idf(q_doc_freq, max_freq_doc, self.docs_count, n_docs_q_term)
                #tf_idf_q = calc_tf_idf(frequencies_q[i], max_freq_q, N, number_documents_with_terms[i])
                #tf_idf = tf_idf_doc # * tf_idf_q
                tf_idf_sum += tf_idf_doc
            docs_relevant_scores[doc_id] = round(tf_idf_sum, 3)
        sorted_candidate_all_resources = sorted(docs_relevant_scores.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_candidate_all_resources

    
    def get_candidate_documents_ids(self, q_terms):
        """
        1) look for each stemmed query term in redis to get their documents e.g. => 1:5,2:10,4:22
        2) create a dictionary with doc:count
        3) only return the docs that have all query terms, if there are less than 50, 
            then reduce the amount of minimum query terms until you get 50 or more.
            
        --for every doc that already exists add the current freq
        --3) order the dictionary by the most frequent and return the id docs list.
        """        
        MAX_DOCUMENTS_TO_RETRIEVE = 50
        candidate_documents = []        
        redisManager = RedisManager()
        dbManager = DbManager()
        candidate_all_resources = {} # used to track every candidate document => doc:totalFrequency
        unique_documents = {} # only tracks the unique_documents => doc:count
        for q_t in q_terms:
            #doc_freqs = redisManager.getValue(q_t)
            doc_freqs = dbManager.get_index_term(q_t)
            if doc_freqs != None:
                docs_with_frequency = doc_freqs.split(',')
                self.q_terms_freqs[q_t] = docs_with_frequency
                for doc_with_freq in docs_with_frequency:
                    if len(doc_with_freq) > 1:
                        doc_freq = doc_with_freq.split(':') # 0-index is docId | 1-index is the doc frequency
                        docId = doc_freq[0]
                        docFreq = doc_freq[1]
                        if docId in candidate_all_resources:
                            candidate_all_resources[docId] += docFreq
                            unique_documents[docId] += 1
                        else:
                            candidate_all_resources[docId] = docFreq
                            unique_documents[docId] = 1

        # now, let's figure out which documents have all query terms and which have the most frequency
        # first, let's see the documents which have at least half of the document terms
        min_size = int(len(q_terms) / 2)
        max_size = len(q_terms)
        while max_size >= min_size:
            candidate_documents += [k for k, v in unique_documents.items() if v == max_size and candidate_documents.count(v) == 0]
            max_size -= 1 

        if len(candidate_documents) < MAX_DOCUMENTS_TO_RETRIEVE:
            # second, let's see the documents with most frequency. Only if there are less than MAX_DOCUMENTS_TO_RETRIEVE in the candidate_documents
            sorted_candidate_all_resources = sorted(candidate_all_resources.items(), key=operator.itemgetter(1), reverse=True)
            for k, v in sorted_candidate_all_resources:
                if not candidate_documents.count(k):
                    candidate_documents.append(v)
                if len(candidate_documents) >= MAX_DOCUMENTS_TO_RETRIEVE:
                    break

        if len(candidate_documents) > MAX_DOCUMENTS_TO_RETRIEVE:
            candidate_documents = candidate_documents[0:MAX_DOCUMENTS_TO_RETRIEVE]
        
        return candidate_documents

    def get_ranked_docs_with_snippets(self, query):
        builder = StructureBuilder()
        q_terms = builder.get_stemmed_tems(query)
        candidate_docs = self.get_candidate_documents_ids(q_terms)
        ranked_docs = self.rank(candidate_docs, q_terms)
        #print(ranked_docs)
        docs_with_snippets = self.add_snippets(ranked_docs, q_terms)
        return docs_with_snippets

    def add_snippets(self, ranked_docs, q_terms):
        redisManager = RedisManager()
        dbManager = DbManager()
        builder = StructureBuilder()
        docs_with_snippets = []
        
        for ranked_doc in ranked_docs:
            doc_id = ranked_doc[0]
            docs_relevant_scores = {}     
            #doc = redisManager.getValueFromHashSet(redisManager.collection_documents, doc_id)
            doc = dbManager.get_document(doc_id)
            sentences = self.get_doc_sentences(doc)
            title = sentences.pop(0)['content']
            N = len(sentences)
            top_snippets = []
            if N > 0:
                num_docs_for_q_terms = {}
                for q_term in q_terms:
                    num_docs_for_q_terms[q_term] = len([s for s in sentences if q_term in s['content']])                
                for sentence in sentences:                    
                    # if the sentence has less than 2 character then it is probabily not an actual sentence.
                    if len(sentence['content']) <= 2: continue
                    sentence_id = sentence['id']
                    tf_idf_sum = 0
                    index_sentence = builder.get_stemmed_terms_frequencies_from_doc(sentence)
                    #s_terms = builder.get_stemmed_tems(sentence)
                    for q_term in q_terms:
                        #q_sentence_freq = s_terms.count(q_term)
                        q_sentence_freq = index_sentence.get_term_freq(q_term)
                        max_freq = index_sentence.get_max_freq()
                        # if the query term doesn't have frequency on the sentence and there is no max freq. then disregard this q_term
                        if (q_sentence_freq == 0 and max_freq == 0):
                            continue
                        tf_idf_doc = self.calc_tf_idf(q_sentence_freq, max_freq, N, num_docs_for_q_terms[q_term]) if num_docs_for_q_terms[q_term] != 0 else 0
                        tf_idf_sum += tf_idf_doc
                    docs_relevant_scores[sentence_id] = round(tf_idf_sum, 3)

                sorted_candidate_all_resources = sorted(docs_relevant_scores.items(), key=operator.itemgetter(1), reverse=True)
                top_sentences = sorted_candidate_all_resources[0:2]
                top_snippets = [s['content'] for s in sentences if s['id'] == top_sentences[0][0] or s['id'] == top_sentences[1][0]]
            docs_with_snippets.append({"doc": doc_id, "score":ranked_doc[1], "title": title, "snippets": top_snippets})
        return docs_with_snippets



    def get_doc_sentences(self, doc):
        #builder = StructureBuilder()
        #regex = r"[^\.\!\?]*[\.\!\?]"
        doc_lines = doc.split('\n')
        if len(doc_lines) > 0:
            sentences = []
            id = 0
            for doc_line in doc_lines:
                # r1 = re.findall(regex, doc_line)
                # #if doc_line.count(". ") > 0:
                # if len(r1) > 0:
                #     #doc_sentences = doc_line.split('. ')
                #     for doc_sentence in r1:
                #         #sentences.append(builder.get_stemmed_terms_frequencies_from_doc({ "content": doc_sentence, "id": id}))
                #         sentences.append({ "content": doc_sentence, "id": id})
                #         #sentences.append(doc_sentence)
                #         id += 1
                # else:
                #     if doc_line != "":
                #         if id != 0:
                #             #sentences.append(builder.get_stemmed_terms_frequencies_from_doc({ "content": doc_line, "id": id}))
                #             sentences.append({ "content": doc_line, "id": id})
                #             #sentences.append(doc_line)
                #         id += 1

                if doc_line.count('<br>'):
                    for l in doc_line.split('<br>'):
                        if l != "":
                            sentences.append({ "content": l, "id": id})
                            id += 1
                    continue

                if doc_line != "":                    
                        #sentences.append(builder.get_stemmed_terms_frequencies_from_doc({ "content": doc_line, "id": id}))
                    sentences.append({ "content": doc_line, "id": id})
                        #sentences.append(doc_line)
                    id += 1
            return sentences
        else:
            return [doc]
