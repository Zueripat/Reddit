import json
import requests.auth

class redditApi:
    def __init__(self, config_filename):
        with open(config_filename, "r") as cf:
            self.__data = json.load(cf)["reddit"]
            self.__auth = requests.auth.HTTPBasicAuth(self.__data["client_id"], self.__data["secret"])
            self.__data = {'grant_type': 'password','username': self.__data["username"],'password': self.__data["password"]}
            self.__headers_old = {'User-Agent': 'MyBot/0.0.1'}
            try: self.__res = requests.post('https://www.reddit.com/api/v1/access_token', auth=self.__auth, data=self.__data, headers=self.__headers_old)
            except Exception as error_1: print(f"Error Occured: {error_1}")
            self.__token = self.__res.json()['access_token']
            self.__headers = {**self.__headers_old, **{'Authorization': f"bearer {self.__token}"}}

    def request_posts(self, subreddit, mode, limit=25):
        __request = requests.get(f'https://oauth.reddit.com/r/{subreddit}/{mode}', headers=self.__headers, params={"limit": limit}).json()
        return [{post["data"]["id"]: {post["data"]["title"]: post["data"]["url"]}} for post in __request["data"]["children"]]

    def request_random(self, subreddit):
        __request = requests.get(f'https://oauth.reddit.com/r/{subreddit}/random', headers=self.__headers,).json()
        return [{post["data"]["id"]: {post["data"]["title"]: post["data"]["url"]}} for post in __request[0]["data"]["children"]][0]

    def subreddit_exists(self, subreddit):
        __request = requests.get(f'https://oauth.reddit.com/r/{subreddit}/about', headers=self.__headers).json()
        return __request["kind"] == "t5"

    def get_url(self, subreddit, post_id):
        __request = requests.get(f'https://oauth.reddit.com/r/{subreddit}/comments/{post_id}', headers=self.__headers).json()
        return [{post["data"]["id"]: {post["data"]["title"]: post["data"]["url"]}} for post in __request[0]["data"]["children"]][0]

    def get_gallery(self, subreddit, post_id):
        __request = requests.get(f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json", headers=self.__headers_old).json()
        try:
            posts = [posts["data"]["media_metadata"] for posts in __request[0]["data"]["children"]][0]
            return [posts[post]["p"][-1:][0]["u"].replace("preview.redd.it", "i.redd.it") for post in posts]
        except Exception as err: return err

    def get_vreddit(self, subreddit, post_id):
        __request = requests.get(f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json", headers=self.__headers_old).json()
        posts = [posts["data"] for posts in __request[0]["data"]["children"]][0]
        try: return [posts["secure_media"]["reddit_video"]["fallback_url"]]
        except Exception as err: return err