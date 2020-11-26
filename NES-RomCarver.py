#/bin/python
import sys
import os
import mmap
import argparse

parser = argparse.ArgumentParser(description='Extract INES format NES roms from Wii virtual console, or any file really')

parser.add_argument("Input", help="Input file")
parser.add_argument("Output", help="Output file")

args = parser.parse_args()

def findINESHeader(inFile):
    s = mmap.mmap(inFile.fileno(), 0, access=mmap.ACCESS_READ)
    return s.find(b'NES\x1A')

def retPRGplusCHRSize(inFile):
    inFile.seek(4, 1)
    prgsize = int.from_bytes(inFile.read(1), "little") * 16384
    chrsize = int.from_bytes(inFile.read(1), "little") * 8192
    inFile.seek(findINESHeader(inFile), 0)
    return(prgsize + chrsize) 

inFile = open(sys.argv[1], 'rb')

inFile.seek(findINESHeader(inFile))

nes = open(args.Output, 'wb')
nes.write(inFile.read(retPRGplusCHRSize(inFile) + 16))
nes.close()