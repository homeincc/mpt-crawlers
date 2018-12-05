#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from datetime import datetime
import pprint


paging_limit = 50
api_url = "https://api.apify.com/v1/"
default_date = datetime(1970,1,1)
date_format = "%Y-%m-%dT%H:%M:%S"
date_start = 0
date_end = -5

class Apify:
	def __init__(self,user,api_token):
		self.user = user
		self.api_token = api_token
		self.api_url = os.path.join(api_url,self.user)
	def build_crawler(self,cdata):
		if cdata["lastExecution"]==None:
			cdata["lastExecution"] = {}
			cdata["lastExecution"]["status"]="NONE"
			cdata["lastExecution"]["_id"]=""		
		c = Crawler(self,
			cdata["_id"],
			cdata["customId"],
			datetime.strptime(cdata["createdAt"][date_start:date_end],date_format),
			datetime.strptime(cdata["modifiedAt"][date_start:date_end],date_format),
			cdata["lastExecution"]["status"],
			cdata["lastExecution"]["_id"])
		return c
	def get_crawlers(self):
		params = {
			"token": self.api_token,
			"limit": paging_limit,
			"offset": 0,
			"desc": 1
		}
		crawlers = []
		endpoint = "crawlers"
		url = os.path.join(self.api_url,endpoint)
		offset = 0
		while True:
			params["offset"] = offset
			r = requests.get(url,params=params)
			data = r.json()
			if len(data)==0 or data==None: break
			for cdata in data:
				c = self.build_crawler(cdata)
				crawlers.append(c)
			offset += len(data)
		return crawlers
	def get_crawler(self,cid):
		params = {
			"token": self.api_token
		}
		endpoint = os.path.join("crawlers",cid)
		url = os.path.join(self.api_url,endpoint)
		r = requests.get(url,params=params)
		data = r.json()
		if len(data)==0:
			return None
		else:
			return self.build_crawler(data)
	def run_crawler(self,cid):
		params = {
			"token": self.api_token,
			"tag": "run_from_script"
		}
		endpoint = os.path.join("crawlers",cid,"execute")
		url = os.path.join(self.api_url,endpoint)
		r = requests.get(url,params=params)
		data = r.json()

class Crawler():
	def __init__(self,parent,_id="",name="",created=default_date,modified=default_date,status="STOPPED",last_execution_id=""):
		self.parent = parent
		self.id = _id
		self.name = name
		self.created = created
		self.modified = modified
		self.status = status
		self.last_execution_id = last_execution_id
	def load(self):
		self.parent.get_crawler(self.id)
	def __str__(self):
		return "<apify.Crawler \"{0}\", id={1}, created at {2}>".format(self.name,self.id,str(self.created))
	def __repr__(self):  return str(self)