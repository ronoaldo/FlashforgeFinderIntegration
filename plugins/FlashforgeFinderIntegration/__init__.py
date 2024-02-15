# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Description:  Install printer definition and other scripts for the Flashforge Finder printer. 
# License:  GPLv3

import sys

from UM.Logger import Logger
try:
    from . import Installer 
    _installer = Installer.Installer()
    _registry = { "extension": _installer }
except ImportError:
    _registry = None
    Logger.log("w", "Could not import GXWriter")

def getMetaData():
    return {}

def register(app):
    if _registry is not None:
        _installer.installFiles(showMessage=False)
        return _registry
    return {}
