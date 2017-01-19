import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.dag


def getConnectedFollicle( targetNode ):
    
    follicleNodes = cmds.listConnections( targetNode, type='follicle' )
    trNodes = cmds.listConnections( targetNode, type='transform' )
    
    if not follicleNodes and not trNodes: return None
    follicleNode  = None
    
    if follicleNodes:
        follicleNode = follicleNodes[0]
    else:
        for trNode in trNodes:
            shapeNodes = cmds.listRelatives( trNode, s=1, f=1 )
            if not shapeNodes: continue
            if cmds.nodeType( shapeNodes[0] ) != 'follicle': continue
            follicleNode = shapeNodes[0]

    return follicleNode




def getConnectedFolliclesAndJoints( joints ):
    
    jointChildren = sg.dag.getChildrenJoints(joints)
    joints += jointChildren
    
    jnts = []
    follicles = []
    for joint in joints:
        follicle = getConnectedFollicle( joint )
        if not follicle: continue
        follicles.append( cmds.listRelatives( follicle, p=1, f=1 )[0] )
        jnts.append( joint )
    
    return follicles, jnts




def setJointPosToConnectedFollicle( follicles, joints ):
    
    for i in range( len( joints ) ):
        folliclePos = cmds.getAttr( follicles[i] + '.wm' )
        cmds.xform( joints[i], ws=1, matrix= folliclePos )




def setAnimationFollicleConnectedJoints( joints ):
    
    start = cmds.playbackOptions( q=1, ast=1 )
    end   = cmds.playbackOptions( q=1, aet=1 )
    
    follicles, joints = getConnectedFolliclesAndJoints( joints )

    cmds.select( joints )
    for i in range( int(start), int(end + 1) ):
        cmds.currentTime( i )
        setJointPosToConnectedFollicle( follicles, joints )
        cmds.SetKey()
        

        