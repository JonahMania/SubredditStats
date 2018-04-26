import requests

REDDIT_URL = "https://www.reddit.com"
BLACK_LIST = {
    "and", "the", "a",
    "to", "in", "of",
    "for", "with", "i",
    "on", "from", "at",
    "so", "this"
}

def getSubreddit(subreddit):
    response = requests.get(REDDIT_URL + "/r/" + subreddit + "/top/.json?count=40", headers = {'User-agent': 'subredditstats 0.0'})
    data = response.json()
    if "error" in data:
        print("Error " + str(data["error"]) + ": " + data["message"])
        return []

    dataText = [x["data"]["title"] for x in data["data"]["children"]]
    return dataText

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
