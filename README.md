Hi,

This project has been directed towards the creation of system where:-

1.We are querying the Youtube API every 1 minute to retrieve latest data currently related to 'cricket'
2.Serving a web application where the users will be able to view all the videos and will be able to search on them based on any phrases.

Initial insights from the requirement-

My initial approach comprised of building a django application which will have MySQL as the database and i can handle the read/write on the same server.
But i could see this to be a design issue as if i have multiple users hitting my website trying to read data and if my database starts writing at the same time it will cause an availibility issue.
Also, this requirement meant the data will keep growing with time and that needs to be handled while reading too.

Method Adopted-

Keeping in mind the above points i designed the following architecture-

1. A flask application with the specific purpose of writing onto the database and is unrelated to my reading django webapp.
2. A django application which will facilitate :
        - Viewing all videos by latest published date
        - Searching within the results
3. I initially used Mysql, but had to replace it since it was not an optimal selection to search within the dataset and the size of the dataset will cause delays moving further.
4. To optimise the searching within the database i implemented elasticsearch and replaced MySQL as it will be easy to phrase search on top of it and the reading will also be optimised.
5.Another place for optimisation was the way the full text search was performed,so i created a flow where used stored title+description, id and date in elastic search and queried on it to get relevant video-ids and used extracted videos-ids to get all data from MySql tables. Although this led to faster searches but increased response time so decided to use only elasticsearch for generating response to the user.
6. And to optimise the reading the website serves all results by page which means - you see the latest data always but in sets of 10 at a time and the data for next 10 videos is only queried once the user clicks on next page option. So only the data supposed to be shown to user reamins inmemory and on next page selection next batch of data is fetched thus making it scalable.
