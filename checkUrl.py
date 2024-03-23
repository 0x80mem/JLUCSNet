import time
visited_pages = set()


def findGotted(url):
    if url in visited_pages:
        print("此页面已经访问过")
        time.sleep(5)
        return -1
    else:
        return 1


def addGotted(url):
    visited_pages.add(url)


def clearGotted():
    visited_pages.clear()
