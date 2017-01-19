import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.dag


def updateSkeleton( mesh, jointGrp ):
    
    meshShape = sg.dag.getShape( mesh )
    
    follicles = cmds.listConnections( meshShape , type='follicle', s=0, d=1 )
    
    returnJnts = []
    for follicle in follicles:
        cons = cmds.listConnections( follicle+'.wm' )
        if cons: continue
        
        jnt = cmds.createNode( 'joint' )
        mm = cmds.createNode( 'multMatrix' )
        dcmp = cmds.createNode( 'decomposeMatrix' )
        
        cmds.connectAttr( follicle + '.wm', mm + '.i[0]' )
        cmds.connectAttr( jnt + '.pim', mm + '.i[1]' )
        cmds.connectAttr( mm + '.o', dcmp + '.imat' )
        cmds.connectAttr( dcmp + '.ot', jnt + '.t' )
        cmds.connectAttr( dcmp +'.or', jnt + '.r' )
        
        jnt = cmds.parent( jnt, jointGrp )[0]
        returnJnts.append( jnt )
    
    return returnJnts