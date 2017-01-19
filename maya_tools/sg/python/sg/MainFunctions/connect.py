import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.connect



def tx( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.tx( sels[0], sels[1:] )


def ty( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.ty( sels[0], sels[1:] )


def tz( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.tz( sels[0], sels[1:] )
    


def rx( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.rx( sels[0], sels[1:] )


def ry( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.ry( sels[0], sels[1:] )


def rz( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.rz( sels[0], sels[1:] )


def sx( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.sx( sels[0], sels[1:] )


def sy( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.sy( sels[0], sels[1:] )


def sz( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.sz( sels[0], sels[1:] )



def lookAt( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.lookAtConnect( sels[0], sels[1:] )
    
    

def blendTwoMatrixConnect( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.blendTwoMatrixConnection( sels[0], sels[1], sels[2] )  



def blendMatrixConnect( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.blendMatrixConnect( sels[:-1], sels[-1] )



def blendMatrixConnect_mo( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.blendMatrixConnect( sels[:-1], sels[-1] )



def constraint_point( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.constraint_point( sels[0], sels[1:] )
    
    

def constraint_orient( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.constraint_orient( sels[0], sels[1:] )
    


def constraint_parent( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.constraint_parent( sels[0], sels[1:] )



def optimizeConnection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.opptimizeConnection( sels )
    

def parentToConstrainedObject( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.parentToConstrainedObject(sels[0], sels[1])



def getLocalDcmp( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.getLocalDcmp( sels[0], sels[1] )




def getLookAtConnectNode( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.getLookAtConnectNode( sels[0], sels[1] )



def getLocalDcmpDistance( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.connect.getLocalDcmpDistance( sels[0], sels[1] )


def getAngle( evt=0 ):
    
    sels = sg.listNodes( sl=1 )
    for sel in sels:
        sg.connect.getAngle( sel )

