import argparse
import subprocess

# Get inputs
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="Input file")
parser.add_argument("-o", "--output", required=True, help="Output file")
parser.add_argument("-q", "--quality", required=True, type=int, help="Quality")
parser.add_argument("-p", "--profile", required=True, help="profile")

#args = vars(parser.parse_args())
args = parser.parse_args()

#print args['input'], args['output'], args['quality'], args['profile']
print "{} {} {} {}".format(args['input'], args['output'], args['quality'], args['profile'])

#subprocess.check_output(['mediainfo', +infile])
