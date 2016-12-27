#!/usr/bin/env python3

"""	tmx2appv: Convert tmx map to appVar
	(Designed to use with Hero Core ti83/4+ version)
	Author: Koen van Vliet <8by8mail@gmail.com> """

import pytmx as tm
import sys
import argparse
import os
from to8xv import ti83f
from to8xv.ti83f import int2b8

# Name of the layer which holds our tilemap data
#TODO argparse?
tile_layer_name = "Tile Layer 1"

# TODO: Do these really need to be inside of a class? {
class Room:
	width = 11
	height = 8

class World:
	width = 0
	height = 0
# }

# Bash colors (TODO make cross compatible)
class bcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

parser = argparse.ArgumentParser()
parser.add_argument("filename", type=str)
parser.add_argument("-o", "--output", type=str)
parser.add_argument("-n", "--varname", type=str)
parser.add_argument("--roomwidth", type=int)
parser.add_argument("--roomheight", type=int)
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-s", "--checksum", action="store_true", help="show appvar checksum")

args = parser.parse_args()

fname_src = args.filename
if args.output:
	fname_dst = args.output
else:
	fname_dst = os.path.splitext(fname_src)[0] + '.8xv'

if args.varname:
	varName =  args.varname.encode()
else:
	varName = b'MYVAR'

if args.roomwidth:
	Room.width = args.roomwidth

if args.roomheight:
	Room.height = args.roomheight

tmxdata = tm.TiledMap(fname_src)
t = None
i = 0
for layer in tmxdata.layers:
	if layer.name == tile_layer_name:
		if args.verbose:
			print(bcol.OKBLUE + "Layer", i, "named", '"' + layer.name +'"', "found!" + bcol.ENDC)
		if t == None:
			t = layer
			LAYER_NUMBER = i
		else:
			print(bcol.WARNING + "Warning: Duplicate layers are ignored!" + bcol.ENDC)
	else:
		if args.verbose:
			print("Layer", i, "named", '"' + layer.name +'"', "ignored")
	i += 1

if t == None:
	print(bcol.FAIL + "Could not find a layer named", '"' + tile_layer_name + '"', bcol.ENDC)
	print("This layer is required for generating the appVar. Perhaps you misspelled its name?")
	sys.exit(1)

if args.verbose:
	print("Total size =", t.width, "x", t.height, "tiles")

if t.width % Room.width or  t.height % Room.height:
	print(bcol.FAIL + "Layer width and height should be multiples of", Room.width, "and", Room.height, "respectively." + bcol.ENDC)
	sys.exit(1)

World.width = int(t.width / Room.width)
World.height = int(t.height / Room.height)

if World.width > 255 or World.height > 255:
	print(bcol.FAIL + "World is too large! Should not exceed 255x255 rooms" + bcol.ENDC)
	sys.exit(1)

if args.verbose:
	print("Now converting to appVar!")

tileData = int2b8(World.width)
tileData += int2b8(World.height)

for wy in range(0, World.height):
	for wx in range(0, World.width):
		for ry in range(0, Room.height):
			for rx in range(0, Room.width):
				x = wx * Room.width + rx
				y = wy * Room.height + ry
				# TODO: Unused tiles are apparently excluded from global tile ID pool.
				# This is a temporary workaround for this issue. Can only be used in this
				# specific case
				# TODO: Use tmxdata.gidmap
				image = tmxdata.get_tile_image(x, y, LAYER_NUMBER)
				tx = int(image[1][0] / tmxdata.tilewidth)
				ty = int(image[1][1] / tmxdata.tileheight)
				# TODO: Stop using hardcoded tileset width. Instead use tile gid to resolve tile ID
				tileset_width = 16
				tileId = ty * tileset_width + tx

				tileData += int2b8(tileId)

with open(fname_src, 'rb') as src:
	var = ti83f.Var(varName, archived=True, data = tileData)

with open(fname_dst, 'wb') as dst:
	appv = ti83f.AppVar()
	appv.add(var)

	dst.write(bytes(appv))
if args.verbose or args.checksum:
	print("Checksum :", hex(appv.checksum()))

if args.verbose:
	print(bcol.OKGREEN + "Done converting. Written output to ", '"' + fname_dst + '"' + bcol.ENDC)