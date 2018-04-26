#!/usr/bin/python3
import sys
import getopt
from redditApi import getTopWords

def main(argv):
    if len(argv) < 1:
        print("Usage: ./main [subreddit]")
        return;
    topWords = getTopWords(argv[0])
    for word in topWords:
        print(word[0] + ", " + str(word[1]))

if __name__ == "__main__":
    main(sys.argv[1:])
