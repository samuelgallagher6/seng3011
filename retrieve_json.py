#!/usr/bin/env python

import os, sys, re, urllib.request, json, datetime, time
from datetime import timedelta

# The method apiRequest takes in 5 different variables:
    # - InstrumentID
    # This is a code that designates the company. Usually of the format ABC.YZ
    # where ABC is the company code and YZ denotes the stock exchange code. It
    # may be encountered in the format ABC
    # - DateOfInterest
    # Presented as 10 character string in the format YYYY-MM-DD, this
    # designates the particular day in which the upper and lower windows must
    # grow from.
    # - CM_Return/AV_Return/Both_Returns
    # A flag for the output, whether it should return the cumulative return,
    # the average return, or both. Encountered as an integer (0/1/2)
    # - upper_window
    # In this code, it is defined as the number of days after the DateOfInterest
    # which the user wants to include in their search.
    # - lower_window
    # Defined as the number of days before the DateOfInterest which the user
    # wants to include in their search.
    
    # Potential pitfalls:
    # - InstrumentID may not be valid
    # - DateOfInterest may not be a real date
    # - DateOfInterest may not be a trading date
    # - windows must be non-negative
    
# apiRequest returns results - a dictionary with the primary key being date.
    # The key corresponds to an inner dictionary which contains several key-value pairs.
    
    # date
    # closing price
    # closing price adjusted - bankers rounding to 2 decimal points
    # return - bankers rounding to 2 decimal points
    # return percentage - bankers rounding to 2 decimal points
    # relative date - in perspective to the date of interest
    
def apiRequest(instrument_id, date_of_interest, return_code, upper_window, lower_window):
    url_start = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="
    url_end = "&apikey=9MLR16RAJZLF533S&outputsize=compact" #compact/full
    url = "".join( (url_start, instrument_id, url_end) )
    
    year, month, day = date_of_interest.split("-")
    d_now = datetime.datetime(int(year), int(month), int(day))
    d_up = d_now+timedelta(days=int(upper_window))
    d_lo = d_now-timedelta(days=int(lower_window))
    d_one = timedelta(days=1)
    
    # Replace the below two lines with the below lines marked at the end with ###
    # if you want to read from local input. Replace 'output.json' with the proper file
    
    # with open('output.json', 'r') as f:
        # my_dict = json.load(f)
        
    with urllib.request.urlopen(url) as f: ###
        my_dict = json.loads(f.read().decode('utf-8')) ###
        results = {}
        
        d = d_lo
        inner_dict = {}
        relative_date = -int(lower_window)
        
        last_price = my_dict.get("Time Series (Daily)").get(d.strftime("%Y-%m-%d")).get("4. close")
        
        inner_dict['date'] = d.strftime("%Y-%m-%d")
        inner_dict['closing_price'] = last_price
        inner_dict['closing_price_adjusted'] = str( round(float( last_price ), 2) )
        inner_dict['return'] = "0.00"
        inner_dict['return_percentage'] = "0.00"
        inner_dict['relative_date'] = relative_date
        
        results[d.strftime("%Y-%m-%d")] = inner_dict
        
        d = d + d_one
        relative_date = relative_date + 1
        
        while (d != d_up+d_one):
            inner_dict = {}
            if (my_dict.get("Time Series (Daily)").get(d.strftime("%Y-%m-%d")) == None ):
                inner_dict['closing_price'] = last_price
                inner_dict['closing_price_adjusted'] = str( round(float( last_price ), 2) )
                inner_dict['return'] = "0.00"
                inner_dict['return_percentage'] = "0.00"
                
            else:
                current_price = my_dict.get("Time Series (Daily)").get(d.strftime("%Y-%m-%d")).get("4. close")
                
                inner_dict['closing_price'] = current_price
                inner_dict['closing_price_adjusted'] = str( round(float( current_price ), 2) )
                inner_dict['return'] = str( round(round(float(current_price), 2) - round(float(last_price), 2), 2) ) 
                inner_dict['return_percentage'] = str(round( ((round(float(current_price), 2) / round(float(last_price), 2) - 1)/100), 2 ))
                
                last_price = current_price
            
            inner_dict['date'] = d.strftime("%Y-%m-%d")
            inner_dict['relative_date'] = relative_date    
            results[d.strftime("%Y-%m-%d")] = inner_dict
            
            relative_date = relative_date + 1
            d = d + d_one
        return results
      
# The method calculateReturns takes on only one value - the dictionary of dictionaries created from apiRequest.
    # It calculates the cumulative return and average return for each date, then
    # it appends these values to the keys "cumulative_return" and "average_return"
    # inside the inner dictionary.
    
def calculateReturns(outer_dictionary):
    # TODO
    return outer_dictionary

if __name__ == "__main__":
    results = apiRequest(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    calculateReturns(results)
    
    # return results
    
    with open("output.json", "w") as f:
        json.dump(results, f, sort_keys = True, indent = 4, ensure_ascii = False)
    

    
