#!/usr/bin/env python3
# -*- coding: utf-8 -*-

PLUGIN_NAME = "PornHub.com scraper for MPT"
PLUGIN_FILENAME = "plugin.py"
PLUGIN_DESCRIPTION = "Scrapes videos info and stores it in the MPT DB structure."


# Standard imports
import os
import json
import sys

# MPT Plugin base module
sys.path.append("../base")
try:
	import mpt_plugin
except ImportError as e:
	print(e)
	print("Maybe you moved the directory?")
	sys.exit(0)

# Apify module
try:
	from apify import Apify
except ImportError as e:
	print(e)
	print("Apify module is required. See our git.")
	sys.exit(0)
	

# Config file (containing apify token and user info (see config-sample.json for more information)
if not os.path.exists("config.json"):
	print("config.json does not exist.")
	sys.exit(0)

with open("config.json") as infile:
	config = json.load(infile)

# Initiate MPT plugin base module
args = mpt_plugin.init(PLUGIN_FILENAME,PLUGIN_DESCRIPTION,supports=mpt_plugin.SUPPORTS_ALL)

def action_poll(action_arguments={}):
	a = Apify(config["apify"]["user"],config["apify"]["token"])
	for crawler in config["crawlers"]:
		print(a.get_crawler(crawler["id"]).status)

if args.action[0] == "poll":
	action_poll()

