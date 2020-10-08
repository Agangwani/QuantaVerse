import os
import sys
import time
from random import randint,choice
import string
from multiprocessing import Pool, cpu_count
import json
from glob import glob

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
    return 

def connect_to_data_store():
    return

def read_message_from_broker(message):
    return message['date'], message['url']

def send_message_to_broker(date,url):
    return json.dumps({'date':date, 'url':url})

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
    date,url = read_message_from_broker(message)

    def generate_content(purl):
        with open(purl) as fin:
            content = ''.join(fin.readlines())
        return content

    print('Processing',name,date,url,flush=True)
    content = read_content_from_disk(fs_root_in, date, url)
    if content:
        try:
            if save_content_to_disk(fs_root_out, date, url, content):
                return send_message_to_broker(date,url)
        except:
            return
    else:
        print('--Failed processing',date,url,flush=True)
        #retry?
    return

def collect_processed_responses(response):
    if response:
        with open(os.path.join(fs_root_out,'broker.txt'),'a') as fout:
            fout.write(response+'\n')
    return

if __name__ == "__main__":
    #connect servers
    connect_to_data_store()
    connect_to_message_broker()
   
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
        message = _fin.readline().strip()
        if message:
            pool.apply_async(process_news, args=(name, json.loads(message)), callback=collect_processed_responses)
            #collect_processed_responses(process_news(name, json.loads(message)))
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
