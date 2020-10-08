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
frequency,concurrency,expiration,fs_root,name=sys.argv[-5:]

def connect_to_message_broker():
    return 

def connect_to_data_store():
    return

def send_message_to_broker(date,url):
    return json.dumps({'date':date, 'url':url})

def disconnect_from_message_broker():
    return

def disconnect_from_data_store():
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

def save_content_to_disk(root, date, url, content):
    def create_path(root,date,url):
        purl=url.lower().replace('/','I').replace(':','-')
        purl=purl[:min(250,len(purl))]
        return os.path.join(root,date,purl)
    os.mkdir(os.path.join(root,date)) 
    return save_to_preferred_data_store(create_path(root, date, url), content)

def generate_news(name):
    global _list_of_sources

    def pick_news_source():
        return choice(_list_of_sources)

    def generate_date():
        year  = str(randint(2000,2020))
        month = str(randint(1,12)).zfill(2)
        day   = str(randint(1,30)).zfill(2)
        return year+month+day

    def generate_url():
        url   = 'http'+ \
                ('s' if randint(1,5) > 1 else '')+ \
                '://www.'+ \
                ''.join(choice(string.ascii_letters + string.digits) for x in range(randint(5,10)))+ \
                '.com/'+ \
                ''.join(choice(string.ascii_letters + string.digits) for x in range(randint(10,15)))+ \
                '/'+''.join(choice(string.ascii_letters + string.digits) for x in range(randint(5,20)))+ \
                '.html'
        return url

    def generate_content(purl):
        with open(purl) as fin:
            content = ''.join(fin.readlines())
        return content

    date    = generate_date()
    url     = generate_url()
    print('Collecting',name,date,url,flush=True)
    content = generate_content(pick_news_source()) 

    if save_content_to_disk(fs_root, date, url, content):
        return send_message_to_broker(date,url)
    else:
        print('--Failed collecting',date,url,flush=True)
        #retry?
    return

def collect_processed_responses(response):
    if response:
        with open(os.path.join(fs_root,'broker.txt'),'a') as fout:
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
    _list_of_sources = glob(os.path.join(fs_root,'source','*'))
    
    #produce articles until expiration time is reached
    pool     = Pool(processes=concurrency)
    t0       = time.time()
    finished = False 
    while not finished:
        for t in range(concurrency):
            if time.time()-t0 > expiration:
                finished = True
                break
            pool.apply_async(generate_news, args=(name,), callback=collect_processed_responses)
            #collect_processed_responses(generate_news(name))
            time.sleep(delay)
        
    pool.close()
    pool.join()

    #disconnect servers
    disconnect_from_message_broker()
    disconnect_from_data_store()
    print('Finished collecting urls for',name,flush=True)
