#!/usr/bin/env python3

"""	tmx2appv: Convert tmx map to appVar
	(Designed to use with Hero Core ti83/4+ version)
	Author: Koen van Vliet <8by8mail@gmail.com> """

import pytmx as tm
import sys
from int_utils import *

# Name of the layer which holds our tilemap data
tile_layer_name = "Tile Layer 1"

# Define room size here
class Room:
	width = 11
	height = 8

class World:
	width = 0
	height = 0

# Bash colors (TODO make cross compatible)
class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# TODO: Change to variable instead of hardcoded filename
tmxdata = tm.TiledMap('map.tmx')

t = tmxdata.get_layer_by_name(tile_layer_name)

if t == None:
	print(bcol.FAIL + "Could not find a layer named", '"' + tile_layer_name + '"', bcol.ENDC)
	print("This layer is required for generating the appVar. Perhaps you misspelled its name?")
	sys.exit(1)

# TODO remove this line
## Uncomment to see all available attributes
#print(dir(t))

print("Found layer", '"' + t.name + '"')
print("Layer size =", t.width, "x", t.height, "tiles")

if t.width % Room.width or  t.height % Room.height:
	print(bcol.FAIL + "Layer width and height should be multiples of", Room.width, "and", Room.height, "respectively." + bcol.ENDC)
	sys.exit(1)

World.width = int(t.width / Room.width)
World.height = int(t.height / Room.height)

if World.width > 255 or World.height > 255:
	print(bcol.FAIL + "World is too large! Should not exceed 255x255 rooms" + bcol.ENDC)
	sys.exit(1)

print("Now converting to appVar!")

# TODO: Change to variable instead of harcoded fname
f = open('HCMT.tmp', mode='wb')

f.write(int2b8(World.width))
f.write(int2b8(World.height))

for wy in range(0, World.height):
	for wx in range(0, World.width):
		for ry in range(0, Room.height):
			for rx in range(0, Room.width):
				x = wx * Room.width + rx
				y = wy * Room.height + ry

				# TODO: This layer number should not be fixed!
				gid = tmxdata.get_tile_gid(x, y, 0)
				tileId = gid - 1

				f.write(int2b8(tileId))

f.close()