#!/usr/bin/env python
""" jinja2-nxos-config

    Accepts arguments from YAML config file
    and generates a Jinja2 configuration
"""

#TODO: Consider use of the leading underscore
#from ucstools import storage
from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('./snippets/'))

def get_config(configfile):
    """Pulls YAML configuration from file and returns dict object"""
    with open(configfile) as _:
        return yaml.load(_)

def gen_snippet(snippet, config):
    """Renders a config snippet.
    "config" represents the portion of the YAML
    file applicable to this snippet"""

    template = ENV.get_template(snippet + ".j2")
    return template.render(config=config)
