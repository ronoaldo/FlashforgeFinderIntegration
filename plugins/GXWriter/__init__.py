# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Description:  This plugin generates and inserts code including a image of the
#               slices part.
# License:  GPLv3

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
                    "mime_type": "application/gx",
                    "mode": MeshWriter.OutputMode.BinaryMode,
                    "extension": "gx",
                    "description": i18n_catalog.i18nc("@item:inlistbox", "GX (gx)")
                }
            ]
        }
    }

def register(app):
    if "GXWriter.GXWriter" not in sys.modules:
        return {}
    
        
    return { "mesh_writer": GXWriter.GXWriter() }
