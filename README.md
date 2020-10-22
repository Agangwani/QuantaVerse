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
AMAN::::

So to install Kafka locally you need openJDK 1.8 and Zookeeper which is an apache service To intsall this on macbooks i used
brew cask install homebrew/cask-versions/adoptopenjdk8           
brew install kafka 

To run zookeeper:

brew services start zookeeper
brew services start kafka 

create a test topic: 
 kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test

put messages in the topic 
kafka-console-producer --broker-list localhost:9092 --topic test
> insert some messages here 

Read the messages in the topic
kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning

Now that we understand how exactly it works lets start working on getting python-kafka working so everything runs through the python script 
First run
pip install kafka-python


