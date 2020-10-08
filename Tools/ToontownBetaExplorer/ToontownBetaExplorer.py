# =============================================================================
# Toontown Beta Explorer
# Author: Joey Ziolkowski
# Date: 10/7/2020
#
# Purpose: Loads Bam and DNA files from Toontown Online Beta (v1.0.5) for
#          easy viewing. This tool must be ran with the same Python version
#          bundled with the Toontown Online Beta install. See README for
#          instructions.
#
# Usage: BETA_INSTALL_PATH/python.exe -O ToontownBetaExplorer.py "path/to/file.ext"
# =============================================================================

# If you moved the 1.0.5-install directory or downloaded it separately,
# update this variable with the correct location on your computer.
BETA_INSTALL_PATH = "../../Releases/ToontownBeta/1.0.5-install"

# Add paths to search for for beta files
import sys
sys.path.append(BETA_INSTALL_PATH + "/phase_2/lib/py")
sys.path.append(BETA_INSTALL_PATH + "/phase_3/lib/py")

import libdtoolconfig
import libpandaexpress
import libtoontownModules
from DepthTestProperty import *
from DepthTestTransition import *
from DepthWriteTransition import *
from libpandaexpressModules import *
from ShowBase import ShowBase

base = ShowBase()

# Get file path from argument
filePath = sys.argv[1]
fileParts = filePath.split('/')

if filePath[-3:] == 'bam':
    # Just loading a regular ol' bam file. No fancy tricks here.
    geom = base.loader.loadModel(filePath)
    geom.reparentTo(render)
elif filePath[-3:] == 'dna':
    if fileParts[-1].find('storage') > -1:
        raise ValueError("Storage files just contain model definitions for other DNA files, so there's nothing to display! Try a non-storage DNA file.")

    # Load global DNA storage files
    storage = libtoontownModules.DNAStorage()
    libtoontownModules.loadDNAFile(storage, 'phase_4/dna/storage.dna', 0, 0)
    libtoontownModules.loadDNAFile(storage, 'phase_5/dna/storage_town.dna', 0, 0)

    # Load phase-specific DNA storage files, and set sky based on area
    if filePath.find('phase_4') > -1 or filePath.find('phase_5') > -1:
        # Toontown Central
        skyFile = 'phase_4/models/props/TT_sky'
        libtoontownModules.loadDNAFile(storage, 'phase_4/dna/storage_TT.dna', 0, 0)
        libtoontownModules.loadDNAFile(storage, 'phase_4/dna/storage_TT_sz.dna', 0, 0)
        libtoontownModules.loadDNAFile(storage, 'phase_5/dna/storage_TT_town.dna', 0, 0)
    elif filePath.find('phase_6') > -1:
        if filePath.find('donalds') > -1:
            # Donald's Dock
            skyFile = 'phase_6/models/props/BR_sky'
            libtoontownModules.loadDNAFile(storage, 'phase_6/dna/storage_DD.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_6/dna/storage_DD_sz.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_6/dna/storage_DD_town.dna', 0, 0)
        elif filePath.find('minnies') > -1:
            # Minnie's Melodyland
            skyFile = 'phase_6/models/props/MM_sky'
            libtoontownModules.loadDNAFile(storage, 'phase_6/dna/storage_MM.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_6/dna/storage_MM_sz.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_6/dna/storage_MM_town.dna', 0, 0)
    elif filePath.find('phase_8') > -1:
        if filePath.find('burrrgh') > -1:
            # The Brrrgh
            skyFile = 'phase_6/models/props/BR_sky'
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_BR.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_BR_sz.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_BR_town.dna', 0, 0)
        elif filePath.find('daisys') > -1:
            # Daisy Gardens
            skyFile = 'phase_4/models/props/TT_sky'
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_DG.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_DG_sz.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_DG_town.dna', 0, 0)
        elif filePath.find('donalds') > -1:
            # Donald's Dreamland
            skyFile = 'phase_8/models/props/DL_sky'
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_DL.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_DL_sz.dna', 0, 0)
            libtoontownModules.loadDNAFile(storage, 'phase_8/dna/storage_DL_town.dna', 0, 0)

    # Load main DNA file
    dnaGeom = libtoontownModules.loadDNAFile(storage, filePath, 0, 0)
    render.attachNewNode(dnaGeom)

    # Load skybox
    sky = base.loader.loadModel(skyFile)
    # Normally we would use CompassEffect to unlock the sky from camera rotation, but that wasn't
    # available in Panda3D until 2002. Need to figure out what Disney's method was prior to that effect.
    sky.reparentTo(camera)
    sky.setZ(-30)
    # Disable depth on skybox (The fun 2001 way of doing it!) so that it doesn't render over the scene
    dw = DepthWriteTransition.off()
    dt = DepthTestTransition(DepthTestProperty.MNone)
    sky.arc().setTransition(dw, 1)
    sky.arc().setTransition(dt, 1)
    sky.setBin('background', -100)
else:
    TypeError("Sorry, that file format isn't supported! Try dropping in a '.bam' or '.dna' file.")

# Enable camera controls
base.useTrackball()

# Open main window
base.run()
