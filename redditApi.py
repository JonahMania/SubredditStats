import requests
import socket

REDDIT_URL = "www.reddit.com"
BLACK_LIST = {
    "and", "the", "a",
    "to", "in", "of",
    "for", "with", "i",
    "on", "from", "at",
    "so", "this"
}

"""
def getJSON(url):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((REDDIT_URL, 80))
    request = b"GET " + url.encode() + b" HTTPS/1.1\nHost: " + REDDIT_URL.encode() + b"\n\n"
    print(request)
    s.send(request)
    response = s.recv(1000)
    s.close()
    return response
"""

def getCommentText(url):
    text = []
    response = requests.get("https://" + REDDIT_URL + url + ".json", headers = {'User-agent': 'subredditstats 0.0'})

    data = response.json()

    if "error" in data:
        print("Error " + str(data["error"]) + ": " + data["message"])
        return []


    for x in data:
        for comment in x["data"]["children"]:
            if "body" in comment["data"]:
                text.append(comment["data"]["body"])

    return text

def getSubreddit(subreddit):
    response = requests.get("https://" + REDDIT_URL + "/r/" + subreddit + "/top/.json?count=40?t=day", headers = {'User-agent': 'subredditstats 0.0'})
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
            if word in BLACK_LIST:
                continue
            if word in commonWords:
                commonWords[word] += 1
            else:
                commonWords[word] = 1
    topWords = [(key, commonWords[key]) for key in commonWords]
    topWords = sorted(topWords, key=lambda x: x[1], reverse=True)
    return topWords[:20]
