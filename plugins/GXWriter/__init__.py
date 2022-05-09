# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Updates:  Matthew Tong
# Date:     May 9, 2022

# Description:  This plugin generates and inserts code including a image of the
#               slices part.
# License:  GPLv3

import os, json, sys

from . import GXWriter

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("cura")

from UM.Version import Version
from UM.Application import Application
from UM.Logger import Logger

from UM.Mesh.MeshWriter import MeshWriter

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

    if __matchVersion():
        return {"mesh_writer": GXWriter.GXWriter()}
    else:
        Logger.log("w", "Plugin not loaded because of a version mismatch")
        return {}


def __matchVersion():
    cura_version = Application.getInstance().getVersion()
    if cura_version == "master":
        Logger.log("d", "Running Cura from source; skipping version check")
        return True
    if cura_version.startswith("Arachne_engine"):
        Logger.log("d", "Running Cura Arachne preview; skipping version check")
        return True

    cura_version = Version(cura_version)
    cura_version = Version([cura_version.getMajor(), cura_version.getMinor()])

    # Get version information from plugin.json
    plugin_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "plugin.json"
    )
    try:
        with open(plugin_file_path) as plugin_file:
            plugin_info = json.load(plugin_file)
            minimum_cura_version = Version(plugin_info["minimum_cura_version"])
            maximum_cura_version = Version(plugin_info["maximum_cura_version"])
    except:
        Logger.log("w", "Could not get version information for the plugin")
        return False

    if cura_version >= minimum_cura_version and cura_version <= maximum_cura_version:
        return True
    else:
        Logger.log(
            "d",
            "This version of the plugin is not compatible with this version of Cura. Please check for an update.",
        )
        return False
