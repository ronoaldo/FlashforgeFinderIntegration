import unittest
from gx import GX

test_gcode = """;FLAVOR:Marlin
;TIME:1066
;Filament used: 0.681442m
;Layer height: 0.12
;MINX:-14
;MINY:-14
;MINZ:0.2
;MAXX:14
;MAXY:14
;MAXZ:10.04
;TARGET_MACHINE.NAME:Flashforge Finder
;Generated with Cura_SteamEngine 5.6.0
M82 ;absolute extrusion mode
M140 S0
M104 S195.0 T0
M104 S0 T1
M107
G90
G28
M132 X Y Z A B
G1 Z50.00 F400
G161 X Y F3300
M6 T0
M907 X100 Y100 Z40 A80 B20
M108 T0
G1 Z.20 F400
G92 E0
G92 E0
G1 F1800 E-1.3
;LAYER_COUNT:83
;LAYER:0
M106 S255
G0 F3000 X14 Y9.314 Z0.2"""

class TestGX(unittest.TestCase):

    def test_from_gcode(self):
        gx = GX.from_gcode(test_gcode)
        result = gx.encode().decode('latin1')
        print("Resulting gcode: ", result)
        self.assertFalse(' S195.0 ' in result)
        self.assertTrue(' S195 ' in result)
        self.assertTrue('xgcode' in result)

if __name__ == '__main__':
    unittest.main()
