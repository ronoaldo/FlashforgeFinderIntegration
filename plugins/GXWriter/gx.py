#!/usr/bin/env python3
# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Description:  This module implements parsing and writing xgcode 1.0 files. 
# License:  GPLv3

import struct
import base64

class GX(object):
    """
    GX class implements the xgcode 1.0 decoding and encoding.
    """

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
        self.bmp = _SAMPLE_BMP
        self.gcode = b""

    def decode(self, data):
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

# base64 --wrap=80 testdata/cura.bmp | xclip -sel clip
_SAMPLE_BMP = base64.decodebytes("""
Qk12OAAAAAAAADYAAAAoAAAAUAAAADwAAAABABgAAAAAAEA4AADDDgAAww4AAAAAAAAAAAAAnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAUVFRxMTE7u7u/Pz89/f36Ojovb29VlZWAAAAAAAAAAAAAAAAAAAAAAAAAAAA
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
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAXV1d8fHx4ODghYWFNTU1S0tLf39/x8fHqKioAAAAAAAAAAAAAAAAAAAAAAAAAAAA
XFxc8fHx4ODggYGBMjIyWFhYkZGR39/fHBwcAAAAYGBg9PT03d3dc3NzKioqcHBw2tra9PT0YGBgAAAA
AAAA0NDQ4eHhAAAAFhYWVlZWoaGh8vLy4uLiMjIyAAAAAAAA0NDQ4eHhAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAATU1Nw8PD7u7u/Pz89vb25OTkra2tODg4AAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAT09PxcXF7+/v/Pz88/Pz2traiYmJAAAAAAAAAAAAWlpay8vL8/Pz/f398/PzzMzMWlpaAAAAAAAA
AAAA0NDQ/////////f399vb24ODgq6urIiIiAAAAAAAAAAAA0NDQ////////////////////6+vrAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
BAQEGhoaGhoaGhoaGhoaGhoaHh4eICAgJSUlJSUlICAgHBwcGhoaGhoaGhoaGhoaGhoaGhoaGhoaGhoa
GhoaFhYWExMTEBAQBAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
RUVFnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycZ2dnGBgYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
RUVFnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycZ2dnFhYWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
RUVFnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycXl5eGhoaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
RUVFnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycXl5eGhoaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
RUVFnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycXl5eGhoaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycZ2dnGBgYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
UlJSnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnZ2dn5+fn5+fn5+f
n5+fn5+fn5+fn5+fn5+fn5+fn5+fn5+fnZ2dnJycnJycXl5eHBwcAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
UVFRnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnp6eubm509PT4uLi6Ojo6urq6urq
6urq6urq6urq6urq6urq6urq6urq6urqvb29nJycnJycnJycY2NjGBgYAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
SEhInJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnZ2dvr6+7Ozs/v7+////////////////////
////////////////////////////////yMjInJycnJycnJycnJycWVlZGBgYAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
QUFBnJycnJycnJycnJycnJycnJycnJycnJycnJycnp6e0NDQ+fn5////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycWVlZCQkJAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
QUFBnJycnJycnJycnJycnJycnJycnJycnJycnZ2d2tra////////////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycnJycMTExAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
QUFBnJycnJycnJycnJycnJycnJycnJycnJyctLS0+/v7////////////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
QUFBnJycnJycnJycnJycnJycnJycnJycpqam8fHx/////////////////////v7+8fHx5ubm4eHh4eHh
4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHhubm5nJycnJycnJycnJycnJycnJycWlpaBAQEAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
REREnJycnJycnJycnJycnJycnJycnJycx8fH/////////////////////v7+3Nzcpqamnp6enZ2dnZ2d
nZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
R0dHnJycnJycnJycnJycnJycnJycnJyc39/f/////////////////v7+zc3NnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJyc7Ozs////////////////9/f3qKionJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJyc8/Pz////////////////6OjonZ2dnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJyc9/f3////////////////2tranJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycm5ub9fX1////////////////4ODgnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJyc8PDw////////////////8PDwn5+fnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycWlpaAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJyc5+fn////////////////+vr6tLS0nJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycX19fAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJyc1dXV////////////////////6enprKysnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycZGRkAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
S0tLnJycnJycnJycnJycnJycnJycnJycuLi4/v7+////////////////////8/Pz0tLSubm5sLCwr6+v
r6+vr6+vr6+vr6+vr6+vr6+vr6+vr6+vo6OjnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
R0dHnJycnJycnJycnJycnJycnJycnJycnJyc2NjY////////////////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
BQUFgoKCnJycnJycnJycnJycnJycnJycnJyco6Oj8vLy////////////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAGhoagoKCnJycnJycnJycnJycnJycnJycnJycurq68PDw////////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAGhoaeHh4nJycnJycnJycnJycnJycnJycnJycqqqq7e3t////////////////////////////
////////////////////////////////yMjInJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAHBwceHh4nJycnJycnJycnJycnJycnJycnJyco6Ojw8PD4+Pj8fHx+vr6/f39/v7+/v7+
/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+x8fHnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAHR0deHh4nJycnJycnJycnJycnJycnJycnJycnJycnZ2dn5+fpKSksLCwtra2tra2
tra2tra2tra2tra2tra2tra2tra2tra2pqamnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAISEheHh4nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAISEheHh4nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAHx8fbGxsnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHR0dYWFhnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycaGhoAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHR0dYWFhnJycnJycnJycnJycnJycnJycnJycnJycnJyc
nJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJycnJyclZWVjo6OVlZWAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA""".encode())

__usage="""Usage: gx.py COMMAND FILE

Where COMMAND can be:
    wrap    will add a basic GX header to the provided GCODE and print the result to stdout.
            Example: ./gx.py wrap testdata/cube.gcode > /tmp/cube.gx

    info    will print info from the GX header.
            Example: ./gx.py info testdata/cube.gx"""

if __name__ == "__main__":
    import sys, traceback
    cmd = sys.argv[1] if len(sys.argv)>1 else ""
    if cmd == "wrap":
        # Wraps the gcode file into a .gx one, output to stdout
        with open(sys.argv[2], 'rb') as fd:
            g = GX()
            g.gcode = fd.read()
            gcode_str = g.gcode.decode()
            # find print time from Cura
            for line in gcode_str.split('\n'):
                try:
                    if line.startswith(';TIME:'):
                        g.print_time = int(line.split(':')[1].strip())
                    if line.startswith(';Layer height: '):
                        f = float(line.replace(';Layer height: ', ''))
                        g.layer_height = int(f*1000)
                except:
                    sys.stderr.write('Error parsing g-code line [%s]' % line)
                    traceback.print_exc()
            sys.stdout.buffer.write(g.encode())
    elif cmd == "info":
        # Read the gx file and output the header information
        with open(sys.argv[2], 'rb') as fd:
            g = GX()
            g.decode(fd.read())
            print("File:", sys.argv[2])
            print("Print time:", g.print_time, 's')
            print("Layer height:", g.layer_height / 1000, 'mm')
            print("Perimeter shells:", g.shells)
            print("Bed temperature:", g.bed_temperature, 'C')
            print("Right extruder temp.:", g.print_temperature, 'C')
            print("Left extruder temp.:", g.print_temperature_left, 'C')
            print("Right extruder filament usage:", g.filament_usage, 'mm')
            print("Left extruder filament usage:", g.filament_usage_left, 'mm')
    else:
        print(__usage)
        sys.exit(1)
