#Copyright (c) 2018 Ultimaker B.V.
#Cura is released under the terms of the LGPLv3 or higher.

import sys

from UM.Logger import Logger
try:
    from . import GXWriter 
except ImportError:
    Logger.log("w", "Could not import GXWriter")

from UM.i18n import i18nCatalog #To translate the file format description.
from UM.Mesh.MeshWriter import MeshWriter #For the binary mode flag.

i18n_catalog = i18nCatalog("cura")

def getMetaData():
    if "GXWriter.GXWriter" not in sys.modules:
        return {}

    return {
        "mesh_writer": {
            "output": [
                {
                    "mime_type": "application/xgcode",
                    "mode": MeshWriter.OutputMode.BinaryMode,
                    "extension": "gx",
                    "description": i18n_catalog.i18nc("@item:inlistbox", "GX (xgcode)")
                }
            ]
        }
    }

def register(app):
    if "GXWriter.GXWriter" not in sys.modules:
        return {}
    
        
    return { "mesh_writer": GXWriter.GXWriter() }
