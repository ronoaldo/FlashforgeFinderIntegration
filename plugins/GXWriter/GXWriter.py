# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Description:  This plugin generates and inserts code including a image of the
#               slices part.
# License:  GPLv3

from UM.Mesh.MeshWriter import MeshWriter
from UM.MimeTypeDatabase import MimeTypeDatabase, MimeType
from cura.Snapshot import Snapshot
from cura.Utils.Threading import call_on_qt_thread
from UM.Logger import Logger
from UM.Scene.SceneNode import SceneNode #For typing.
from UM.PluginRegistry import PluginRegistry
from UM.i18n import i18nCatalog
catalog = i18nCatalog("cura")

import re
from io import StringIO, BufferedIOBase
from typing import cast, List
from . import gx

qt_version = 6
try:
    from PyQt6 import QtGui, QtCore
except ImportError:
    qt_version = 5
    from PyQt5 import QtGui, QtCore

# Helper function that extracts values from gcode to add to the binary header.
def getValue(line, key, default=None):
    if key not in line:
        return default
    else:
        subPart = line[line.find(key) + len(key):]
        m = re.search('^-?[0-9]+\\.?[0-9]*', subPart)
    try:
        return float(m.group(0))
    except:
        return default

# Implements a MeshWriter that creates the xgcode header before the gcode
# content.
class GXWriter(MeshWriter):

    def __init__(self):
        super().__init__(add_to_recent_files = False)
        self._snapshot = None
        MimeTypeDatabase.addMimeType(
            MimeType(
                name = "application/gx",
                comment = "GX (xgcode)",
                suffixes = ["gx"],
            )
        )

    @call_on_qt_thread 
    def write(self, stream, nodes: List[SceneNode], mode = MeshWriter.OutputMode.BinaryMode) -> bool:
        Logger.log("i", "Starting GXWriter.")
        if mode != MeshWriter.OutputMode.BinaryMode:
            Logger.log("e", "GXWriter does not support non-text mode.")
            self.setInformation(catalog.i18nc("@error:not supported", "GXWriter does not support non-text mode."))
            return False
        # Render in-memory gcode
        gcode_textio = StringIO() #We have to convert the g-code into bytes.
        gcode_writer = cast(MeshWriter, PluginRegistry.getInstance().getPluginObject("GCodeWriter"))
        success = gcode_writer.write(gcode_textio, None)
        # If gcode fails, we can't proceed.
        if not success: 
            self.setInformation(gcode_writer.getInformation())
            return False
        # Mofify gcode adding xgcode header binary information and image preview.
        result = self.modify(gcode_textio.getvalue())
        stream.write(result)
        Logger.log("i", "GXWriter done")
        return True

    def modify(self, gcode):
        try:
            # Initialize GX header variables
            g = gx.GX()
            g.gcode = gcode.encode('latin-1')
            # Parse values from original gcode
            self._parse_gcode_info(g, gcode)
            self._createSnapshot(g)
            return g.encode()
        except Exception:
            Logger.logException("w", "\n*** Failed to create gx file, defaulting to write regular gcode!!! ***\n")
            return gcode.encode('latin-1')

    def _parse_gcode_info(self, gx, gcode):
        for line in gcode.split("\n"):
            if line.startswith(';TIME:'):
                gx.print_time = int(getValue(line, ';TIME:', 0))
            if line.startswith(';Filament used:'):
                f = float(line.split(':')[1].split('m')[0].strip())
                f = f*100
                gx.filament_usage = int(f)
            if line.startswith(';Layer height:'):
                f = float(getValue(line, ';Layer height:', 0))
                f = f*1000
                gx.layer_height = int(f)
        Logger.log("i", "Updated values from struct =>", vars(gx))

    def _createSnapshot(self, g, *args):
        Logger.log("i", "Creating thumbnail image ...")
        try:
            # Convert the image to grayscale, and back to 24bits so it renders properly
            # in printer.
            qt_format_ctx = QtGui.QImage.Format if qt_version == 6 else QtGui.QImage
            qt_openmode_ctx = QtCore.QIODeviceBase.OpenModeFlag if qt_version == 6 else QtCore.QIODevice
            img = Snapshot.snapshot(width = 80, height = 60)
            img = img.convertToFormat(qt_format_ctx.Format_Grayscale8)
            img = img.convertToFormat(qt_format_ctx.Format_RGB666)
            # Converts the image into BMP byte array.
            arr = QtCore.QByteArray()
            buff = QtCore.QBuffer(arr)
            buff.open(qt_openmode_ctx.WriteOnly)
            img.save(buff, format="BMP")
            g.bmp = arr.data()
        except Exception:
            Logger.logException("w", "Failed to create snapshot image")
            g.bmp = gx._SAMPLE_BMP 
