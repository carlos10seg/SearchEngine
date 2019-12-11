import operator
import math
import re
from structure_builder import StructureBuilder
from db_manager import DbManager

class Engine:    
    
    def __init__(self):
        self.q_terms_freqs = {}
        self.docs_count = 1662757
        self.max_freq_docs = {}

    def get_q_doc_freq(self, q_term, doc_id):
        if not q_term in self.q_terms_freqs: return None
        for doc_with_freq in self.q_terms_freqs[q_term]:
            doc_freq = doc_with_freq.split(':') # 0-index is docId | 1-index is the doc frequency
            docId = doc_freq[0]
            docFreq = doc_freq[1]
            if docId == doc_id:
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
        dbManager = DbManager()
        builder = StructureBuilder()
        docs_relevant_scores = {}

        for doc_id in doc_ids:
            tf_idf_sum = 0
            for q_term in q_terms:
                q_doc_freq = self.get_q_doc_freq(q_term, doc_id)
                if q_doc_freq == None: continue # not found on index
                max_freq_doc = dbManager.get_max_freq_doc(doc_id)
                if max_freq_doc != None:
                    self.max_freq_docs[doc_id] = max_freq_doc
                    # number of documents in DC in which q_term appears at least once.
                    n_docs_q_term = len(self.q_terms_freqs[q_term])

                    tf_idf_doc = self.calc_tf_idf(q_doc_freq, max_freq_doc, self.docs_count, n_docs_q_term)
                    tf_idf_sum += tf_idf_doc
            docs_relevant_scores[doc_id] = round(tf_idf_sum, 3)
        sorted_docs_total_freqs = sorted(docs_relevant_scores.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_docs_total_freqs

    def rank_cosine_sim(self, doc_ids, q_terms):
        dbManager = DbManager()
        builder = StructureBuilder()
        docs_relevant_scores = {}
        q_freqs = dict()
        # set the query terms frequencies
        for q_term in q_terms:
            if q_term in q_freqs:
                q_freqs[q_term] += 1
            else:
                q_freqs[q_term] = 1

        # set max frequency
        sorted_q_freqs = sorted(q_freqs.items(), key=operator.itemgetter(1), reverse=True)
        max_q_freq = sorted_q_freqs[0][1]

        for doc_id in doc_ids:
            tf_idf_sum = 0
            denom_di_sum = 0
            denom_qi_sum = 0
            for q_term in q_terms:
                q_doc_freq = self.get_q_doc_freq(q_term, doc_id)
                if q_doc_freq == None: continue # not found on index
                max_freq_doc = dbManager.get_max_freq_doc(doc_id)
                if max_freq_doc != None:
                    self.max_freq_docs[doc_id] = max_freq_doc
                    # number of documents in DC in which q_term appears at least once.
                    n_docs_q_term = len(self.q_terms_freqs[q_term])

                    tf_idf_doc = self.calc_tf_idf(q_doc_freq, max_freq_doc, self.docs_count, n_docs_q_term)
                    tf_idf_q = self.calc_tf_idf(q_freqs[q_term], max_q_freq, self.docs_count, n_docs_q_term)
                    tf_idf = tf_idf_doc * tf_idf_q
                    tf_idf_sum += tf_idf
                    denom_di_sum += tf_idf_doc ** 2
                    denom_qi_sum += tf_idf_q ** 2
                    #tf_idf_sum += tf_idf_doc
            denom = math.sqrt(denom_di_sum) * math.sqrt(denom_qi_sum)
            score = tf_idf_sum/denom
            docs_relevant_scores[doc_id] = round(score, 3)
        sorted_docs_total_freqs = sorted(docs_relevant_scores.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_docs_total_freqs
    
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
        dbManager = DbManager()
        docs_total_freqs = {} # used to track every candidate document => doc:totalFrequency
        q_terms_count_per_doc = {} # only tracks the q_terms_count_per_doc => doc:count
        docs_count_all_terms = []
        count = 1
        for q_t in q_terms:
            doc_freqs = dbManager.get_index_term(q_t)
            if doc_freqs != None:
                docs_with_frequency = doc_freqs.split(',')
                self.q_terms_freqs[q_t] = docs_with_frequency
                for doc_with_freq in docs_with_frequency:
                    if len(doc_with_freq) > 1:
                        doc_freq = doc_with_freq.split(':') # 0-index is docId | 1-index is the doc frequency
                        docId = doc_freq[0]
                        docFreq = doc_freq[1]
                        if docId in docs_total_freqs:                            
                            docs_total_freqs[docId] += docFreq
                            q_terms_count_per_doc[docId] += 1
                            if count == len(q_terms) and q_terms_count_per_doc[docId]  == len(q_terms):
                                docs_count_all_terms.append(q_terms)
                        else:
                            docs_total_freqs[docId] = docFreq
                            q_terms_count_per_doc[docId] = 1
            count += 1

        q_terms_min_size = len(q_terms) if len(q_terms) == 1 else int(len(q_terms) / 2)     
        # get the most frequent terms
        sorted_docs_total_freqs = sorted(docs_total_freqs.items(), key=operator.itemgetter(1), reverse=True)
        for k, v in sorted_docs_total_freqs:
            # get the docs which have all query terms at least
            if q_terms_count_per_doc[k] == len(q_terms):
                candidate_documents.append(k)
            elif len(docs_count_all_terms) < MAX_DOCUMENTS_TO_RETRIEVE:
                candidate_documents.append(k)
            if len(candidate_documents) >= MAX_DOCUMENTS_TO_RETRIEVE:
                break


        if len(candidate_documents) > MAX_DOCUMENTS_TO_RETRIEVE:
            candidate_documents = candidate_documents[0:MAX_DOCUMENTS_TO_RETRIEVE]
        
        return candidate_documents

    def get_local_max_freq(self, q_terms):
        max_value = 1
        for q_term in q_terms:
            q_count = q_terms.count(q_term)
            if (q_count > max_value):
                max_value = q_count
        return max_value

    def add_snippets(self, ranked_docs, query):
        dbManager = DbManager()
        builder = StructureBuilder()
        docs_with_snippets = []
        tf_idf_q_terms = {}
        q_terms = builder.get_stemmed_tems(query)

        for q_term in q_terms:
            # number of documents in DC in which q_term appears at least once.
            n_docs_q_term = len(self.q_terms_freqs[q_term]) if q_term in self.q_terms_freqs else 0
            if n_docs_q_term != 0:
                freq_d = len([q for q in q_terms if q == q_term])
                max_q_freq = self.get_local_max_freq(q_terms)
                tf_idf_q_terms[q_term] = self.calc_tf_idf(freq_d, max_q_freq, self.docs_count, n_docs_q_term)
            else:
                tf_idf_q_terms[q_term] = 0

        for ranked_doc in ranked_docs:
            doc_id = ranked_doc[0]
            docs_relevant_scores = {}     
            doc = dbManager.get_document(doc_id)
            if doc == None: continue
            sentences = self.get_doc_sentences(doc)
            title = sentences.pop(0)['content']

            for sentence in sentences:
                senetence_content = sentence['content']
                # if the sentence has less than 2 character then it is probabily not an actual sentence.
                if len(senetence_content) <= 2: continue
                sentence_id = sentence['id']
                tf_idf_sum = 0
                denom_di_sum = 0
                denom_qi_sum = 0
                index_sentence = builder.get_stemmed_terms_frequencies_from_doc(sentence)
                for q_term in q_terms:
                    # check the not stemmed words                        
                    if q_term in index_sentence.Terms: 
                        q_sentence_freq = index_sentence.get_term_freq(q_term)
                        max_freq = index_sentence.get_max_freq()
                        # if the query term doesn't have frequency on the sentence and there is no max freq. then disregard this q_term
                        if (q_sentence_freq == 0 and max_freq == 0):
                            continue
                        
                        tf_idf_doc = self.calc_tf_idf(q_sentence_freq, max_freq, self.docs_count, len(self.q_terms_freqs[q_term]))
                        tf_idf_q = tf_idf_q_terms[q_term]
                        # The two sentences in d that have the highest cosine similarity with respect to q; with TF-IDF as the term weighting scheme.

                        tf_idf_sum += tf_idf_doc * tf_idf_q
                        denom_di_sum += tf_idf_doc ** 2
                        denom_qi_sum += tf_idf_q ** 2
                
                denom = math.sqrt(denom_di_sum) * math.sqrt(denom_qi_sum)
                score = tf_idf_sum/denom if denom != 0 else 0
                docs_relevant_scores[sentence_id] = round(score, 3)

            sorted_docs_total_freqs = sorted(docs_relevant_scores.items(), key=operator.itemgetter(1), reverse=True)
            top_sentences = sorted_docs_total_freqs[0:2]
            top_snippets = [s['content'] for s in sentences if s['id'] == top_sentences[0][0] or s['id'] == top_sentences[1][0]]
        
            docs_with_snippets.append({"docId": doc_id, "score":ranked_doc[1], "title": title, "snippets": top_snippets})
        return docs_with_snippets

    def get_doc_sentences(self, doc):
        doc_lines = doc.split('\n')
        if len(doc_lines) > 0:
            sentences = []
            id = 0
            for doc_line in doc_lines:
                if doc_line.count('<br>'):
                    for l in doc_line.split('<br>'):
                        if l != "":
                            for s in l.split('.'):
                                if s != '':
                                    sentences.append({ "content": s, "id": id})
                                    id += 1
                    continue

                if doc_line != "":
                    for s in doc_line.split('.'):
                        if s != '':
                            sentences.append({ "content": s, "id": id})
                            id += 1
            return sentences
        else:
            return [doc]

    def get_ranked_docs_with_snippets(self, query):
        builder = StructureBuilder()
        query = query.strip()
        q_terms = builder.get_stemmed_tems(query)
        candidate_docs = self.get_candidate_documents_ids(q_terms)
        # current ranking algorithm:
        #ranked_docs = self.rank(candidate_docs, q_terms)
        # new ranking algorithm:
        ranked_docs = self.rank_cosine_sim(candidate_docs, q_terms)
        docs_with_snippets = self.add_snippets(ranked_docs, query)
        return docs_with_snippets