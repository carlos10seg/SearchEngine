import re
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from index_structure import IndexStructure
#nltk.download('punkt')

class StructureBuilder:
    # without stem
    #stopwords = ['a','about','above','after','again','against','all','am','an','and','any','are','aren''t','as','at','be','because','been','before','being','below','between','both','but','by','can''t','cannot','could','couldn''t','did','didn''t','do','does','doesn''t','doing','don''t','down','during','each','few','for','from','further','had','hadn''t','has','hasn''t','have','haven''t','having','he','he''d','he''ll','he''s','her','here','here''s','hers','herself','him','himself','his','how','how''s','i','i''d','i''ll','i''m','i''ve','if','in','into','is','isn''t','it','it''s','its','itself','let''s','me','more','most','mustn''t','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','shan''t','she','she''d','she''ll','she''s','should','shouldn''t','so','some','such','than','that','that''s','the','their','theirs','them','themselves','then','there','there''s','these','they','they''d','they''ll','they''re','they''ve','this','those','through','to','too','under','until','up','very','was','wasn''t','we','we''d','we''ll','we''re','we''ve','were','weren''t','what','what''s','when','when''s','where','where''s','which','while','who','who''s','whom','why','why''s','with','won''t','would','wouldn''t','you','you''d','you''ll','you''re','you''ve','your','yours','yourself','yourselves', ',', ':', '.']
    # with stem
    stopwords=['a','about','abov','after','again','against','all','am','an','and','ani','are','aren''t','as','at','be','becaus','been','befor','be','below','between','both','but','by','can''t','cannot','could','couldn''t','did','didn''t','do','doe','doesn''t','do','don''t','down','dure','each','few','for','from','further','had','hadn''t','ha','hasn''t','have','haven''t','have','he','he''d','he''ll','he''s','her','here','here''s','her','herself','him','himself','hi','how','how''s','i','i''d','i''ll','i''m','i''ve','if','in','into','is','isn''t','it','it''s','it','itself','let''s','me','more','most','mustn''t','my','myself','no','nor','not','of','off','on','onc','onli','or','other','ought','our','our','ourselv','out','over','own','same','shan''t','she','she''d','she''ll','she''s','should','shouldn''t','so','some','such','than','that','that''s','the','their','their','them','themselv','then','there','there''s','these','they','they''d','they''ll','they''re','they''ve','thi','those','through','to','too','under','until','up','veri','wa','wasn''t','we','we''d','we''ll','we''re','we''ve','were','weren''t','what','what''s','when','when''s','where','where''s','which','while','who','who''s','whom','whi','whi''s','with','won''t','would','wouldn''t','you','you''d','you''ll','you''re','you''ve','your','your','yourself','yourselv',',',':','.']
    #'!', '#', '$', '%', '&', '\'', '\'\'']

    def __atoi(self, text):
        try:            
            return int(text) if text.isdigit() else text
        except ValueError:
            return text

    def __natural_keys(self, text):
        return [self.__atoi(c) for c in re.split(r'(\d+)', text) ]

    def get_stemmed_tems(self, text):
        stemmed_terms = []
        ps = PorterStemmer()
        words = word_tokenize(text.lower())
        for w in words:
            w = ps.stem(w) # get the stem
            if w not in self.stopwords: # only use words not in stopwords
                stemmed_terms.append(w)
        return stemmed_terms

    def get_stemmed_terms_frequencies_from_doc(self, doc):
        # create the inverted index
        #Steps:
        # 1. Create the word-document list
        # 2. Sort the word-document list by word
        # 3. Add the position to the document column and remove duplicates because of the position value.

        #for step 1:
        #indexDict = {'Term': [], 'Document': []}
        #for step 3:
        #indexDict = {'Term': [], 'Document:position': []}

        terms = []
        frequencies = []
        docCount = 1
        cleaned_corpus = []
        mode = 2 # 1: Position | 2: Frequency
        ps = PorterStemmer()
        
        finalDoc = ''
        words = word_tokenize(doc['content'].lower())

        # we stem and remove stopwords from the docs
        words = [ps.stem(w) for w in words if w not in self.stopwords] 
        wordPosition = 1
        countWords = 0
     
        for w in words:
            countWords = words.count(w)
            #w = ps.stem(w) # get the stem

            #if w not in self.stopwords: # only use words not in stopwords
            finalDoc += w + ' '
            # only for step 1:
            #terms.append(w)
            #frequencies.append(str(docCount))            
            #for step 3:
            #docValue = str(docCount) + ':' + (str(wordPosition) if mode == 1 else str(countWords))
            docValue = str(doc['id']) + ':' + (str(wordPosition) if mode == 1 else str(countWords))
            if (w in terms):
                currentIndex = terms.index(w)
                if (mode == 2):
                    # we count all the words and add them only once, 
                    # so if there are more than one word, it is only added once to the frequencies but counted correctly
                    if (docValue not in frequencies[currentIndex]): 
                        frequencies[currentIndex] += ',' + docValue
                else:
                    frequencies[currentIndex] += ',' + docValue
            else:
                terms.append(w)
                frequencies.append(w + '-' + docValue)
            wordPosition += 1
        docCount += 1
        cleaned_corpus.append(finalDoc)
       
       
        # for step 3:
        terms.sort()
        frequencies.sort(key=self.__natural_keys)
        for i in range(len(frequencies)):
            frequencies[i] = re.sub(r'.*-', '', frequencies[i])
            
        #indexDict['Term'] = terms
        # only for step 1:
        #indexDict['Document'] = frequencies
        # for step 3:
        #indexDict['Document:frequency'] = frequencies

        #invertedIndex = pd.DataFrame.from_dict(indexDict)        
        return IndexStructure(terms, frequencies, doc['id'])
    

    def get_stemmed_terms_frequencies(self, corpus):
        # create the inverted index
        #Steps:
        # 1. Create the word-document list
        # 2. Sort the word-document list by word
        # 3. Add the position to the document column and remove duplicates because of the position value.

        #for step 1:
        #indexDict = {'Term': [], 'Document': []}
        #for step 3:
        indexDict = {'Term': [], 'Document:position': []}

        terms = []
        frequencies = []
        docCount = 1
        cleaned_corpus = []
        mode = 2 # 1: Position | 2: Frequency
        ps = PorterStemmer()

        for doc in corpus:
            finalDoc = ''
            words = word_tokenize(doc['content'].lower())
            # we stem and remove stopwords from the docs
            words = [ps.stem(w) for w in words if w not in self.stopwords] 
            wordPosition = 1
            countWords = 0
            for w in words:
                # if a word contains more than 2 times the character "\" then do not add it to the
                if w.count("\\") > 2:
                    continue
                countWords = words.count(w)
                #w = ps.stem(w) # get the stem

                #if w not in self.stopwords: # only use words not in stopwords
                finalDoc += w + ' '
                # only for step 1:
                #terms.append(w)
                #frequencies.append(str(docCount))            
                #for step 3:
                #docValue = str(docCount) + ':' + (str(wordPosition) if mode == 1 else str(countWords))
                docValue = str(doc['id']) + ':' + (str(wordPosition) if mode == 1 else str(countWords))
                if (w in terms):
                    currentIndex = terms.index(w)
                    if (mode == 2):
                        # we count all the words and add them only once, 
                        # so if there are more than one word, it is only added once to the frequencies but counted correctly
                        if (docValue not in frequencies[currentIndex]): 
                            frequencies[currentIndex] += ',' + docValue
                    else:
                        frequencies[currentIndex] += ',' + docValue
                else:
                    terms.append(w)
                    frequencies.append(w + '-' + docValue)
                wordPosition += 1
            docCount += 1
            cleaned_corpus.append(finalDoc)
        # for step 3:
        terms.sort()
        frequencies.sort(key=self.__natural_keys)
        for i in range(len(frequencies)):
            frequencies[i] = re.sub(r'.*-', '', frequencies[i])
            
        #indexDict['Term'] = terms
        # only for step 1:
        #indexDict['Document'] = frequencies
        # for step 3:
        #indexDict['Document:frequency'] = frequencies

        #invertedIndex = pd.DataFrame.from_dict(indexDict)        
        return IndexStructure(terms, frequencies, None)