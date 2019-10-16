class IndexStructure:
    def __init__(self, terms, frequencies, doc_id):
        self.Terms = terms
        self.Frequencies = frequencies
        self.doc_id = doc_id

    def get_max_freq(self):
        return max(self.Frequencies).split(':')[1]