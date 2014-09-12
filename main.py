import argparse
import subprocess
import xml.etree.ElementTree as ET
import os
import pyrax
import datetime

# get inputs
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input file")
parser.add_argument("-o", "--output", required=True, help="Output file")
parser.add_argument("-q", "--quality", required=True, type=int, help="Quality")
parser.add_argument("-p", "--profile", required=True, help="profile")

args = vars(parser.parse_args())

print args['input'], args['output'], args['quality'], args['profile']

# run mediainfo using inputs
#root = ET.fromstring(subprocess.check_output(['mediainfo', '--Output=XML', args['input']]))

# parse XML
#for child in root:
#	print child.tag, child.attrib

raxcreds = os.path.expanduser('~/.credentials')

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region('lon')

pyrax.set_credential_file(raxcreds)

cs = pyrax.cloudservers

image = pyrax.images.get('88928a0a-f94c-47e3-ad7d-27b735af1a15')

flavor = cs.flavors.get('2')

keypair = cs.keypairs.create("ubuntu-zfs", public_key)

server = cs.servers.create('encoder'+datetime.datetime.now().isoformat(), image.id, flavor.id, key_name=keypair.name)

pyrax.utils.wait_for_build(server, verbose=True)
