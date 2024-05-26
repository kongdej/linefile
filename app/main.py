# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
from datetime import datetime
import pytz 
import zeep

from fastapi import Request, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_TOKEN', None)
host_url = os.getenv('HOST_URL', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=channel_access_token
)

app = FastAPI()

async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)

app.mount("/liff", StaticFiles(directory="liff", html = True), name="liff")

@app.post("/webhook")
async def handle_callback(request: Request):
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        
        if event.message.type == 'text':
            if event.message.text == 'register':
                url= host_url + '/liff'
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=url)]
                    )
                )
            else:
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=event.message.text)]
                    )
                )
        

    return 'OK'

@app.post("/register")
async def handle_register(request: Request):
    body = await request.body()
    body = body.decode()
    body = json.loads(body)
    if isEGATUser(body['username'],body['password']) == True:
        #add user to db
        addUser(body)
        print ("found user")
        return True
    else:
        return False

def isEGATUser(username,password):
    print (username,password)
    try: 
        wsdl = 'http://webservices.egat.co.th/authentication/au_provi.php?wsdl'
        client = zeep.Client(wsdl=wsdl)
        result = client.service.validate_user(username, password)
        print('EGAT User: ', result)
        return result
    except:
        return False


def addUser(data):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # Creating table
    table = """ 
        CREATE TABLE IF NOT EXISTS users (
            empn VARCHAR(6) NOT NULL,
            userId VARCHAR(25) NOT NULL,
            created VARCHAR(25) NOT NULL
        ); 
       """
 
    cur.execute(table)
    sql = ''' INSERT INTO users (empn, userId, created)
              VALUES(?,?,?) '''
    val = (data['username'],data['userId'], datetime.now(pytz.timezone('Asia/Bangkok')))
    
    cur.execute(sql, val)
    con.commit()


    print ('add user into DB',data)