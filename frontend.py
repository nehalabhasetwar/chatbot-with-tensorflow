from flask import Flask, render_template, request, url_for
import re
from datetime import datetime, timezone

from werkzeug.utils import redirect


def utl(utc_dt):
	now = datetime.now()
	current_time = now.strftime("%H:%M")
	return current_time

import requests
import json

app=Flask(__name__)


data=[
	{
		'name':'Bot',
		'text':'Hi , I am John Lewis',
		'time':'11:00',
		'link':'',
		'list':''
	}
]
data[0]['time']=str(utl(datetime.utcnow()))

@app.route('/',methods=['GET','POST'])
def chatter():
	if request.is_json:
		text=request.get_json()
		print(text)
		temp={
			'name':'User',
			'text':'',
			'time':'',
			'link':'',
			'list':''
		}

		oldmsg = text[1]
		newmsg = text[0]
		str1=""
		if newmsg[1] == '?':
			str1 = oldmsg+" "+newmsg[2:]
			temp['text']=newmsg
			print(str1)
		else:
			str1=newmsg
			temp['text']=newmsg

		print(temp['text'])

		temp['time']=str(utl(datetime.utcnow()))
		print(datetime.utcnow)
		data.append(temp)

		#try:
		
		body={'text':''}
		body['text']=str1
		text2=requests.post('http://127.0.0.1:5500',json=body)
		print(text2.status_code)
		#except:
			#print("cannot connect to server")


	return render_template('chatbot2.html',data=data)

@app.route('/reply',methods=['POST'])
def getchat():
	response=request.json
	text=response['text']
	link=response['link']
	list=response['list']
	temp={
		'name':'Bot',
		'text':'',
		'time':'',
		'link':'',
		'list':''
	}
	temp['text']=text
	temp['time']=str(utl(datetime.utcnow()))
	temp['link']=link
	temp['list']=list
	data.append(temp)
	return


if __name__=='__main__':
	app.run(port=5200 , debug=True)