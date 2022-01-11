from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from elasticsearch import Elasticsearch
import json
# from datetime import datetime
import requests 
from datetime import datetime, timezone, timedelta
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

es=Elasticsearch("http://localhost:9200")
db_connection_str = 'mysql+pymysql://root:root@localhost/youtube_data'
db_connection = create_engine(db_connection_str)

df = pd.read_sql('SELECT * FROM Videos', con=db_connection)
print("df",df)

#line:
#Fetch youtube data after above date
#write to no-sql
#write to sql
#add 30 seconds to last_fetch_datetime
#goto line

def write():
    
    local_time = datetime.now(timezone.utc).astimezone() - timedelta(minutes=120)
    time=local_time.isoformat()
    print("TIME:",time)

    youtube_key='AIzaSyBKgW_UGx_U6XswobiA4iKWppXLn3uDmcI'
    
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
            'part' : 'snippet',
            'q' : 'kdramas',
            'key' : youtube_key,
            'publishedAfter' : time,
            'maxResults' : 50
        }
    r=requests.get(search_url,params=params)
    print("r text=",r.text)
    res = json.loads(r.text)

    #Writing to db for page 1
    result_set=[[item["id"]["videoId"],item["snippet"]["title"],item["snippet"]["description"],item["snippet"]["thumbnails"]["default"]["url"],item["snippet"]["publishedAt"].replace("T"," ").replace("Z","")] for item in res["items"] if item["id"]["kind"]=="youtube#video"]

    df=pd.DataFrame(result_set,columns=["videoId", "title", "description", "thumbnail","publishedat"])        
    df.to_sql("Videos",con=db_connection,if_exists="append",index=False)
    pno=1
    while "nextPageToken" in res:
        pno+=1
        print(pno,res["nextPageToken"])
        params = {
            'part' : 'snippet',
            'q' : 'cats',
            'key' : youtube_key,
            'publishedAfter' : time,
            'maxResults' : 50,
            'pageToken' : res["nextPageToken"]
        }
        r=requests.get(search_url,params=params)
        print("r text=",r.text)

        res = json.loads(r.text)
        
        #Writing to db for rest pages
        result_set=[[item["id"]["videoId"],item["snippet"]["title"],item["snippet"]["description"],item["snippet"]["thumbnails"]["default"]["url"],item["snippet"]["publishedAt"].replace("T"," ").replace("Z","")] for item in res["items"] if item["id"]["kind"]=="youtube#video"]

        df=pd.DataFrame(result_set,columns=["videoId", "title", "description", "thumbnail","publishedat"])        
        df.to_sql("Videos",con=db_connection,if_exists="append",index=False)

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="root",
#   database="youtube_data"
# )

# mycursor = mydb.cursor()
# mycursor.execute("SHOW DATABASES")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Videos(ID int NOT NULL AUTO_INCREMENT,videoId varchar(255) NOT NULL,title varchar(255),description varchar(255),thumbnail varchar(255),info_one varchar(255),info_two varchar(255),publishedat DATETIME,PRIMARY KEY (ID));")


# for x in mycursor:
#     print("DATABASE=",x)



sched = BackgroundScheduler(daemon=True)
sched.add_job(write,'interval',seconds=20)  
sched.start()
    
app = Flask(__name__)

@app.route("/")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"

if __name__ == "_main_":
    app.run()

