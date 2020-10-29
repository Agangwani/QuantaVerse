import os
import sys
import time
from random import randint,choice
import string
from multiprocessing import Pool, cpu_count
import json
from glob import glob

from kafka import KafkaConsumer

from kafka import KafkaProducer
import ast

#frequency  = how many articles per minute
#concurrency= how many cpus (bound to number of available cores)
#expiration = run for 'expiration' seconds
#fs_root    = root directory in file system
frequency,concurrency,expiration,fs_root_in,fs_root_out,name=sys.argv[-6:]

_fin  = None
def connect_to_message_broker():
	#Using a file as a message broker
    global _fin
    global fs_root_in
    while not _fin:
        try:
            _fin = open(os.path.join(fs_root_in,'broker.txt'))
        except:
            pass

    consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

    producer = KafkaProducer(bootstrap_servers='localhost:9092')
	
    return consumer, producer

#This used to be in connect_to_message_broker
def connect_to_data_store():
    return

def read_message_from_broker(message):
    return message['date'], message['url']

def send_message_to_broker(date,url):
    #return json.dumps({'date':date, 'url':url})
    #print("Reached send_message_to_broker")
    return #producer.send('test', json.dumps(url).encode('utf-8'))

def disconnect_from_message_broker():
    global _fin
    global _fout
    _fin.close()
    return

def disconnect_from_data_store():
    return

def read_from_preferred_data_store(path):
    try:
        with open(path) as fin:
            content = ''.join(fin.readlines())
        #with open(path.replace(),'wb') as fin:
        #    icontent = ''.join(fin.read())
        return content
    except:
        return

def save_to_preferred_data_store(path, content):
    try:
        with open(path,'w') as fout:
            fout.write(content)
        #with open(path.replace(),'wb') as fout:
        #    fout.write(content)
        return True
    except:
        return False

def read_content_from_disk(root, date, url):
    def create_path(root,date,url):
        purl=url.lower().replace('/','I').replace(':','-')
        purl=purl[:min(250,len(purl))]
        return os.path.join(root,date,purl)
    return read_from_preferred_data_store(create_path(root, date, url))

def save_content_to_disk(root, date, url, content):
    def create_path(root,date,url):
        purl=url.lower().replace('/','I').replace(':','-')
        purl=purl[:min(250,len(purl))]
        return os.path.join(root,date,purl)
    os.mkdir(os.path.join(root,date)) 

    return save_to_preferred_data_store(create_path(root, date, url), content)

def process_news(name, message):
    #content comes from brokers 
    #_ , producer = connect_to_message_broker()
    #consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])
    #date,url = read_message_from_broker(message)
    #value = next(consumer)
    #temp = value.value
    #dict_str = message.decode("UTF-8")
   # mydata = ast.literal_eval(dict_str)
    #### this gives us our dictionary, let's get the date and url now ###
    print(" Here is our dictionary", repr(message))
    date, url = message.get('date'), message.get('url')
    print("LETS GET THE DATE")
    print(date, url)

    def generate_content(purl):
        with open(purl) as fin:
            content = ''.join(fin.readlines())
        return content

    print('Processing',name,date,url,flush=True)
    #content = read_content_from_disk(fs_root_in, date, url)

    #print("PROCESSING sent to producer before")
    #producer.send('test', json.dumps(url).encode('utf-8'))
   # print("PROCESSING Sent to producer after")
   # if content: change when we set up mongo. 
    if message:
        #return send_message_to_broker(date,url)
        #return message
        pass
        """
        try:
            if save_content_to_disk(fs_root_out, date, url, content):
                return send_message_to_broker(date,url)
        except:
            return"""
    else:
        print('--Failed processing',date,url,flush=True)
        #retry?
    return "{'No message found': 'error'}"

def collect_processed_responses(response):
    #message, producer = response
    global producer
    #_, producer = connect_to_message_broker()
    #if response:
    #    with open(os.path.join(fs_root,'broker.txt'),'a') as fout:
    #        fout.write(str(response)+'\n')
    print("\n###This is the response ####\n")
    print(response)

    print("\n###This is the json.dumps response ####\n")

    print(json.dumps(response))
    #print(json.dumps)
    producer.send('SAdone', json.dumps(response).encode('utf-8'))
    return

if __name__ == "__main__":
    #connect servers
    #connect_to_data_store()
    consumer, producer = connect_to_message_broker()
    #mydict = {'consumer': consumer, 'producer': producer}
    #normalize input parameters
    delay      = 60.0/float(frequency)
    concurrency= min(int(concurrency),cpu_count())
    expiration = float(expiration)#*60.0

    #load list of source articles
    _list_of_sources = glob(os.path.join(fs_root_out,'source','*'))
    
    #produce articles until expiration time is reached
    pool     = Pool(processes=concurrency)
    t0       = time.time()
    while True:
        for message in consumer: 
        #message = next(consumer)#_fin.readline().strip()
            print("MESSAGE SET")
            print(message)
            temp = message.value
            print('TEMP TYPE', type(temp))
            print('PASSING THIS TO COLLECTPROCESSED',temp)
       # print(type(message))
       # print(message.value)

        #for key in range(len(message.args)):
           # print(key, message.args[key])

            print("new stuff")
            if message:
                #pool.apply_async(process_news, args=(name, json.loads(message)), callback=collect_processed_responses)
                collect_processed_responses(process_news(name, json.loads(temp)))
                t0 = time.time()
                time.sleep(delay)
            else:
                time.sleep(0.1)
                if time.time()-t0 > expiration:
                    break

    pool.close()
    pool.join()

    #disconnect servers
    disconnect_from_message_broker()
    disconnect_from_data_store()
    print('Finished processing all urls for',name,flush=True)
