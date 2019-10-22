class IndexStructure:
    def __init__(self, terms, frequencies, doc_id):
        self.Terms = terms
        self.Frequencies = frequencies
        self.doc_id = doc_id

    def get_max_freq(self):
        max_freq = 0
        if self.Frequencies and len(self.Frequencies) > 0:
            for f in self.Frequencies:
                freq = int(f.split(':')[1])
                if freq > max_freq:
                    max_freq = freq
        return max_freq
    
    def get_term_freq(self, term):
        for i in range(len(self.Terms)):
            if self.Terms[i] == term:
                return int(self.Frequencies[i].split(":")[1])
        return 0