#!/usr/bin/env python

# map_split.py :  extracts variant and fuel maps from a Nanocom .map file

# Copyright (C) 2018  Paul Jacobson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
from array import *

# split a Nanocom .map into variant and fuelmap components.
# usage:  python  map_split.py  mapfile.map

def writechunk(filename, bindata):
	with open(filename, "wb") as thisfile:
	  thisfile.write(bindata)
	  thisfile.close()

def ffpad(map_array, expect_len):
	for i in range(len(map_array), expect_len << 10):
		map_array.append(255)

path = sys.argv[1]

with open( path, 'rb') as file:

	fdata = array('B', file.read())
	file.close()

	# check this is a .map file
	header = fdata[0:6]

	if (header.tostring() != b'TD5map'):
		print('File is not a Td5 .map' )
		exit()

	# Read fuel map offset from the .map header
	fm_start = (fdata[6] << 16) + (fdata[7] << 8) + fdata[8]

	# Extract the Variant Map
	va = fdata[9:fm_start]

	ffpad(va, 128)
	va_name = va[1024:1040:2].tostring()

	# Extract the Fuel Map
	fm_length = (fdata[fm_start] << 8) + fdata[fm_start + 1]
	fm = fdata[fm_start:fm_start+fm_length]
	
	# Pad map to exactly 16Kb
	ffpad(fm, 16)
	fm_name = fm[2:18].tostring()

	writechunk("vm_" + va_name + ".bin", va)
	writechunk("fm_" + fm_name + ".bin", fm)
