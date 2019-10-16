import operator
import math
from structure_builder import StructureBuilder
from redis_manager import RedisManager

class Engine:
    docs_count = 1662757
    
    def __init__(self):
        self.q_terms_freqs = {}

    def get_q_doc_freq(self, q_term, doc_id):
        for doc_with_freq in self.q_terms_freqs[q_term]:
            doc_freq = doc_with_freq.split(':') # 0-index is docId | 1-index is the doc frequency
            docId = doc_freq[0]
            docFreq = doc_freq[1]
            if docId == docId:
                return docFreq

    def calc_tf_idf(self, freq, max_freq_doc, N_documents, ni):
        return (freq/max_freq_doc) * math.log2(N_documents/ni)

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
        builder = StructureBuilder()
        relevant_score = 0
        for doc_id in doc_ids:

            for q_term in q_terms:
                q_doc_freq = self.get_q_doc_freq(q_term, doc_id)
                max_freq_doc = redisManager.getValueFromHashSet(redisManager.max_freq_doc, doc_id)
                # number of documents in DC in which q_term appears at least once.
                n_docs_q_term = len(self.q_terms_freqs[q_term])


    
    def get_candidate_documents_ids(self, q_terms):
        """
        1) look for each stemmed query term in redis to get their documents e.g. => 1:5,2:10,4:22
        2) create a dictionary with doc:count
        3) only return the docs that have all query terms, if there are less than 50, 
            then reduce the amount of minimum query terms until you get 50 or more.
            
        --for every doc that already exists add the current freq
        --3) order the dictionary by the most frequent and return the id docs list.
        """        
        MAX_DOCUMENTS_TO_RETRIEVE = 100
        candidate_documents = []        
        redisManager = RedisManager()
        candidate_all_resources = {} # used to track every candidate document => doc:totalFrequency
        unique_documents = {} # only tracks the unique_documents => doc:count
        for q_t in q_terms:
            doc_freqs = redisManager.getValueFromHashSet(redisManager.inverted_index, q_t)
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

    def get_ranked_docs(self, query):
        builder = StructureBuilder()
        q_terms = builder.get_stemmed_tems(query)
        candidate_docs = self.get_candidate_documents_ids(q_terms)        

