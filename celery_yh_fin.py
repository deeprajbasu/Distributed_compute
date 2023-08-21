
from threading import Thread
from queue import Queue
import urllib.request
from io import StringIO as sio
import csv
import celery

app=celery.Celery('currency',broker='redis://localhost:6379',backend='redis://localhost:6379',)
URL ='https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1660768315&period2=1692254623&interval=1d&events=history&includeAdjustedClose=true'

@app.task
def get_rate(pair, url_tmplt=URL):
  #download data from yahoo given a tickr
  #put data in que when recieved
 with urllib.request.urlopen(url_tmplt.format(pair)) as res:

  body = str(res.read())
  return (pair,body.strip())


if __name__ == '__main__':
 import argparse
 parser = argparse.ArgumentParser()
 parser.add_argument('pairs', type=str, nargs='+')
 args = parser.parse_args()

 results = [get_rate.delay(pair) for pair in args.pairs]

 for result in results:
  pair,rate = result.get()
  print(pair,rate)  
