#!/usr/bin/python2.7
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import psycopg2
import json
import time
import logging
import traceback

class HttpProcessor(BaseHTTPRequestHandler):
   def do_POST(self):
      self.send_response(200)
      self.send_header('content-type','application/json')
      self.send_header('Access-Control-Allow-Origin','*')
      self.end_headers()
      cursor.execute("select internal_temp1, internal_temp2,internal_temp3, internal_temp4,to_char(datetime, 'YYYY-MM-DD') ||'T'|| to_char(datetime, 'HH24:MI:SS') from sensors where id> (select id from sensors limit 1)-300")
      results = cursor.fetchall()
      print (json.dumps(results)) 
      self.wfile.write(json.dumps(results))

logging.basicConfig(filename="sample.log", filemode="w", level=logging.DEBUG)
logging.debug("This is a debug message:")
logging.info("This is an info message:")
logging.error("An error has happened:")

DBconn = psycopg2.connect(host='localhost', user='username', password='password', dbname='databasename')
cursor = DBconn.cursor()

serv = HTTPServer(("localhost",9999),HttpProcessor)
serv.serve_forever()

