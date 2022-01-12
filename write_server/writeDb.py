from elasticsearch import Elasticsearch
from datetime import datetime
import requests 


#line:
    #Fetch youtube data after above date
    #write to no-sql
    #write to sql
    #add 30 seconds to last_fetch_datetime
    #goto line
# 2022-01-10T00:00:00Z
now=datetime.now()

print("now is=",now.strftime("%Y-%m-%dT%H:%M:%SZ"))

youtube_key='AIzaSyDbZIkRRtwYryt7whtsQUHIkSOnyoK5vU4'


search_url = 'https://www.googleapis.com/youtube/v3/search'
params = {
        'part' : 'snippet',
        'q' : 'kdramas',
        'key' : youtube_key,
        'publishedAfter' : now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        'pageInfo.resultsPerPage' : 20
    }
r=requests.get(search_url,params=params)
print("r=",r.text)



