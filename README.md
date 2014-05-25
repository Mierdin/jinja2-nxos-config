## ABOUT

A set of files producing Cisco NXOS configurations using Jinja2 framework

Powered by Python and Jinja2, but intended to be easy enough to use that you only have to modify the YAML config files

## JINJA2 Snippets

This is a work in progress, please see [snippets](snippets) directory for all of the Jinja2 snippets I'm currently working with.

I have them split out as granularly as possible - I didn't want to have snippets per switch type, so the YAML file will pick and choose from these to build the configuration appropriate for the target switch.

## REQUIREMENTS

This will build a configuration for a very specific hardware platform right now. Details:

Tested NXOS version and switch model TBD. However, some assumptions during this initial build:
- Nexus 5K with FC/FCoE services (this shows in many various snippets)
- vPC using the mgmt0 interfaces for keepalive
Future versions will allow this to be more configurable

Requires [UCS Python SDK](https://communities.cisco.com/docs/DOC-37174) (if you want to pull data from UCS to define config)
