#!/usr/bin/env python3
"""	to8xv: Convert any file to appVar
	(Python version) """

# TODO use commandline params

import int_utils as iu

TI83F_SIGNATURE = b'\x2A\x2A\x54\x49\x38\x33\x46\x2A\x1A\x0A\x00'
TI83F_COMMENT = b'AppVariable file'

VAR_START = b'\x0D\x00'
VAR_TYPEID = b'\x15'
VAR_NAME = b'HCMT'
VAR_VERSION = b'\x00'
VAR_FLAG = b'\x00'	# \x80 for archived. \x00 otherwise
varHeaderSize = 19

# Pad certain fields (TODO refactor)
TI83F_COMMENT += bytearray(42 - len(TI83F_COMMENT))
VAR_NAME += bytearray(8 - len(VAR_NAME))

fname_src = "HCMT.tmp"
# TODO base output filename on input filename if no
# output name is specified!
fname_dst = "HCMT.8xv"

src = open(fname_src, 'rb')
dst = open(fname_dst, 'wb')
VAR_DATA = src.read(-1)
dataSize = len(VAR_DATA)
varSize = dataSize + 2		# 2 bytes for variable header
totalSize = dataSize + varHeaderSize

APPV_HEADER = TI83F_SIGNATURE + TI83F_COMMENT + iu.int2b16(totalSize)
VAR_HEADER = VAR_START + iu.int2b16(varSize) + VAR_TYPEID + VAR_NAME + \
	VAR_VERSION	+ VAR_FLAG + iu.int2b16(varSize) + iu.int2b16(dataSize)

# Lower 16 bits of sum of all bytes in data segment and variable header combined
VAR_CHECKSUM = iu.int2b16(sum(VAR_HEADER) + sum(VAR_DATA))

dst.write(APPV_HEADER + VAR_HEADER + VAR_DATA + VAR_CHECKSUM);

src.close()
dst.close()
