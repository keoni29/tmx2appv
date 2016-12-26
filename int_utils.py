import struct

# Convert int type to a bytearray of two bytes. Little endian
def int2b16(val):
	return struct.pack('<H',val)

# Convert int type to a bytearray of one byte.
def int2b8(val):
	return struct.pack('B',val)