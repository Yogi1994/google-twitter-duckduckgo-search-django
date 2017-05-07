# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import time
import oauth2 as oauth
import threading

def google_request(query_string, result):
    google_url ='https://www.googleapis.com/customsearch/v1?key=AIzaSyAk_2v_7k4EAG6j4oe-UExvBCSFXm2U0j4&cx=017576662512468239146:omuauf_lfve&q=' + query_string

    google_response = requests.get(google_url)
    
    google_response = google_response.json()
    print google_response
    res_google = {}
    if(len(google_response['items'])):
        res_google['text'] = google_response['items'][0]['title']
        res_google['url'] = google_response['items'][0]['link']
    
    result['google'] = res_google


def duckduckgo_request(query_string, result):
    duckduckgo_url = 'http://api.duckduckgo.com/?q=' + query_string + '&format=json'

    duckduckgo_response = requests.get(duckduckgo_url)
    duckduckgo_response = duckduckgo_response.json()
    res_ddg = {}
    if(len(duckduckgo_response['RelatedTopics'])):
        res_ddg['text'] = duckduckgo_response['RelatedTopics'][0]['Text']
        res_ddg['url'] = duckduckgo_response['RelatedTopics'][0]['FirstURL']
    # duckduckgo = {}
    # duckduckgo['duckduckgo'] =  res_ddg
    result['duckduckgo'] = res_ddg

def twitter_request(query_string, result):
    twitter_url ='https://api.twitter.com/1.1/search/tweets.json?count=1&q=' + query_string

    CONSUMER_KEY = "MJmhSwcLw5OEvf3Yj5VbIEUBS"
    CONSUMER_SECRET = "6udAiQT0I6QK2sjkcRABy8Z1cxAtE6RaneU0jOpC3lkYNP5y03"
    ACCESS_KEY = "211807118-LIhgcDErkXzgBxLDFuIYMVIUv3YqVrCxDb2UImS2"
    ACCESS_SECRET = "orcuKd13ZSBLPuPwwlHgU9Kyk9IxWEZQda7E3WWEWlF9E"

    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    
    twitter_response, data = client.request(twitter_url)

    tweets = json.loads(data)
    
    res_twitter = {}
    if(len(tweets['statuses'])):
        res_twitter['text'] = tweets['statuses'][0]['text']
        res_twitter['url'] = tweets['statuses'][0]['entities']['urls']

    result['twitter'] = res_twitter


def index(request):

    query_string = request.GET["q"]
    jobs = []
    result = {}
    
    thread = threading.Thread(target=google_request(query_string, result))
    jobs.append(thread)
    thread = threading.Thread(target=duckduckgo_request(query_string, result))
    jobs.append(thread)
    thread = threading.Thread(target=twitter_request(query_string, result))
    jobs.append(thread)
    


    # Start the threads (i.e. calculate the random number lists)
    for j in jobs:
        j.start()

    # Ensure all of the threads have finished
    for j in jobs:
        j.join()

    return JsonResponse(result)
#     GET /1.1/search/tweets.json?q=modi&oauth_consumer_key=MJmhSwcLw5OEvf3Yj5VbIEUBS&oauth_token=211807118-LIhgcDErkXzgBxLDFuIYMVIUv3YqVrCxDb2UImS2&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1494170872&oauth_nonce=1568847899&oauth_version=1.0&oauth_signature=3XjLtUpuL4J6+mk3km6fnIw/BOk= HTTP/1.1
# Host: api.twitter.com
# Authorization: OAuth oauth_consumer_key="MJmhSwcLw5OEvf3Yj5VbIEUBS",oauth_token="211807118-LIhgcDErkXzgBxLDFuIYMVIUv3YqVrCxDb2UImS2",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1494173377",oauth_nonce="WEiBpZKtREW",oauth_version="1.0",oauth_signature="Xd%2FyBGHpNtSnvVMAV5qBNEOqK18%3D"
# Cache-Control: no-cache
# Postman-Token: 9265e5ec-27ab-e135-4534-ab27fc5d3ad7
 