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

import Actor
import libtoontownModules
from DepthTestProperty import *
from DepthTestTransition import *
from DepthWriteTransition import *

# Store a dictionary of actor files and their file path. This is used for loading animation.
ACTOR_REFERENCE = {
    # Classic Characters
    'mickey-1200': 'phase_3/models/char',
    'TT_MK-1500': 'phase_3/models/char',
    'minnie-1200': 'phase_4/models/char',
    'TT_D-1500': 'phase_6/models/char',
    'TT_G-1500': 'phase_6/models/char',
    'TT_MN-1500': 'phase_6/models/char',
    # Cogs
    'suitA-mod': 'phase_4/models/char',
    'suitB-mod': 'phase_4/models/char',
    'suitC-mod': 'phase_4/models/char',
    # Props
    'book-mod': 'phase_4/models/props',
    'portal-mod': 'phase_4/models/props',
    'stormcloud-mod': 'phase_4/models/props',
}

TOON_ACTOR_ELEMENTS = (
    ['dogSS_Shorts', 'dogMM_Shorts', 'dogLL_Shorts', 'dogSS_Skirt', 'dogMM_Skirt', 'dogLL_Skirt'],
    ['head', 'torso', 'legs'],
    ['1000']
)

def product(*args, **kwds):
    """
    Reimplemented from itertools, which isn't supported in Python 2.0

    Example Usage:
        product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111

    Returns:
        list: Cartesian product of input.
    """
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    return result

# Generate cartesian product of TOON_ACTOR_ELEMENTS and append to ACTOR_REFERENCE to store all Toon base models.
for element in product(*TOON_ACTOR_ELEMENTS):
    baseModel = '-'.join(element) # Join all parts with '-'
    ACTOR_REFERENCE[baseModel] = 'phase_3'


class ToontownBetaLoader:
    """
    Loader class for Toontown Beta files.
    """

    def loadFile(self, filePath):
        """
        Parses Toontown Beta file path to determine how it should be loaded.

        Args:
            filePath (string): Path to the file to load.
        """
        if filePath[-3:] == 'bam':
            # Handle Bam files, used for models and animation
            self.loadBam(filePath)
        elif filePath[-3:] == 'dna':
            # Handle DNA files, used for levels
            self.loadDNA(filePath)
        else:
            TypeError("Sorry, that file format isn't supported! Try dropping in a '.bam' or '.dna' file.")

    def loadBam(self, filePath):
        """
        Loads a Toontown Beta Bam file.

        Args:
            filePath (string): Path to Bam file to load.
        """
        isAnimation = 0

        # First, we need to check if this Bam file is an animation. It's definitely not animation
        if filePath[-8:-4] not in ('1500', '1000', '-500', '-250', '-800', '-400', '-mod'):
            for actorBase, actorPhase in ACTOR_REFERENCE.items():
                if filePath.find(actorBase[:-4]) > -1:
                    # If the beginning of the file name is found in the Actor Reference, treat
                    # this file as an animation
                    isAnimation = 1
                    geom = Actor.Actor(actorPhase + '/' + actorBase, {'anim': filePath})
                    geom.loop('anim')
                    break

        # If it's not an animation, just load a regular ol' bam file
        if not isAnimation:
            geom = base.loader.loadModel(filePath)

        geom.reparentTo(render)
        return geom

    def loadDNA(self, filePath, loadSky=True):
        """
        Loads a Toontown Beta DNA file.

        Args:
            filePath (string): Path to DNA file to load.
        """
        fileParts = filePath.split('/')
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
        geom = libtoontownModules.loadDNAFile(storage, filePath, 0, 0)
        render.attachNewNode(geom)

        # Load skybox if wanted
        if loadSky:
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

        return geom


# Get file path from command line argument
filePath = sys.argv[1]

# Start Beta loader, attempt to load file path
betaLoader = ToontownBetaLoader()
betaLoader.loadFile(filePath)

# Enable camera controls
base.useTrackball()

# Open main window
base.run()
