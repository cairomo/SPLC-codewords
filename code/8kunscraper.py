from selenium import webdriver

# create webdriver with incognito window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome('/Users/arushigupta/chromedriver', options=chrome_options)

# number of pages of posts in /pnd/
NUM_PAGES = 25
BASE_DIR = './8kun_corpus/'


# for a page of posts, get all the threads and add thread id to thread_nos
def get_page_threads(page_url, file):
    driver.get(page_url)
    threads = driver.find_elements_by_class_name("thread")
    for thread in threads:
        print("reading element " + thread.get_property("id"))
        file.write((thread.get_property("id"))[7:] + "\n")

# goes through each page of posts
def get_all_thread_nos():
    thread_nos = open(BASE_DIR + "all_thread_nos.txt", "w")

    print("scraping page 1...")
    get_page_threads('https://8kun.top/pnd/index.html', thread_nos)
    print("finished page 1")

    for i in range(2, NUM_PAGES + 1):
        print("scraping page " + str(i) + "...")
        get_page_threads("https://8kun.top/pnd/" + str(i) + ".html", thread_nos)
        print("finished page " + str(i))

    thread_nos.close()

# goes to the url for a certain thread id and writes the thread contents to a file
def scrape_thread(num):
    f = open(BASE_DIR + num + ".txt", "w")
    driver.get("https://8kun.top/pnd/res/" + num + ".html")

    op = driver.find_element_by_id("op_" + num)
    print("reading op")
    f.write(op.find_element_by_class_name("body").text)
    f.write("\n\n\n")

    replies = driver.find_elements_by_css_selector("p.body-line.ltr")
    print("reading " + str(len(replies)) + " replies")
    for reply in replies:
        text = reply.text
        if (len(text) > 1) & (text[:2] != ">>"):
            f.write(reply.text)
            f.write("\n\n")

    f.close()
    completed.write(num + "\n")


# creates a file with all the thread numbers
get_all_thread_nos()

# writes the thread number that were scraped successfully to this file
completed = open(BASE_DIR + "completed_thread_nos.txt", "a")
# reads the thread numbers in this file
thread_nos = open(BASE_DIR + "thread_nos.txt", "r")
for thread_no in thread_nos.readlines():
    print("scraping thread " + thread_no[:-1] + "...")
    scrape_thread(thread_no[:-1])
    print("finished thread " + thread_no[:-1])

driver.quit()
