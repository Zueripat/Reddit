import os
import requests
from time import time, sleep
from reddit.main import redditApi
import concurrent.futures

# On Error check Reddit API Status: https://www.redditstatus.com/ or the File which Failed

def redgifs(url):
    website = requests.get(url).text
    for element in website.split('"'):
        if element.endswith(".mp4") and not element.endswith("-mobile.mp4"): return [element]

def imgur_i_reddit(url):
    if url.endswith(".jpg") or url.endswith(".png") or url.endswith(".jpeg") or url.endswith(".gif"): return [url]
    else:
        website = requests.get(url).text
        for element in website.split('"'):
            if url.endswith("gifv"):
                if element.endswith(".mp4"): return [element]
            else:
                if element.endswith(".jpg"): return [element]

def filtering(url, __id, sub):
    if "redgifs.com" in url: return redgifs(url)
    if "i.imgur.com" in url or "i.redd.it" in url or "imgur.com/a" in url: return imgur_i_reddit(url)
    if "/gallery/" in url: return api.get_gallery(sub, __id)
    if "v.redd.it" in url: return api.get_vreddit(sub, __id)
    else: return [url]

api = redditApi("config.json")

def inputs(ampunt_in):
    subreddit = []
    amount = []
    mode = []
    dest = []

    for i in range(ampunt_in):
        while True:
            __dest = input("Destination folder: ")
            if os.path.isdir(__dest):
                dest.append(__dest)
                break
            else:
                print("Folder not found")
        while True:
            __subreddit = input("Subreddit: ")
            if api.subreddit_exists(__subreddit):
                subreddit.append(__subreddit)
                break
            else:
                print("Subreddit not found")
        while True:
            __amount = input("Amount of posts to download: ")
            try:
                int(__amount)
                amount.append(__amount)
                break
            except:
                print("Please enter a number")
        while True:
            __mode = input("Mode: ")
            if __mode == "hot" or __mode == "new" or __mode == "top" or __mode == "random" or __mode == "best":
                mode.append(__mode)
                break
            else:
                print("Please enter a valid mode")
    return dest, subreddit, amount, mode

def req(output, dest, subreddit):
    global success, fail, existing, count
    __id = list(output.keys())[0]
    __dic = output[__id]
    __url = filtering(__dic[list(__dic.keys())[0]], __id, subreddit)
    __name = str(list(__dic.keys())[0])
    for symbol in ["/", "\\", ":", "*", "?", '"', "<", ">", "|", "."]: __name = __name.replace(symbol, "-")
    fin_path = f"{dest}{'/' if not dest.endswith('/') else ''}{__name}.{str(__url).split('.')[-1]}"[:-2].split("?")[0]
    if not os.path.exists(fin_path):
        try:
            # print(f"[ {count}/{amount} ]: Getting Picture...", end=" ")
            picCount = 1
            for pic in __url:
                if len(__url) > 1:
                    open(f"{fin_path.split('.')[0]} ({picCount}).{fin_path.split('.')[1]}", "wb").write(requests.get(pic).content)
                    picCount += 1
                else:
                    open(fin_path, "wb").write(requests.get(pic).content)
                success += 1
            # print(__dic)
        except Exception as error:
            # print({'Error': error})
            fail += 1
    else:
        # print(f"[ {count}/{amount} ]: Getting Picture... { {'File already exists': __dic} }")
        existing += 1
    count += 1

def download(mode, amount, subreddit, dest):
    if mode == "random":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(api.request_random, subreddit) for _ in range(int(amount))]
            for f in concurrent.futures.as_completed(results):
                try:
                    req(f.result(), dest, subreddit)
                except Exception as err:
                    print(err)
    else:
        if int(amount) > 100: amount = 100
        for post in api.request_posts(subreddit, mode, int(amount)):
            req(post, dest, subreddit)


ampunt_inputs = input("Amount of diffrent inputs: ")
dests, subs, amounts, modes = inputs(int(ampunt_inputs))
__sleep = input("Sleep time (h): ")
# dests = []
# subs = []
# amounts = []
# modes = []
while True:
    for (dest, subb, amount, mode) in zip(dests, subs, amounts, modes):
        success, fail, existing, count = (0, 0, 0, 1)
        start = time()
        print(f"######################################\nDownloading {amount} posts from {subb} in {mode} mode to {dest}\n", end="")
        download(mode, amount, subb, dest)
        end = time()
        print(f"Finished after: {round(end - start, 2)} seconds\nTotal Pictures: {success+fail+existing}\nSuccess: {success}\nFail: {fail}\nExisting: {existing}\n######################################")
    print("Sleeping for 1h...\n")
    sleep(int(__sleep) * 3600) # Sleep for 1 hour
