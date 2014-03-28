#This will build a configuration for a very specific hardware platform right now. Details:

	#Cisco Nexus 5548UP (48 SFP+ ports)
	#No Fibre Channel ports configured (intent is all FCoE)
	#Tested NXOS version TBD

#Requires Cisco UCS Python SDK 0.8 to pull vHBA information
#Tested with UCS Platform Emulator 2.2(1bPE1)
from UcsSdk import *

from jinja2 import Template, Environment, FileSystemLoader
import csv


#Building these classes to keep things straight in my head - these may go away for simpler alternatives in the future.

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

def getFeatures():
	# Some feature enablement/installation varies by syntax, so "features" should be an array of actual NXOS commmands to install or enable a feature 
	# This may change in the future with some kind of "feature" class....need to think about this
	featureArray = ['feature fcoe',
	'install feature-set fabricpath',
	'feature-set fabricpath',
	'feature npiv',
	'feature fport-channel-trunk',
	'feature tacacs+',
	'cfs eth distribute',
	'feature udld',
	'feature interface-vlan',
	'feature lacp',
	'feature vpc',
	'feature lldp']
	return featureArray

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


def getUcsWWPNs():
	handle = UcsHandle()
	handle.Login('10.12.0.136', username="config", password="config")

	vHBADict = {}

	#TODO: Statically defining sub-organization for now, will make more dynamic later
	obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-ORG_TEST/"})
	moArr = handle.GetManagedObject(obj, "vnicFc")
	for mo in moArr:
		#Pull only actual vHBAs (not templates) and on the desired fabric (A/B)
		if str(mo.Addr) != 'derived' and mo.SwitchId == 'A':

			#We're retrieving Dn here so we can include the service profile in the name
			origDn = str(mo.Dn)
			
			#Need to do a little string surgery to transform the Dn of the vHBA into a proper zone name.
			origDn = origDn.replace('org-root/org-ORG_TEST/','')
			origDn = origDn.replace('/','_')
			origDn = origDn.replace('ls-','')
			origDn = origDn.replace('fc-','')

			#using the WWPN address as key since more likely to be unique
			vHBADict[mo.Addr] = origDn

	return vHBADict

env = Environment(loader=FileSystemLoader('./Templates/n5k/'))
template = env.get_template('nexus5548UP')

print template.render(hostname='N5K-A',
	features=getFeatures(),
	vlanDict=getVlans(),
	vsanDict=getVsans(),
	initDict=getUcsWWPNs(),
	targetDict=getTargets(),
	pints=getPhysicalInterfaces())






