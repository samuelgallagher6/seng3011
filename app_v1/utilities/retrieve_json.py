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
    # grow from. If the date of interest is not valid, it doubles back
    # indefinitely until it reaches a valid date to copy initial values from
    
    # - CM_Return/AV_Return/Both_Returns
    # A flag for the output, whether it should return the cumulative return,
    # the average return, or both. Note that apiRequest calculates the cumulative
    # and average return regardless and whether it is given to the user should
    # be handled by the program using retrieve_json.py
    
    # - upper_window
    # In this code, it is defined as the number of days after the DateOfInterest
    # which the user wants to include in their search.
    
    # - lower_window
    # Defined as the number of days before the DateOfInterest which the user
    # wants to include in their search.
    
    # Potential pitfalls:
    # - The program is assumed to take in valid inputs. No defensive programming here
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
    url_end = "&apikey=9MLR16RAJZLF533S&outputsize=full" #compact/full
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
        
        while d.strftime("%Y-%m-%d") not in my_dict.get("Time Series (Daily)"):
            d = d - d_one
        
        last_price = my_dict.get("Time Series (Daily)").get(d.strftime("%Y-%m-%d")).get("4. close")
        
        inner_dict['date'] = d_lo.strftime("%Y-%m-%d")
        inner_dict['closing_price'] = last_price
        inner_dict['closing_price_adjusted'] = str( round(float( last_price ), 2) )
        inner_dict['return'] = "0.00"
        inner_dict['return_percentage'] = "0.00"
        inner_dict['relative_date'] = relative_date
        inner_dict['cumulative_return'] = "0.000000"
        inner_dict['average_return'] = "0.000000"
        
        results[d_lo.strftime("%Y-%m-%d")] = inner_dict
        
        d = d_lo + d_one
        relative_date = relative_date + 1
        
        days_passed = 1
        while (d != d_up+d_one):
            inner_dict = {}
            if d.strftime("%Y-%m-%d") not in my_dict.get("Time Series (Daily)"):
                inner_dict['closing_price'] = last_price
                inner_dict['closing_price_adjusted'] = str( round(float( last_price ), 2) )
                inner_dict['return'] = "0.00"
                inner_dict['return_percentage'] = "0.00"
            else:
                current_price = my_dict.get("Time Series (Daily)").get(d.strftime("%Y-%m-%d")).get("4. close")
                
                inner_dict['closing_price'] = current_price
                inner_dict['closing_price_adjusted'] = str( round(float( current_price ), 2) )
                inner_dict['return'] = str( round(round(float(current_price), 2) - round(float(last_price), 2), 2) ) 
                inner_dict['return_percentage'] = str(round( ((round(float(current_price), 2) / round(float(last_price), 2) - 1)*100), 2 ))
                
                last_price = current_price
            
                
            d_prev = d - d_one
            prev_cm = float(results.get(d_prev.strftime("%Y-%m-%d")).get("cumulative_return")) + 1
            return_ratio =  float(inner_dict.get('return_percentage')) / 100
            inner_dict['cumulative_return'] = str(round((prev_cm * (1 + return_ratio) - 1), 6))
            
            days_passed = days_passed + 1
            inner_dict['average_return'] = str(round((float(inner_dict['cumulative_return']) / days_passed), 6))
            
            inner_dict['date'] = d.strftime("%Y-%m-%d")
            inner_dict['relative_date'] = relative_date    
            results[d.strftime("%Y-%m-%d")] = inner_dict
            
            relative_date = relative_date + 1
            d = d + d_one
            
        return results

if __name__ == "__main__":
    results = apiRequest(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    
    # return results
    
    with open("output.json", "w") as f:
        json.dump(results, f, sort_keys = True, indent = 4, ensure_ascii = False)
    

    
