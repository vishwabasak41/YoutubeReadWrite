from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
import requests

def search(request):
    videos = []

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part' : 'snippet',
        'q' : 'kdramas',
        'key' : settings.YOUTUBE_KEY,
        'publishedAfter' : '2022-01-10T00:00:00Z',
        'pageInfo.resultsPerPage' : 20
    }

        

    # context = {
    #     'videos' : videos
    # }
    # print("CONTEXT found : ",context)
    r=requests.get(search_url,params=params)
    print("r=",r.text)
    return render(request, 'index.html')
