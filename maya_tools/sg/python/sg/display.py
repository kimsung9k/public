import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


def position( pos ):
    
    displayObj = cmds.createNode( 'transform' )
    cmds.setAttr( displayObj + '.dh', 1 )

    if type( pos ) == type( [] ):
        pos = OpenMaya.MPoint( *pos )
    
    cmds.setAttr( displayObj + '.t', pos.x, pos.y, pos.z )