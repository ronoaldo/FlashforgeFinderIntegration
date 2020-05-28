# Cura GX writer

GX file implementation for Cura. GX files are normal g-code but with an extra
binary header used for FlashForge Finder and similar printers.

The header contains a few data used by the printer firmware, such as
a thumbnail of the objet to print, print time, temperature and other
information.

This work is based on the ChituCodeWriter from https://github.com/Spanni26/ChituCodeWriter.

# Install

1. download the latest release from here 
2. unzip it 
4. find your local plugin dir (start Cura -> Help -> Show configuration folder)
3. copy the folder "GXWriter" into the "plugins" dir 
4. restart cura

To inlcude the GX code into the gcode slice as normal an save as "GX file"

Have Fun!

# TODO

* Add printer definition and submit plugin + printer definition to cloud
* Add send job/monitor support

# Links

https://www.reddit.com/r/3Dprinting/comments/9lcdti/flashforge_finder_wireless_monitoring_tools/
https://github.com/01F0/flashforge-finder-api/tree/master/api

