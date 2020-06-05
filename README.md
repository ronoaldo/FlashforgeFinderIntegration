# Flashforge Finder Cura utilities

This project contains several Cura slicer utilities that enhance the
experience for Flashforge Finder users.

# Install

## From Marketplace

Comming soon.

## Binary releases

Download from the .curapackages from Releases page and drop them into Cura.
After you restart Cura, plugins will be installed and you can save .GX files already.

In order to add Flashforge Finder, you need to use the Extensions ->
Flashforge Finder -> Install files menu entry. After that step, you can see FlashForge Finder
in the Add Printer dialog.

## From source

You can checkout the repository and use the GNU Make tool to build the .curapackage
files yourself:

	git clone https://github.com/ronoaldo/FlashforgeFinderIntegration
	cd FlashforgeFinderIntegration
	make

After that, there will be two .curapackage files in the build directory.
Follow the same steps as the "Binary Releases" section to use them.

Optionally, you can just copy the two folders under plugins/ directory
in your Cura configuration plugins direcotry. Go to "Help -> Show configuration directories"
menu in order to achieve that.

# About the support for .gx (xgcode) files

GX files are normal g-code but with an extra binary header used
by FlashForge Finder and similar printers.

The header contains a few data used by the printer firmware, such as
a thumbnail of the objet to print, print time, temperature and other
information.

This work is based on the ChituCodeWriter from https://github.com/Spanni26/ChituCodeWriter
and the detailed reverse-engineering description of the binary header
from this issue on Github.

# Whishlist 

* ~Add printer definition and submit plugin + printer definition to cloud~ Available here https://github.com/eskeyaar/Flashforge-Finder-
* Add send job/monitor support

# Binary xgcode 1.0 header

*Github user https://github.com/cme-linux made a great work reverse engineering
the binary header fields and shared this as a feature request for Slic3r.*

To extract .BMP from .GX in Linux:

	dd if=”file.gx” of=”file.bmp” skip=58 count=14454 iflag=skip_bytes,count_bytes

To extract G-Code from .GX in Linux:

	dd if=”file.gx” of=”file.gcode” skip=14512 iflag=skip_bytes

Byte offsets in the .GX file, as stated in this feature request, are 0-based.
All numbers are little-endian binary (2 or 4 bytes) unless specified to be ASCII plaintext.

Offsets through 0x1B seem to contain constant data:

* The string "xgcode 1.0" terminated with a newline & NUL.
* Then four 32-bit constants. (0, 58, 14512, 14512)
  * 58 is a pointer to the start of the bitmap
  * 14512 is a pointer to the start of the G-Code

Offsets 0x1C through 0x39 seem to contain the following variables.
The first three are 4 bytes; the other ones are 2 bytes.

 * 0x1C - print time in seconds, 4 bytes.
 * 0x20 - filament usage in mm, 4 bytes.
 * 0x24 - left extruder filament usage in mm, 4 bytes.
 * 0x28 - multi-extruder type; the latest FlashPrint version (1.23.0) seems to put 0x0B here
 * 0x2A - layer height, microns (for example, 180 means 0.18 mm)
 * 0x2C - unknown; maybe unused (zero)
 * 0x2E - number of perimeter shells
 * 0x30 - print speed, mm/s
 * 0x32 - platform temp, Celsius
 * 0x34 - extruder temp, Celsius 
 * 0x36 - left extruder temp, Celsius
 * 0x38 - unknown; maybe unused (zero)

FlashForge software/firmware uses that data these ways:

1. The printer itself uses only the preview bitmap & the 4-byte print duration.
2. FlashPrint has a "Slice Parameters" window that uses the 4-byte duration &
  filament length numbers. The other data in the "Slice Parameters" window comes
  from parsing the comments at the start of the G-Code, not from the binary header fields:
  (That means that Slic3r needs to generate these comments in the same format as FlashPrint.)

* Layer height in mm (not microns)
* Number of perimeter shells
* Fill density (percentage)
* Fill pattern (keywords I've seen are)
  * hexagon
  * triangle
  * line
  * 3dInfill
* Print speed
* Travel speed
* Extruder temp (1-extruder printers use the comment for right_extruder)
* Platform temp

After the header is the bitmap. This starts at offset 0x3A (decimal 58), ends @ offset 0x38AF.
The next offset, 0x38B0 (decimal 14512), is the start of the G-code.
The length of the bitmap is 0x3876 (decimal 14454) bytes.

The picture is in the ordinary .BMP format, uncompressed, 80 x 60 pixels (0x50 by 0x3C).
Some of the following parameters would be taken care of automatically by a .BMP library,
but I'll list these parameters anyway. The pixels start at byte offset 0x36 into the .BMP
section of the .GX file. There are 256 shades of gray, written as 24-bit color,
3 bytes per pixel, all 3 bytes having the same value.

The .BMP pixels-per-meter values are set to 0x1274 which is 120 dpi. BMP files contain
the pixel rows in bottom-to-top order.

The background is black and the 3D model is shown in an angled perspective view
(lines parallel to the coordinate axes converge slightly into the distance).

# Usefull links

* GX header reverse engineer discussion: https://github.com/slic3r/Slic3r/issues/4869
* Finder wire protocol: https://www.reddit.com/r/3Dprinting/comments/9lcdti/flashforge_finder_wireless_monitoring_tools/
* Finder web-based API implementation: https://github.com/01F0/flashforge-finder-api/tree/master/api

