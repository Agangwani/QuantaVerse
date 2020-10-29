from kafka import KafkaConsumer

from kafka import KafkaProducer
import json


def send_to_broker(data):
	pass

def main():
	#consumer = KafkaConsumer(group_id='test', bootstrap_servers=['localhost:9092'])
	producer = KafkaProducer(bootstrap_servers='localhost:9092')
	myarr = [6,7,8,9,10]
	#for element in myarr:
		#producer.send('test', json.dumps(element).encode('utf-8'))



	mydict = {'date': 2123091219029012, 'url': 'asdlfkj;alsdfjk.html'}
	producer.send('test', json.dumps(mydict).encode('utf-8'))
	#break this into 2 scripts
	#one for consumer, one for producer

	#Ok this sends your values in the array to the test one. 

main()