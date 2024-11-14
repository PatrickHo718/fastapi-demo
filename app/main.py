#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

app = FastAPI()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello beautiful people"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/square/{a}")
def sqr(a: int):
    return {"square": a * a}

@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    return {"multiply": a * b}

@app.get("/subtract/{a}/{b}")
def subtract(a: int, b: int):
    return {"difference": a - b}


import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

DBHOST = os.getenv('DBHOST')
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
DB = os.getenv('DB')

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        output = json_data
        return(output)
    except mysql.connector.Error as e:
        print("MySQL Error: ", str(e))
        return None
    cur.close()

@app.get('/songs')
def get_songs():
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre FROM songs JOIN genres ON songs.genre = genres.genreid ORDER BY songs.title;"
    try:
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        output = json_data
        return(output)
    except mysql.connector.Error as e:
        print("MySQL Error: ", str(e))
        return None
    cur.close()
