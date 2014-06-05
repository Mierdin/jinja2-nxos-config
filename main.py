#!/usr/bin/env python
""" jinja2-nxos-config

    Accepts arguments from YAML config file
    and generates a Jinja2 configuration
"""

import sys, methods

def run():
    """Function docstring"""
    try:
        yamlfile = sys.argv[1]
    except IndexError:
        print "Please refer to documentation for proper arguments"
    configdict = methods.get_config(yamlfile)
    
    #Generate configurations for the core snippets
    for snippet in configdict['coresnippets']:
        print methods.gen_snippet(snippet, configdict[snippet])

    #TODO: consider doing some kind of check for core stuff before features

if __name__ == "__main__":
    run()
