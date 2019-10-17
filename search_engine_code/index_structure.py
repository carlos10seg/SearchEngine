class IndexStructure:
    def __init__(self, terms, frequencies, doc_id):
        self.Terms = terms
        self.Frequencies = frequencies
        self.doc_id = doc_id

    def get_max_freq(self):
        return max(self.Frequencies).split(':')[1] if self.Frequencies and len(self.Frequencies) > 0 else 0
    
    def get_term_freq(self, term):
        for i in range(len(self.Terms)):
            if self.Terms[i] == term:
                return self.Frequencies[i].split(":")[1]
        return 0