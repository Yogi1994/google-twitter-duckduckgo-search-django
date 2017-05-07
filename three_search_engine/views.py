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

def index(request):
    response_data = {}
    response_data['result'] = 'error'
    response_data['message'] = 'Some error message'
    query_string = request.GET["q"]
    # response['google']  = 
    # return HttpResponse("Hello, world. You're at the polls index.")

    url ='https://www.googleapis.com/customsearch/v1?key=AIzaSyAk_2v_7k4EAG6j4oe-UExvBCSFXm2U0j4&cx=017576662512468239146:omuauf_lfve&q=' + query_string
    response = requests.get(url)
    response = response.json()
    res_google = {}
    res_google['text'] = response['items'][0]['title']
    res_google['url'] = response['items'][0]['link']
    google={}
    google['google'] = res_google

    url2 = 'http://api.duckduckgo.com/?q=' + query_string + '&format=json'
    response = requests.get(url2)
    response = response.json()
    res_ddg = {}
    if(response['RelatedTopics'].length()):
        res_ddg['text'] = response['RelatedTopics'][0]['Text']
        res_ddg['url'] = response['RelatedTopics'][0]['FirstURL']
    duckduckgo = {}
    duckduckgo['duckduckgo'] =  res_ddg


    CONSUMER_KEY = "MJmhSwcLw5OEvf3Yj5VbIEUBS"
    CONSUMER_SECRET = "6udAiQT0I6QK2sjkcRABy8Z1cxAtE6RaneU0jOpC3lkYNP5y03"
    ACCESS_KEY = "211807118-LIhgcDErkXzgBxLDFuIYMVIUv3YqVrCxDb2UImS2"
    ACCESS_SECRET = "orcuKd13ZSBLPuPwwlHgU9Kyk9IxWEZQda7E3WWEWlF9E"

    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    url ='https://api.twitter.com/1.1/search/tweets.json?count=10&q=' + query_string
    response, data = client.request(url)

    tweets = json.loads(data)
    
    res_twitter = {}
    if(tweets['statuses'].length()):
        res_twitter['text'] = tweets['statuses'][0]['text']
        res_twitter['url'] = tweets['statuses'][0]['entities']['urls']
    twitter={}
    twitter['twitter'] = res_twitter



    
    return JsonResponse({'google':google, 'duckduckgo':duckduckgo, 'twitter':res_twitter})
#     GET /1.1/search/tweets.json?q=modi&oauth_consumer_key=MJmhSwcLw5OEvf3Yj5VbIEUBS&oauth_token=211807118-LIhgcDErkXzgBxLDFuIYMVIUv3YqVrCxDb2UImS2&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1494170872&oauth_nonce=1568847899&oauth_version=1.0&oauth_signature=3XjLtUpuL4J6+mk3km6fnIw/BOk= HTTP/1.1
# Host: api.twitter.com
# Authorization: OAuth oauth_consumer_key="MJmhSwcLw5OEvf3Yj5VbIEUBS",oauth_token="211807118-LIhgcDErkXzgBxLDFuIYMVIUv3YqVrCxDb2UImS2",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1494173377",oauth_nonce="WEiBpZKtREW",oauth_version="1.0",oauth_signature="Xd%2FyBGHpNtSnvVMAV5qBNEOqK18%3D"
# Cache-Control: no-cache
# Postman-Token: 9265e5ec-27ab-e135-4534-ab27fc5d3ad7
 