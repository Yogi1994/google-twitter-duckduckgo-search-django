# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse

def index(request):
    response_data = {}
    response_data['result'] = 'error'
    response_data['message'] = 'Some error message'
    query_string = request.GET["q"]
    # return HttpResponse("Hello, world. You're at the polls index.")
    url ='https://www.googleapis.com/customsearch/v1?key=AIzaSyAk_2v_7k4EAG6j4oe-UExvBCSFXm2U0j4&cx=017576662512468239146:omuauf_lfve&q=' + query_string
    response = requests.get(url)
    return JsonResponse({'foo':'bar', 'res':response.json()})