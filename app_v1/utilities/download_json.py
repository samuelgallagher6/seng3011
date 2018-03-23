#!/usr/bin/env python

import os, sys, re, urllib.request

# Usage: 
    # python retrieve_json.py BHP

if __name__ == "__main__":
    filename = sys.argv[1]
    filename = "".join((filename, ".json"))
    
    url_start = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="
    url_end = "&apikey=9MLR16RAJZLF533S&outputsize=full" # can replace full with compact
    url = "".join( (url_start, sys.argv[1], url_end) )
    
    urllib.request.urlretrieve(url, filename)