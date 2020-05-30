# Copyright (c) 2020 Ronoaldo JLP 
# The PostProcessingPlugin is released under the terms of the AGPLv3 or higher.

from ..Script import Script

##  Pause at layer with M25.
class PauseAtLayerFFFinder(Script):
    def getSettingDataString(self):
        return """{
            "name": "Pause at layer (FlashForge Finder)",
            "key": "PauseAtLayerFFFinder",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "layer":
                {
                    "label": "Layer",
                    "description": "Layer number where a pause is added before it starts printing.",
                    "type": "str",
                    "default_value": ""
                }
            }
        }"""
    def execute(self, data):
        layer = self.getSettingValueByKey("layer")
        try:
            layer_num = int(layer) + 1
            gcode = "; PAUSE AT " + str(layer_num-1)
            gcode += "\nM25\n"
            data[layer_num] = data[layer_num] + gcode
        except:
            print("[ronoaldo] Invalid layer: '%s'", layer)
        return data
