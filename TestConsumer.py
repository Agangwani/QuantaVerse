from kafka import KafkaConsumer

from kafka import KafkaProducer
import json
import ast

def send_to_broker(data):
	pass

def main():
	consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])
	#producer = KafkaProducer(bootstrap_servers='localhost:9092')
	myarr = [6,7,8,9,10]
	#for element in consumer:
		#print(element)
	#break this into 2 scripts
	#one for consumer, one for producer

	value = next(consumer)
	print("\n ###### First all this garbage in the consumer ###### \n")
	print(value)
	print("\n ###### Next the Value b{dict} ######\n" )
	print(value.value)
	print("\n##### Now let's get the type for this value ######\n")
	print(type(value.value))


	print("\n##### Convert this garbage to something useful, like a dictionary ######\n")
	temp = value.value
	dict_str = temp.decode("UTF-8")
	mydata = ast.literal_eval(dict_str)
	print(repr(mydata))

	print("\n##### Let's get the values now  ######\n")
	date, url = mydata.get('date'), mydata.get('url')
	print("\n #### here is the parsed data first date #### \n")
	print(date)
	print("\n #### now the url #### \n")
	print(url)

	#print(date, url)
	#Ok this sends your values in the array to the test one. 

main()