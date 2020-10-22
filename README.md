# QuantaVerse
Shared QV repo 
Ok, I did a few things.

1. Mongodb database is set up so everyone can see it I think. Info is:
host: host.trevor.gg
port: 27018
user: quantaverse
pass: capstone

2. set up a website so you can see what is in the database if you are not very familiar with the mongodb commands like me. View at: qv-mongo.trevor.gg
user and pass are same as above

3. Made a spring app to make a rest api for the database, it is in the database-service repo in our github org. Right now it only has endpoints for adding articles and searching all of the articles. I plan on hosting this also and making it auto update with the repo but for now you can just run it yourself if you need.

4. made a program to parse the html files he gave us and put the fields inside of the database. This is the database-populator repo in the github org. It assumes you are locally hosting the database-service program for now.
