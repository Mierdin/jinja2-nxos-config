#!/usr/bin/env python

#TODO: Clean up unused imports
from ucstools import storage
from jinja2 import Template, Environment, FileSystemLoader
import yaml
#TODO: Consider use of the leading underscore

#Set directory for Jinja2 snippets
env = Environment(loader=FileSystemLoader('./snippets/'))

def get_config(file):
    '''Pulls YAML configuration from file and returns dict object'''
    with open(file) as f:
        return yaml.load(f)

def gen_snippet(snippet, config):
    '''Renders a config snippet. "config" represents the portion of the YAML file applicable to this snippet.'''
    template = env.get_template(snippet)
    #See if you can simplify the below even more - may just accept a standard "config" dictionary in each Jinja template so you can refer to it the same way each time
    #See "misc" snippet
    if snippet == 'features':
        return template.render(features=config)
    elif snippet == 'vlans':
        return template.render(vlans=config)
    elif snippet == 'fcalias':
        return template.render(initDict=config['initiators'], targetDict=config['targets'])
    elif snippet == 'qos':
        return template.render(qos=config)
    elif snippet == 'ports':
        return template.render(ports=config)
    elif snippet == 'misc':
        return template.render(config=config)

def getucswwpns(module):
    #Need UCS Python SDK for this
    #May consider simplifying calls like this in a library
    results = {}

    outputfile = module.params['outputfile']
    outputfile = os.path.abspath(outputfile)

    results['outputfile'] = outputfile

    #This module is not built to make changes, so we are returning false here.
    results['changed'] = False

    try:

        logging.info("Connecting to UCSM at " + module.params['host'])

        #Connect to UCSM
        handle = UcsHandle()
        handle.Login(module.params['host'], username=module.params['ucs_user'], password=module.params['ucs_pass'])

        #Instantiate the dictionaries that will hold our WWPNs
        vHBADict = {}
        FabADict = {}
        FabBDict = {}

        #TODO: Statically defining sub-organization for now, will make more dynamic later

        #Need to make a generic function (probably place in central "general functions" file that finds an org at any nest level,
        #and retrieves ful DN for things like what you're doing below. Allows for org filtering at any level
        ucsOrg = "org-ORG_TEST"

        f = open(outputfile,'w')

        #TODO: For some reason, if the specified org does not exist, this still returns all orgs, rather than erroring out or providing a null value. Need to handle this better
        obj = handle.GetManagedObject(None, None, {"Dn":"org-root/" + ucsOrg + "/"})
        moArr = handle.GetManagedObject(obj, "vnicFc")
        for mo in moArr:
            #Pull only actual vHBAs (not templates) and on the desired fabric (A/B)
            if str(mo.Addr) != 'derived' and mo.SwitchId == 'A':

                #We're retrieving Dn here so we can include the service profile in the name
                origDn = str(mo.Dn)

                #Need to do a little string surgery to transform the Dn of the vHBA into a proper zone name.
                origDn = origDn.replace('org-root/' + ucsOrg + '/','')
                origDn = origDn.replace('/','_')
                origDn = origDn.replace('ls-','')
                origDn = origDn.replace('fc-','')

                logging.info('Retrived ' + origDn + ' with address ' + mo.Addr)

                #using the WWPN address as key since more likely to be unique
                FabADict[mo.Addr] = origDn

            elif str(mo.Addr) != 'derived' and mo.SwitchId == 'B':

                #We're retrieving Dn here so we can include the service profile in the name
                origDn = str(mo.Dn)

                #Need to do a little string surgery to transform the Dn of the vHBA into a proper zone name.
                origDn = origDn.replace('org-root/' + ucsOrg + '/','')
                origDn = origDn.replace('/','_')
                origDn = origDn.replace('ls-','')
                origDn = origDn.replace('fc-','')

                logging.info('Retrived ' + origDn + ' with address ' + mo.Addr)

                #using the WWPN address as key since more likely to be unique
                FabBDict[mo.Addr] = origDn

        #Populate primary dictionary
        vHBADict['a'] = FabADict
        vHBADict['b'] = FabBDict

        json.dump(vHBADict, f, sort_keys=True)

        #Clean-up
        f.close()
        handle.Logout()

        logging.info('WWPNs retrieved, JSON file created.')

    except Exception, err:
        results['failed'] = True
        msg = "Unable to retrieve info"
        results['msg'] = msg
        logging.info('Error aon {}'.format(module.params['host']))
        logging.info(err)
        module.fail_json(msg='error on {}'.format(module.params['host']))

    return results


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
