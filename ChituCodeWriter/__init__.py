#Copyright (c) 2018 Ultimaker B.V.
#Cura is released under the terms of the LGPLv3 or higher.

import sys

from UM.Logger import Logger
try:
    from . import ChituCodeWriter
except ImportError:
    Logger.log("w", "Could not import ChituCodeWriter")

from UM.i18n import i18nCatalog #To translate the file format description.
from UM.Mesh.MeshWriter import MeshWriter #For the binary mode flag.

i18n_catalog = i18nCatalog("cura")

def getMetaData():
    if "ChituCodeWriter.ChituCodeWriter" not in sys.modules:
        return {}

    return {
        "mesh_writer": {
            "output": [
                {
                    "mime_type": "text/x-chitu-g-code",
                    "mode": MeshWriter.OutputMode.TextMode,
                    "extension": "gcode",
                    "description": i18n_catalog.i18nc("@item:inlistbox", "Chitu gcode")
                }
            ]
        }
    }

def register(app):
    if "ChituCodeWriter.ChituCodeWriter" not in sys.modules:
        return {}
    
        
    return { "mesh_writer": ChituCodeWriter.ChituCodeWriter() }