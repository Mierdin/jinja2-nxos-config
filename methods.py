#!/usr/bin/env python

#TODO: Clean up unused imports
from ucstools import storage
from jinja2 import Template, Environment, FileSystemLoader
import csv, yaml

class PhysicalInterface:
    '''A class to define a physical interface'''
    def __init__(self):
        self.slotid = ''
        self.portid = ''
        self.description = ''
        self.switchportMode = ''
        self.speed = ''
        self.channelGroup = ''
        self.accessVlan = ''
        self.allowedVlans = ''

def getconfig():
  with open('n5kconfig.yaml') as f:
    return yaml.load(f)

def getVlans():
  vlans = {123: 'TEST-VLAN-123', 234: 'TEST-VLAN-234', 345: 'TEST-VLAN-345'}
  return vlans

def getVsans():
  vsans = {321: 'TEST-VSAN-321'}
  return vsans

def getTargets():
  targets = {}
  targets['50:00:00:00:00:11:a0:01'] = 'Netapp-01-0a'
  targets['50:00:00:00:00:11:a0:02'] = 'Netapp-01-0b'
  return targets

def getInitiators():
    initiators = {}
    initiators['20:00:00:25:b5:11:a0:00'] = 'ESX-01_ESX-VHBA-A'
    initiators['20:00:00:25:b5:11:a0:01'] = 'ESX-02_ESX-VHBA-A'
    initiators['20:00:00:25:b5:11:a0:02'] = 'ESX-03_ESX-VHBA-A'
    initiators['20:00:00:25:b5:11:a0:03'] = 'ESX-04_ESX-VHBA-A'

    handle = UcsHandle()
    handle.Login('10.12.0.136', username="config", password="config")

    return initiators

def getPhysicalInterfaces():

    pintArray = []

    with open('./Templates/n5k/physicalints.csv', 'rb') as csvfile:

        reader = csv.reader(csvfile,delimiter=';')

        for row in reader:
            thisPint = PhysicalInterface()
            thisPint.slotid = row[0]
            thisPint.portid = row[1]
            thisPint.description = row[2]
            thisPint.switchportMode = row[3]
            thisPint.speed = row[4]
            thisPint.channelGroup = row[5]
            thisPint.accessVlan = row[6]
            thisPint.allowedVlans = row[7]
            pintArray.append(thisPint)

    return pintArray
