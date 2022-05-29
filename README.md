# Reddit API

Reddit API is a Python Class, that lets you easely establish a connection to the Reddit Api. The idea behind this is to dowload Images, Animated Images and Videos from Reddit Posts.

## Features
`request_posts` This Function within the redditApi class lets you get between 1 and 100 posts from any subreddit and returns a list of Dictionaries, which contain the Post ID, Image url and Post Title.

`request_random` This Function within the redditApi class lets you get a random Post from any subreddit and returns a list of one Dictionary, which contain the Post ID, Image url and Post Title.

`subreddit_exists` This Function checks if a given Subreddit exists

`get_url` This Function within the redditApi class lets you get a the Image url from any specific Post and returns a list of one Dictionary, which contain the Post ID, Image url and Post Title.

`get_header` Return you the Header Information for you to make further Requests
