### FlashForge Cura Integration
These are various projects and info from around the net that I've gathered.

I've modified some to work with Cura 5 and bundled them together as I found it really hard to get my Adventurer 3 running in Cura.


# GXWriter
https://github.com/ronoaldo/FlashforgeFinderIntegration

This project is a fork of ronoaldo/FlashforgeFinderIntegration to add Cura 5 support.  

GXWriter adds the option to save your sliced gCode in GX format.  This is what most FlashForge printers need.

Features:
 - Includes a snapshot image which displays on the LCD
 - Includes print time, filament amount and other stats


### Install

Download from the .curapackages from Releases page and drag/drop into Cura.
After you restart Cura, plugins will be installed and you can save .GX files.


# Adventurer 3 Profile
https://github.com/KeltE/Flasforge_Adventurer-3_Cura_Definition

I have added the FlashForge Adventurer 3 profile allowing you to easily install it.

Features:
 - Nozzle options: of 0.3mm, 0.4mm and 0.6mm
 - Materials including PLA, ABS, PETG & TPU
 - Bed mesh so cura displays a FlashForge logo

### Install

Copy the "recourses" folder into the "\share\cura" directory in your cura installation.  For example, in Windows 10: C:\Program Files\Ultimaker Cura 5.0.0\share\cura\

The printer appears under the "FlashForge" manufacturer.

If you first test then use a generic PLA, ABS or PETG profile. Dreamer NX print speeds are added to these materials. What is otherwise Flashprint's initial settings are the same as Adventurer 3 speeds. Although I've changed the speeds to improve printing.


# Support & Testing
I have only tested with Cura 5.0.0-beta+1.  Your milage may vary - please open issues.  I'm keen to know if these work in Cura 4.x

# Usefull links

* FlashForge gCode guide & FlashPrint settings: https://github.com/AkiraNorthstar/FlashForge-Settings
