#!/usr/bin/python
import sys
import getopt
from redditApi import getTopWords

def main(argv):
    if len(argv) < 1:
        print("Usage")
        return;
    print(getTopWords(argv[0]))

if __name__ == "__main__":
    main(sys.argv[1:])
