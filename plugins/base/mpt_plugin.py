#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

SUPPORTS_ALL = ["run","stop","store","clean","poll"]
args = None


# Initiate plugin and parse arguments
def init(plugin_name,plugin_description,supports=SUPPORTS_ALL):
	parser = argparse.ArgumentParser(plugin_name,description=plugin_description,epilog="Created with Home, Inc MyPreciousTime")
	parser.add_argument("action",action="store",nargs=1,choices=supports)
	global args
	args = parser.parse_args()
	return args