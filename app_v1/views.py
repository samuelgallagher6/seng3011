from django.shortcuts import render
from django.http import HttpResponse
from app_v1.utilities.retrieve_json import apiRequest
from django.http import JsonResponse

import os, sys, re, urllib.request, json, datetime, time
from datetime import timedelta

# Create your views here.
def api_call(request):
    company_code = request.GET.get('id')
    date_of_interest = request.GET.get('date')
    return_type = request.GET.get('type')
    upper_window = request.GET.get('upper_window')
    lower_window = request.GET.get('lower_window')
    
    results = apiRequest(company_code, date_of_interest, return_type, upper_window, lower_window)
    
    return JsonResponse(results)
    
def index(request):
	# note: render renders template relative to "app_v1/templates" folder
	return render(request, "app_v1/index.html")