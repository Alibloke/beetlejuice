#/bin/python

# Import stuffs
import xml.etree.ElementTree as ET

# Read XML from disk
tree = ET.parse('mediainfo.xml')
root = tree.getroot()


