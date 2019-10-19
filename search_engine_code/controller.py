import time
from structure_manager import StructureManager
from engine import Engine

class Controller:
    
    def build_structure(self):
        # 1) build the structure in mongo and redis
        manager = StructureManager()
        manager.build_all_structure()

    def get_q_suggestions(self, query):
        # do something
        return
    
    def search(self, query):
        engine = Engine()
        return engine.get_ranked_docs_with_snippets(query)

# def main():
#     query = 'A killer performance in Spanish'
#     start = time.time()
#     # 1) build the structure in mongo and redis
#     manager = StructureManager()
#     manager.build_all_structure()

#     # 2) get candidate resources
#     #engine = Engine()
#     #docs = engine.get_candidate_documents(query)
#     #print(docs)

#     done = time.time()
#     elapsed = done - start
#     print('Time elapsed: ' + str(elapsed))

# main()