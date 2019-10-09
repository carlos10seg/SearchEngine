from structure_builder import StructureBuilder
from redis_manager import RedisManager

class Engine:
    # 𝑇𝐹(𝑤,𝑑)= 𝑓𝑟𝑒𝑞(𝑤,𝑑) / 𝑚𝑎𝑥𝑑 
    # w is a non-stop, stemmed/lemmatized word in q
    # freq(w, d) is the number of times w appears in d
    # maxd is the number of times the most frequently-occurred term appears in d (which is constant for each document)
    # ------
    # 𝐼𝐷𝐹(𝑤)=𝑙𝑜𝑔2 𝑁 / 𝑛𝑤
    # N is the number of documents in DC
    # nw is the number of documents in DC in which w appears at least once.
    def rank(self, docs, query):
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
    
    def get_candidate_documents(self, query):
        """
        1) look for each stemmed query term in redis to get their documents
        2) create a dictionary with doc:count
        3) only return the docs that have all query terms, if there are less than 50, 
            then reduce the amount of minimum query terms until you get 50 or more.
            
        --for every doc that already exists add the current freq
        --3) order the dictionary by the most frequent and return the id docs list.
        """

        builder = StructureBuilder()
        redisManager = RedisManager()
        q_terms = builder.get_stemmed_terms_frequencies(query)
        for q_t in q_terms:
            doc_freqs = redisManager.getValue(q_t)