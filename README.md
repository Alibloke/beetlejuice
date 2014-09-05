Beetlejuice.  A script that takes a file and transcodes is using temporary cloud compute.

Current structure:
* Run mediainfo on input, output to XML
* Spin up a compute node
* Upload input file
* Run Handbrake-CLI using a mix of parameters and mediainfo based off the ptp transcoding rules
* Upload resulting transcode somewhere
* Delete compute node

Inputs:
* Filename
* API key
* Encoding options (how many?)
* Upload location & credentials (keys only?)
