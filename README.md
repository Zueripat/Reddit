# Reddit API

Reddit API is a Python Class, that lets you easely establish a connection to the Reddit Api. The idea behind this is to dowload Images, Animated Images and Videos from Reddit Posts.

The script `test.py` is a Script which you can use to test out the functions of the redditApi Class

## Features
`request_posts` This Function within the redditApi class lets you get between 1 and 100 posts from any subreddit and returns a list of Dictionaries, which contain the Post ID, Image url and Post Title.

`request_random` This Function within the redditApi class lets you get a random Post from any subreddit and returns a list of one Dictionary, which contain the Post ID, Image url and Post Title.

`subreddit_exists` This Function checks if a given Subreddit exists

`get_url` This Function within the redditApi class lets you get a the Image url from any specific Post and returns a list of one Dictionary, which contain the Post ID, Image url and Post Title.

`get_header` Return you the Header Information for you to make further Requests


## Setup

Steps you need to complete before you can use these Scripts


### Config File

`username` Your Reddit Account Username

`password` Your Reddit Account Password

`client_id` The Application ID of your Reddit Application

`secret` The Secret of your Reddit Apllication

`Reddit Application` Create your own Reddit Application on the following Website: https://www.reddit.com/prefs/apps

![asasfasrf](https://user-images.githubusercontent.com/66902977/170887501-f81612be-d05e-41c9-8d65-d7650061aa44.PNG)


### Python Libraries

When Installing Python 3.10.4 most of the Modules used in this Script will be pre Installed

`requests` Download the requests module using the command: `pip install requests` in the console
