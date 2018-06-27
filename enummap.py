#!/bin/env python3

import os, xml.etree.ElementTree, sys

# TODO: Make cross-platform, since not all have /tmp
tmpDir = '/tmp/' 

if len(sys.argv) < 3:
    print("Usage: ./enummap.py <input> <output> [<include dirs>...]")
    exit(-1)

for arg in sys.argv:
    arg = arg.replace('\'', '')

fileName = sys.argv[1]
astFileName = tmpDir + os.path.basename(fileName) + ".xml"

includeDirs = ""
for i in range(2, len(sys.argv)):
    for s in sys.argv[i].split():
        includeDirs += " -I" + s

castXmlArgs = includeDirs + " -std=c++17 --castxml-output=1 -o " + astFileName

log = open('/tmp/log.logger', 'w')
log.write("castxml " + fileName + castXmlArgs)
log.close()

os.system("castxml " + fileName + castXmlArgs)

ast = xml.etree.ElementTree.parse(astFileName).getroot()

mapFile = open(sys.argv[2], 'w')
mapFile.write("#pragma once\n#include <unordered_map>\n#include <" + os.path.basename(fileName) + ">\n")
mapFile.write("// Generated from " + fileName + "\n")

for enum in ast.findall('Enumeration'):
    if enum.get("attributes") != "annotate(Stringify)":
        continue
    name = enum.get("name")
    mapFile.write("static const std::unordered_map<" + name + ", std::string> " + name + "Mappings = {")
    for val in enum:
        value = val.get("name")
        mapFile.write("{" + name + "::" + value + ", \"" + value + "\"},\n")
    mapFile.write('};\n')
    mapFile.write("""
    inline const std::string& to_string(const """ + name + """ from) { return """ + name + """Mappings.at(from); } 
   template <>                                                                                 
   inline """ + name +""" from_string<"""+ name + """>(const std::string& in) {                              
      for (const auto& pairing : """ + name + """Mappings)                                                 
         if (pairing.second == in)                                                             
            return pairing.first;
    return """ + name + """(UINTMAX_MAX);                                                         
   }""")

os.system("rm " + astFileName)

