BASE_DIR = "./8kun_corpus/"

thread_nos = open(BASE_DIR + "all_thread_nos.txt", "r")
corpus = open(BASE_DIR + "all_threads.txt", "w")

for thread_no in thread_nos:
    print("reading thread " + thread_no)
    f = open(BASE_DIR + thread_no[:-1] + ".txt", "r")
    corpus.write(f.read())
    print("finished writing thread " + thread_no)
    f.close()