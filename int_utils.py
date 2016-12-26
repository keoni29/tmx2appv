# Hack to convert int type to a string of two bytes. Little endian
def int2b16(val):
	val_l = chr(val % 256)
	val_h = chr(int(val / 256))
	return (val_l + val_h).encode()

# Hack to convert int type to a string of one byte.
def int2b8(val):
	return chr(val % 256).encode()