import concurrent.futures
import requests
import random

list = open("proxies.txt", "r").readlines()

def extract(proxy):
    try:
        proxy = {"http://": "{}".format(random.choice(list).rstrip())}
        ret = requests.get("http://www.immobiliare.it/affitto-case/firenze-provincia/?criterio=dataModifica&ordine=desc&prezzoMassimo=500", proxies=proxy, timeout=2)
        if(ret.status_code == 200):
            print("working...")
    except:
        pass
        
with concurrent.futures.ThreadPoolExecutor() as exector:
    exector.map(extract, list)
