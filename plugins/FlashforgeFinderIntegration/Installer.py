
import os
import shutil

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

    def installFiles(self):
        Logger.log("i", "Installing printer support files (*.def.json, meshes and scripts) ...")

        # Local paths
        plugin_path = os.path.join(Resources.getStoragePath(Resources.Resources),
                "plugins", "FlashforgeFinderIntegration", "FlashforgeFinderIntegration")
        definitions_path = Resources.getStoragePath(Resources.DefinitionContainers)
        resources_path = Resources.getStoragePath(Resources.Resources)

        # Build src -> dst resource map
        resource_map = {
            "finder.def.json": {
                "src": os.path.join(plugin_path, "printer", "definitions"),
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
            "PauseAtLayerFFFinder.py": {
                "src": os.path.join(plugin_path, "scripts"),
                "dst": os.path.join(resources_path, "scripts")
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
                    os.mkdir(dst_dir)
                shutil.copy2(src, dst, follow_symlinks=False)
                restart_required = True

        # Display a message to the user
        if restart_required:
            msg = catalog.i18nc("@info:status", "Flashforge Finder files installed. Please restart Cura.")
        else:
            msg = catalog.i18nc("@info:status", "Flashforge Finder files were already installed.")
        Message(msg).show()

        return
