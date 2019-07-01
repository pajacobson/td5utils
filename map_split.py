#!/usr/bin/env python3
# map_split.py :  extracts variant and fuel maps from a Nanocom .map file

# Copyright (C) 2018-2019  Paul Jacobson

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
import os

# split a Nanocom .map into variant and fuelmap components.
# usage:  python  map_split.py  mapfile.map

class MapSplit():

    def __init__(self, mapname):
        self.mappath = mapname
        self.basepath = os.path.split(mapname)[0]
        self.mapopen()

    def writechunk(self, filename, bindata):
        fp = os.path.join(self.basepath, filename )
        with open(fp, "wb") as thisfile:
            thisfile.write(bindata)

    def ffpad(self, map_array, expect_len):
        for i in range(len(map_array), expect_len << 10):
            map_array.append(255)

    def mapopen(self):
        try:
            with open(self.mappath, 'rb') as file:
                self.mapdata = bytearray(file.read())
        except OSError as error:
            print("File cannot be opened")
            sys.exit(1)


    def mapsplit(self):

        # check this is a .map file
        self.header = self.mapdata[0:6]

        if (self.header.decode() != "TD5map"):
            print('File is not a Td5 .map')
            sys.exit(1)

        # Read fuel map offset from the .map header
        fm_start = (self.mapdata[6] << 16) + \
                   (self.mapdata[7] << 8) +  \
                    self.mapdata[8]

        # Extract the Variant Map
        va = self.mapdata[9:fm_start]

        # Pad to 128Kb
        self.ffpad(va, 128)
        va_name = va[1024:1040:2].decode()

        # Extract the Fuel Map
        fm_length = (self.mapdata[fm_start] << 8) + \
                     self.mapdata[fm_start + 1]

        fm = self.mapdata[fm_start:fm_start+fm_length]

        # Pad map to exactly 16Kb
        self.ffpad(fm, 16)
        fm_name = fm[2:18].decode()
        self.writechunk(f'vm_{va_name}.bin', va)
        self.writechunk(f'fm_{fm_name}.bin', fm)
        print (f'\r\nSplit files written to {self.basepath}.\r\n')

if __name__ == '__main__':

    try:
        path = sys.argv[1]
        x = MapSplit(path)
        x.mapsplit()


    except IndexError as error:
        print("\r\nNo file specified.")
        print("Usage: python3 map_split,py /path/to/file.map\r\n")





