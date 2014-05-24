#!/usr/bin/env python

#TODO: Clean up unused imports
from ucstools import storage
from jinja2 import Template, Environment, FileSystemLoader
import csv, yaml

#TODO: Make all indentations match. (Might be a standard size in Atom)
#TODO: Consider use of the leading underscore
#TODO: Get this to a usable state as quickly as possible, then start making changes in a branch. Get people using master.

import methods

def run():
	env = Environment(loader=FileSystemLoader('./Templates/n5k/'))
	template = env.get_template('nexus5548UP')

	print template.render(hostname='N5K-A',
		features=getFeatures(),
		vlanDict=getVlans(),
		vsanDict=getVsans(),
		initDict=storage.getUcsWWPNs('10.12.0.78','config','config'),
		targetDict=getTargets(),
		pints=getPhysicalInterfaces())

if __name__ == "__main__":
	configDict = methods.getconfig()
	print configDict['pull_fc_from_ucs']
