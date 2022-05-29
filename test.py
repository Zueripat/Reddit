import os
import requests
from time import time
from reddit.main import redditApi
import concurrent.futures

def redgifs(url):
    website = requests.get(url).content.decode()
    for element in website.split('"'):
        if element.endswith(".mp4") and not element.endswith("-mobile.mp4"): return element

def imgur_i_reddit(url):
    if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".gif"): return url
    else:
        website = requests.get(url).content.decode()
        for element in website.split('"'):
            if element.endswith(".jpg"): return element

def filtering(url):
    if "redgifs.com" in url: return redgifs(url)
    if "i.imgur.com" in url or "i.redd.it" in url or "imgur.com/a" in url: return imgur_i_reddit(url)
    else: return url

def req(output):
    global success, fail, existing, count
    __id = list(output.keys())[0]
    __dic = output[__id]
    __url = filtering(__dic[list(__dic.keys())[0]])
    __name = str(list(__dic.keys())[0])
    for symbol in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]: __name = __name.replace(symbol, "-")
    fin_path = f"{dest}{'/' if not dest.endswith('/') else ''}{__name}.{str(__url).split('.')[-1]}"
    if not os.path.exists(fin_path):
        try:
            # print(f"[ {count}/{amount} ]: Getting Picture...", end=" ")
            open(fin_path, "wb").write(requests.get(__url).content)
            success += 1
            # print(__dic)
        except Exception as err:
            # print({'Error': {__url: err}}, __id)
            fail += 1
    else:
        # print(f"[ {count}/{amount} ]: Getting Picture... { {'File already exists': __dic} }")
        existing += 1
    count += 1

api = redditApi("config.json")
inputChoice = ""

while True:
    dest = input("Destination folder: ")
    if os.path.isdir(dest): break
    else: print("Folder not found")
while inputChoice != "x":
    success, fail, existing, count = (0, 0, 0, 1)
    while True:
        subreddit = input("Subreddit: ")
        if api.subreddit_exists(subreddit): break
        else: print("Subreddit not found")
    while True:
        amount = input("Amount of posts to download: ")
        try:
            int(amount)
            break
        except: print("Please enter a number")
    while True:
        mode = input("Mode: ")
        if mode == "hot" or mode == "new" or mode == "top" or mode == "random" or mode == "best": break
        else: print("Please enter a valid mode")

    print(f"-----------------------------------\nExpected Runtime ~{float(amount)*0.15}s - {float(amount)*0.40}s with 50% of pictures being successfully downloaded...")
    start = time()
    if mode == "random":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(api.request_random, subreddit) for _ in range(int(amount))]
            for f in concurrent.futures.as_completed(results):
                req(f.result())
    else:
        if int(amount) > 100: amount = 100
        for post in api.request_posts(subreddit, mode, int(amount)):
            req(post)
    end = time()
    print(f"-----------------------------------\n"
              f"Total Pictures: {fail + success + existing}/{amount}\n"
              f"Successful: {success}\n"
              f"Failed: {fail}\n"
              f"Existing: {existing}\n"
              f"Total Time: {round((end - start), 2)} seconds\n"
              f"Average Time: {round(((end - start) / (fail + success + existing)), 2)} seconds\n"
              f"-----------------------------------")
   
