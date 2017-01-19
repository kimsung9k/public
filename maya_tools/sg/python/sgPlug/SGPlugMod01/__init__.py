commandString = """
import maya.cmds
import maya.mel

if not maya.cmds.pluginInfo( "SGMPlugMod01", q=1, l=1 ):
    maya.cmds.loadPlugin("SGMPlugMod01")
maya.cmds.refresh()

maya.mel.eval( "SGMPlugMod01Command -st;select -cl;" )

import sg.PlugMod01
exectarget = '/'.join( sgPlug.SGPlugMod01.__file__.replace("\\\\", "/").split("/")[:-1] ) + "/execfunction.py"
execfile( exectarget )
"""

import maya.cmds as cmds

def setTool( evt=0 ):
    print commandString
    cmds.evalDeferred( commandString )
