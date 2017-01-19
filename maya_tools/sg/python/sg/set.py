import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.check
import sg.convert


def worldMatrix( target, matrix ):
    if not sg.check.isTransformNode( target ): return None
    if type( matrix ) == type( OpenMaya.MMatrix() ):
        matrix = sg.convert.matrixToList( matrix )
    cmds.xform( target, matrix=matrix, ws=1 )



def localMatrix( target, matrix ):
    if not sg.check.isTransformNode(target) : return None
    if type( matrix ) == type( OpenMaya.MMatrix() ):
        matrix = sg.convert.matrixToList( matrix )
    cmds.xform( target, matrix=matrix )
    
    

def targetPosition( target, dest ):
    destMatrix = cmds.getAttr( dest + ".wm" )
    worldMatrix( target, destMatrix )
    
    
    
def translateDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['tx', 'ty', 'tz' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 0 )
            except:pass
            


def rotateDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['rx', 'ry', 'rz' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 0 )
            except:pass



def scaleDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['sx', 'sy', 'sz' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 1 )
            except:pass



def shearDefault():
    sels = cmds.ls( sl=1 )
    attrs = ['shearXY', 'shearXZ', 'shearYZ' ]
    for sel in sels:
        for attr in attrs:
            try:cmds.setAttr( sel + "." + attr, 0 )
            except:pass



def transformDefault():
    
    translateDefault()
    rotateDefault()
    scaleDefault()
    shearDefault()
    
    

def allDefault():
    
    for sel in cmds.ls( sl=1 ):
        attrs = cmds.listAttr( sel, k=1 )
        for attr in attrs:
            defaultValue = cmds.attributeQuery( attr, node=sel, ld=1 )[0]
            try:cmds.setAttr( sel + '.' + attr, defaultValue )
            except: pass
        
    
    

