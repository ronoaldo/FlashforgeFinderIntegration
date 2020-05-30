# Author:   Ronoaldo JLP 
# Date:     May 24, 2020
# Description:  Install printer definition and other scripts for the Flashforge Finder printer. 
# License:  GPLv3

import sys

from UM.Logger import Logger
try:
    from . import Installer 
    _registry = { "extension": Installer.Installer() }
except ImportError:
    Logger.log("w", "Could not import GXWriter")

def getMetaData():
    return {}

def register(app):
    return _registry 
