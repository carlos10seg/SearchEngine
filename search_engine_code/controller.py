import time
from structure_manager import StructureManager
from engine import Engine

def main():
    query = 'too far'
    start = time.time()
    # 1) build the structure in mongo and redis
    manager = StructureManager()
    manager.build_index_from_csv()

    # 2) get candidate resources
    # engine = Engine()
    # docs = engine.get_candidate_documents()
    # print(docs)

    done = time.time()
    elapsed = done - start
    print('Time elapsed: ' + str(elapsed))

main()