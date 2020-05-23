# tmx2appv
This program allows you to use tilemaps created using Tiled in games for the TI8x series of calculators.
Converts tilemap (.tmx) files to appVar (.8xv)

# Installation
Clone this repository including submodules (recursive.)
```
git clone --recursive https://github.com/keoni29/tmx2appv
```

Install dependencies
```
pip install pytmx pygame
```

# Usage
```
python tmx2appv.py [-h] [-o OUTPUT] [-n VARNAME] [--roomwidth ROOMWIDTH]
                   [--roomheight ROOMHEIGHT] [-v] [-s]
                   filename

positional arguments:
  filename

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
  -n VARNAME, --varname VARNAME
  --roomwidth ROOMWIDTH
  --roomheight ROOMHEIGHT
  -v, --verbose
  -s, --checksum        show appvar checksum
```

## Output
Output file name

## Varname
Under this name you will find the appvar in the calculator.

## Room width/height
Set the width and height of the room. Unit: tiles.

## Verbose
Show more details of the conversion process

## Checksum
Show the appvar checksum

# Credits
tmx2appv created by Koen van Vliet &copy; 2016-2020

pytmx created by Leif Theden 