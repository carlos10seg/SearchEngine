
def read_csv_as_file():
    with open("../data/wikipedia_text_files.csv") as fp:
        line = fp.readline()
        cnt = 1
        while line:
        print("Line {}: {}".format(cnt, str(line)))
        line = fp.readline()
        cnt += 1
        if cnt >= 50:
            break

def read_csv_and_save():
    with open("../data/wikipedia_text_files.csv") as fp:
        line = fp.readline()
        cnt = 1
        while line:
        print("Line {}: {}".format(cnt, line.strip()))
        line = fp.readline()
        cnt += 1
        if cnt >= 50:
            break

read_csv_as_file()