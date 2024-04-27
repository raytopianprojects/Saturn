# LODNodeTest1.py

""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	Description: DESCRIPTION_GOES_HERE

	$Author: pleopard $

	$Modtime: 04/17/07 1:15p $

	$Revision: 1 $

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """

# Standard imports

import sys

# Panda imports

from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
import direct.directbase.DirectStart
from direct.task import Task
from pandac.PandaModules import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def CreateTextLabel( \
        text,
        color,
        i,
        xStart=-1.3,
        yStart=0.95,
        yOffset=0.1,
        tFont=None
):
    if tFont == None:
        return OnscreenText( \
            text=text,
            pos=(xStart, yStart - yOffset * i),
            fg=color,
            mayChange=True,
            align=TextNode.ALeft
        )
    else:
        return OnscreenText( \
            text=text,
            pos=(xStart, yStart - yOffset * i),
            fg=color,
            mayChange=True,
            align=TextNode.ALeft,
            font=tFont
        )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

class World(DirectObject):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    def __init__(self):
        # *** Setup text displays
        textXStart = -1.3
        textYStart = 0.95
        textYOffset = 0.1
        self.mTitleDisplay = \
            CreateTextLabel(
                "LOD Node Test",
                (1.0, 1.0, 0.0, 1.0),
                1,
                textXStart,
                textYStart,
                textYOffset
            )
        self.mMessageDisplay = \
            CreateTextLabel(
                '> ',
                (0.0, 1.0, 0.0, 1.0),
                2,
                textXStart,
                textYStart,
                textYOffset
            )

        # *** Setup world dimensions
        maxWorldDim = 1000
        worldDims = [maxWorldDim, maxWorldDim, maxWorldDim]
        base.camLens.setNearFar(0.1, 2.5 * maxWorldDim)

        # *** Setup lighting
        lightLevel = 0.7
        lightPos = (0.0, -10.0, 10.0)
        lightHpr = (0.0, -26.0, 0.0)
        dlight = DirectionalLight('dlight')
        dlight.setColor(VBase4(lightLevel, lightLevel, lightLevel, 1))
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(lightHpr[0], lightHpr[1], lightHpr[2])
        dlnp.setPos(lightPos[0], lightPos[1], lightPos[2])
        render.setLight(dlnp)

        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight.upcastToPandaNode())

        # *** Setup scene
        base.setBackgroundColor(0.0, 0.1, 0.7, 1.0)

        # *** Setup events
        self.setupKeyBindings()

        # *** Setup models
        lodNode = NodePath(FadeLODNode('lod'))
        lodNode.reparentTo(render)

        lod0 = loader.loadModel("panda")
        lod0.set_scale(0.1, 0.1, 0.1)
        lod0.reparentTo(lodNode)
        lodNode.node().addSwitch(999999, 40)

        lod1 = loader.loadModel("teapot")
        lod1.set_scale(0.1, 0.1, 0.1)
        lod1.reparentTo(lodNode)
        lodNode.node().addSwitch(40, 30)

        lod2 = loader.loadModel("panda")
        lod2.set_scale(0.1, 0.1, 0.1)
        lod2.reparentTo(lodNode)
        lodNode.node().addSwitch(30, 20)

        lod3 = loader.loadModel("teapot")
        lod3.set_scale(0.1, 0.1, 0.1)
        lod3.reparentTo(lodNode)
        lodNode.node().addSwitch(20, 0)

        # *** Done, setup time update task
        taskMgr.add(self.timeUpdate, 'TimeUpdate')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    def toggleWireFrame(self):
        base.toggleWireframe()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    def toggleTexture(self):
        base.toggleTexture()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def snapShot(self):
        base.screenshot("Snapshot")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    def timeUpdate(self, task):
        cPos = base.camera.getPos()
        s = "Camera Pos : %12.4f %12.4f %12.4f" % (cPos[0], cPos[1], cPos[2])
        self.mMessageDisplay.setText(s)
        return Task.cont

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # Method name : setupKeyBindings
    #
    # Description:
    #
    #	Load and register key bindings
    #
    # Input(s):
    #
    #	None
    #
    # Output(s):
    #
    #	None
    #
    def setupKeyBindings(self):
        self.accept('p', self.snapShot)
        self.accept('w', self.toggleWireFrame)
        self.accept('t', self.toggleTexture)
        self.accept('escape', sys.exit)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

world = World()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Run the program

run()