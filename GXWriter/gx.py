#!/usr/bin/env python

import struct

class GX(object):

    def __init__(self):
        # Constants
        self.version = b"xgcode 1.0\n\0"
        self.bitmap_start, self.gcode_start = 58, 14512
        # Values from the print job
        self.print_time = 0
        self.filament_usage, self.filament_usage_left = 0, 0
        self.multi_extruder_type = 11 
        self.layer_height = 0
        self.shells = 0
        self.print_speed = 0
        self.bed_temperature = 0
        self.print_temperature, self.print_temperature_left = 0, 0
        self.bmp = b""
        self.gcode = b""

    def decode(self, data):
        # Parse given data
        self._decode(data)
    
    def encode(self):
        return self._encode()

    def _decode(self, data):
        self._data = bytes(data)
        # First line must be "xgcode 1.0\n"
        rows = self._data.split(b'\n')
        if len(rows) < 2:
            print("gx.py: less than 2 rows")
            return
        if rows[0] != b"xgcode 1.0":
            print("invalid header")
            return
        # Header is first line + \n + second line
        header = rows[0] + b'\n' + rows[1] + b'\n'
        self._header = header
        # Version information
        offset = 0
        self.version = struct.unpack_from("<12s", header, offset)[0]
        offset = len(self.version)
        # Header constants
        cons = struct.unpack_from("<4l", header, offset)
        self.bitmap_start = cons[1]
        self.gcode_start = cons[2]
        # Metadata
        offset = 0x1C
        t, f1, f2, met = struct.unpack_from("<lllh", header, offset)
        self.print_time = t
        self.filament_usage, self.filament_usage_left = f1, f2
        self.multi_extruder_type = met
        offset = 0x2A
        lh, _, sh, spd, bt, et1, et2 = struct.unpack_from("<7h", header, offset)
        self.layer_height = lh
        self.shells = sh
        self.print_speed = spd
        self.bed_temperature = bt
        self.print_temperature = et1
        self.print_temperature_left = et2
        # Bitmap
        self.bmp = self._data[58:14512]
        if len(self.bmp) != 14454:
            raise "BMP length is invalid: %d" % len(self.bmp)
        self.gcode = self._data[self.gcode_start:]

    def _encode(self):
        buff = (self.version)
        buff+= struct.pack("<4i",
                0,
                self.bitmap_start,
                self.gcode_start,
                self.gcode_start
        )
        buff+= struct.pack("<iiih",
                self.print_time,
                self.filament_usage,
                self.filament_usage_left,
                self.multi_extruder_type,
        )
        buff+= struct.pack("<8h",
                self.layer_height,
                0,
                self.shells,
                self.print_speed,
                self.bed_temperature,
                self.print_temperature,
                self.print_temperature_left,
                1,
        )
        buff+= self.bmp
        buff+= self.gcode
        return buff

