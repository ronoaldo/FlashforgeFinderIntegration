# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Description:  Install printer definition and other scripts for the Flashforge Finder printer.
# License:  GPLv3

import os
import shutil
import errno

from UM.i18n import i18nCatalog
from UM.Extension import Extension
from UM.Logger import Logger
from UM.Message import Message
from UM.PluginRegistry import PluginRegistry
from UM.Resources import Resources 

catalog = i18nCatalog("cura")

class Installer(Extension):

    def __init__(self):
        super().__init__()
        self.setMenuName("Flashforge Finder")
        self.addMenuItem(catalog.i18nc("@item:inmenu", "Install printer support"), self.installFiles)

    def installFiles(self, showMessage=True):
        Logger.log("i", "Installing printer support files (*.def.json, meshes and scripts) ...")

        # Local paths
        plugin_path = os.path.join(Resources.getStoragePath(Resources.Resources),
                "plugins", "FlashforgeFinderIntegration", "FlashforgeFinderIntegration")
        definitions_path = Resources.getStoragePath(Resources.DefinitionContainers)
        resources_path = Resources.getStoragePath(Resources.Resources)

        # Build src -> dst resource map
        resource_map = {
            "finder.def.json": {
                "src": os.path.join(plugin_path, "printer", "defs"),
                "dst": os.path.join(definitions_path)
            },
            "FF_finder_extruder_0.def.json": {
                "src": os.path.join(plugin_path, "printer", "extruders"),
                "dst": os.path.join(resources_path, "extruders")
            },
            "FlashforgeFinderBed.stl": {
                "src": os.path.join(plugin_path, "printer", "meshes"),
                "dst": os.path.join(resources_path, "meshes")
            },
            "finder_low.inst.cfg": {
                "src": os.path.join(plugin_path, "printer", "quality", "finder"),
                "dst": os.path.join(resources_path, "quality", "finder")
            },
            "finder_standard.inst.cfg": {
                "src": os.path.join(plugin_path, "printer", "quality", "finder"),
                "dst": os.path.join(resources_path, "quality", "finder")
            },
            "finder_high.inst.cfg": {
                "src": os.path.join(plugin_path, "printer", "quality", "finder"),
                "dst": os.path.join(resources_path, "quality", "finder")
            },
            "finder_hyper.inst.cfg": {
                "src": os.path.join(plugin_path, "printer", "quality", "finder"),
                "dst": os.path.join(resources_path, "quality", "finder")
            }
        }

        # Copy all missing files from src to dst
        restart_required = False
        for f in resource_map.keys():
            src_dir, dst_dir = resource_map[f]["src"], resource_map[f]["dst"]
            src = os.path.join(src_dir, f)
            dst = os.path.join(dst_dir, f)
            if not os.path.exists(dst):
                Logger.log("i", "Installing resource '%s' into '%s'" % (src, dst))
                if not os.path.exists(dst_dir):
                    try:
                        os.makedirs(dst_dir)
                    except OSError as e:
                        if e.errno == errno.EEXIST and os.path.isdir(dst_dir):
                            pass
                        else:
                            raise
                shutil.copy2(src, dst, follow_symlinks=False)
                restart_required = True

        # Display a message to the user
        if showMessage:
            if restart_required:
                msg = catalog.i18nc("@info:status", "Flashforge Finder files installed. Please restart Cura.")
            else:
                msg = catalog.i18nc("@info:status", "Flashforge Finder files were already installed.")
            Message(msg).show()

        return
