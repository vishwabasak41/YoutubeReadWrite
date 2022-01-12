from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
import requests
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from videos_app.models import Videos
from elasticsearch import Elasticsearch

es=Elasticsearch()
query = ''
pno = 0

def search(request):
    print("ELASTIC SEARCH indices are:-",es.indices.get_alias("*"))
    global query,pno
    if request.method=="POST":
        search_value=request.POST.get("search_value")
        query=search_value
        pno=0
    elif request.method=="GET":
        pno+=1
    
    print("search_value",pno,query)
    
    # videos=currentchunk=100000
    #OnlyESread
    data_fetch = es.search(
        index="completedataindex",
        body={
            "from":pno*10,
            "size":10,
            "sort":[{"publishedat":{"order":"desc"}}],
            "query":{
                "multi_match":{
                    "query":query,
                    "fields":["title","description"]
                }
            }
        }
        #sort={"publishedat":{"order":"desc"}}
        )
    #ESSQLread
    data_fetch2 = es.search(
        index="idindex",
        body={
            "from":pno*10,
            "size":10,
            "query":{
                "match":{
                    "text":query
                }
            }
        },
        sort={"publishedat":{"order":"desc"}}
    )
    videos=[item['_source'] for item in data_fetch['hits']['hits']]
    #videos = Videos.objects.all().order_by('-publishedat')
    print("total videos found=",len(videos))
    # print(videos)  
    page=request.GET.get('page',1)
    paginator = Paginator(videos, 12)
    
    try:
        #run for
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'index.html', { 'videos': videos })

def results(request):
    if request.method=="POST":
        search_value=request.POST.get("search_value")
        print("SEARCH VALUE FOUND=",search_value)
        return HttpResponse("Value is : ",search_value)
