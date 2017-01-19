import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.get
import sg.shader
import sg.file
from functools import partial


def create( parent ):
    
    sels = [ sel for sel in cmds.ls( sl=1 ) if sg.get.nonIoMesh(sel) ]
    if not sels: return None
         
    cmds.menuItem( l="Set facing shader", p=parent, c=partial( lambda x, y : sg.shader.setFacingShader(x), sels ) )
