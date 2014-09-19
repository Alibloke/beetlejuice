import argparse
from subprocess import call
import xml.etree.ElementTree as ET
import os
import pyrax
import datetime
import sys

# get inputs
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input file")
parser.add_argument("-o", "--output", required=True, help="Output file")
parser.add_argument("-q", "--quality", required=True, type=int, help="Quality")
parser.add_argument("-p", "--profile", required=True, help="profile, can be normal, simple, faster, 720p, 1080p")
parser.add_argument("-f", "--flavor", required=True, help="flavor, can be fast, faster or fastest")

args = vars(parser.parse_args())

# does file exist?
if not os.path.isfile(args['input']):
	print "Error: Input file doesn't exist"
	sys.exit(1)

# quality check
if args['quality'] > 22 or args['quality'] < 17:
	print 'Error: quality must be between 17-22'
	sys.exit(2)

# profile chooser
if args['profile'] == 'normal':
	profile = 'ref=9:mixed-refs=1:b-adapt=2:bframes=6:weightb=1:direct=auto:me=umh:subq=9:analyse=all:8x8dct=1:trellis=2:no-fast-pskip=1:psy-rd=1,0:merange=24:deblock=-2,-2:rc-lookahead=50:aq-strength=1.2:b-pyramid=2'
elif args['profile'] == 'simple':
        profile = 'ref=9:mixed-refs=1:b-adapt=2:bframes=7:weightb=1:direct=auto:me=umh:subq=9:analyse=all:8x8dct=1:trellis=2:no-fast-pskip=1:psy-rd=0.7,0:merange=24:deblock=0,0:rc-lookahead=50:b-pyramid=2'
elif args['profile'] == 'fast':
        profile = 'ref=5:mixed-refs=1:b-adapt=2:bframes=5:weightb=1:direct=auto:me=umh:subq=8:8x8dct=1:trellis=1:psy-rd=1,0:deblock=-2,-2:rc-lookahead=40:aq-strength=1.2:b-pyramid=2'
elif args['profile'] == '720p':
        profile = 'ref=6:mixed-refs=1:b-adapt=2:bframes=6:weightb=1:direct=auto:me=umh:subq=9:analyse=all:8x8dct=1:trellis=2:no-fast-pskip=1:psy-rd=1,0:merange=28:deblock=-2,-2:rc-lookahead=50:aq-strength=1.0:b-pyramid=2'
elif args['profile'] == '1080p':
	profile = 'ref=4:mixed-refs=1:b-adapt=2:bframes=5:weightb=1:direct=auto:me=umh:subq=9:analyse=all:8x8dct=1:trellis=2:no-fast-pskip=1:psy-rd=1,0:merange=32:deblock=-3,-3:rc-lookahead=50:aq-strength=1.0:b-pyramid=2'
else:
	print "Error: profile must be either normal, simple, faster, 720p or 1080p"
	sys.exit(3)

# choose flavor
if args['flavor'] == 'fast':
	flavors = '8'
elif args['flavor'] == 'faster':
	flavors = 'performance1-8'
elif args['flavor'] == 'fastest':
	flavors = 'performance2-60'
else:
	print "Error: You didn't choose a suitable flavor"
	sys.exit(1)

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

flavor = cs.flavors.get(flavors)

server = cs.servers.create('encoder'+datetime.datetime.now().isoformat(), image.id, flavor.id, key_name="ubuntu-zfs")

pyrax.utils.wait_for_build(server, verbose=True)

# find compute details
network = server.networks["public"]

ipv4='0.0.0.0'

for public_ip in network:
	if '.' in public_ip:
		ipv4 = public_ip

# upload input to compute node
#call(['rsync', '--progress', '-e', 'ssh -o StrictHostKeyChecking=no', args['input'], 'root@'+ipv4+':'])
# temporary copy from faster source
call(['ssh', '-o', 'StrictHostKeyChecking=no', 'root@'+ipv4, 'wget', '-q', '--no-check-certificate', 'https://secure.arhaswell.co.uk/luxo.ts'])

# install handbrake on compute node
call(['ssh', 'root@'+ipv4, 'pacman', '-Sy', 'handbrake-cli', '--noconfirm'])

print ipv4

# run encode
call(['ssh', 'root@'+ipv4, 'HandBrakeCLI', '--main-feature', '-m', '-q', str(args['quality']), '--strict-anamorphic', '--crop', '--detelecine', '--decomb', '-i', args['input'], '-o', args['output'], '-E', 'copy:ac3', '-e', 'x264', '-x', profile])

# copy output back
call(['rsync', '--progress', 'root@'+ipv4+':'+args['output'], '.'])

# delete node
server.delete()
