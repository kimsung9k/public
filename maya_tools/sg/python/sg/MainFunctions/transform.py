import maya.cmds as cmds
import sg.transform



def freezeJoint( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.freezeJoint( sels )



def freezeByParent( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.freezeByParent( sels )




def setJointOrientZero( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.setJointOrientZero( sels )



def makeCenter( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.makeCenter( sels )



def makeMirror( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.duplicateMirror( sels )



def setOrientAsTarget( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.setOrientAsTarget( sels[:-1], sels[-1] )


def setTransformAsTarget( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.transform.setTransformAsTarget( sels[:-1], sels[-1] )


def setOrientByChild( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    for sel in sels:
        sg.transform.setOrientByChild( sel )