import requests
import socket
from stopWords import STOP_WORDS

REDDIT_URL = "www.reddit.com"
NUM_POSTS = 32
TOP_OF = "day"

def recursiveGetComments(json):
    ret = []

    if json == "":
        return []
    for comment in json["data"]["children"]:
        if not("body" in comment["data"]):
            continue
        ret.append(comment["data"]["body"])
        ret.extend(recursiveGetComments(comment["data"]["replies"]))
    return ret

def getCommentText(url):
    text = []
    response = requests.get("https://" + REDDIT_URL + url + ".json", headers = {'User-agent': 'subredditstats 0.0'})
    data = response.json()

    if "error" in data:
        print("Error " + str(data["error"]) + ": " + data["message"])
        return []

    for x in data:
        text.extend(recursiveGetComments(x))

    return text

def getSubreddit(subreddit):
    response = requests.get("https://" + REDDIT_URL + "/r/" + subreddit + "/top/.json?count="+ str(NUM_POSTS) +"?t=" + TOP_OF, headers = {'User-agent': 'subredditstats 0.0'})
    data = response.json()
    ret = []
    if "error" in data:
        print("Error " + str(data["error"]) + ": " + data["message"])
        return []

    #Get comments link from each post and exctract the comment text
    for post in data["data"]["children"]:
        ret.extend(getCommentText(post["data"]["permalink"]))

    return ret

def getTopWords(subreddit):
    commonWords = {}
    subRedditPosts = getSubreddit(subreddit)
    for text in subRedditPosts:
        for word in text.split(" "):
            word = word.lower()
            if word in STOP_WORDS or len(word) < 2:
                continue
            if word in commonWords:
                commonWords[word] += 1
            else:
                commonWords[word] = 1
    topWords = [(key, commonWords[key]) for key in commonWords]
    topWords = sorted(topWords, key=lambda x: x[1], reverse=True)
    return topWords[:20]
