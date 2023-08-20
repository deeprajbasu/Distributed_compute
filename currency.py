
from threading import Thread
from queue import Queue
import urllib.request
import pandas as pd
from io import StringIO as sio
import csv

URL ='https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1660768315&period2=1692254623&interval=1d&events=history&includeAdjustedClose=true'

def get_rate(pair, outq, url_tmplt=URL):
  #download data from yahoo given a tickr
  #put data in que when recieved
 with urllib.request.urlopen(url_tmplt.format(pair)) as res:

  body = str(res.read())
  outq.put((pair, body.strip()))


if __name__ == '__main__':
 import argparse
 parser = argparse.ArgumentParser()
 parser.add_argument('pairs', type=str, nargs='+')
 args = parser.parse_args()

 #hold output data in this que
 outputq = Queue()

for pair in args.pairs:
  t= Thread(target=get_rate,kwargs={'pair':pair,
                                    'outq':outputq})

  #python wont wait for thread to quit
  #notice order of input vs order of putput(sequence)
  t.daemon=True
  t.start()

for _ in args.pairs:
  pair,rate=outputq.get()
  print(pair,rate)
  outputq.task_done()

outputq.join()
