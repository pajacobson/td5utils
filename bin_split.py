#!/usr/bin/env python

# bin_split.py  splits Td5 NNN flash images (.bin or .ori) into component parts.

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


# Usage:
#   python  bin_parse.py bin_to_split.bin
#   split bin components are saved into the current working directory


import sys
import array


def writechunk(filename, bindata):
    with open(filename, "wb") as thisfile:
        thisfile.write(bindata)
        thisfile.close()


def bcdascii(bcd_array):
    result = array.array("B")
    for x in bcd_array:
        result.append((x >> 4) + 48)
        result.append((x & 15) + 48)
    return result.tobytes().decode()


path = sys.argv[1]

with open(path, "rb") as file:

    fdata = bytearray(file.read())

    # Byte swap to little endian byte ordering, if necessary
    if fdata[0] == 48:
        fdata[0::2], fdata[1::2] = fdata[1::2], fdata[0::2]

    bo = fdata[0:65536]  # 64Kb
    va = fdata[65536:196608]  # 128Kb
    vi = fdata[237568:245760]  # 8Kb
    fm = fdata[245760:262144]  # 16Kb

    file.close()


writechunk(bo[1024:1040:2].decode() + ".bin", bo)
writechunk(va[1024:1040:2].decode() + ".bin", va)

# Extract VIN for use as filename
designator = vi[0:11].decode()

serialnum = bcdascii(vi[11:14])


writechunk(designator + serialnum + ".bin", vi)

writechunk(fm[2:18].decode() + ".bin", fm)
