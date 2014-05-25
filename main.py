#!/usr/bin/env python

import sys, methods

if __name__ == "__main__":
	try:
		yamlfile = sys.argv[1]
	except IndexError:
		pass #TODO: add error message
	configDict = methods.get_config(yamlfile)

	for snippet in configDict['5ksnippets']:
		print methods.gen_snippet(snippet, configDict[snippet])
