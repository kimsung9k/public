import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

import sg.convert


def createFollicleOnMeshByPositions( points, baseMesh ):
    
    points = sg.convert.singleToList( points )
    
    nonIoMeshs = sg.get.nonIoMesh( baseMesh )
    if not nonIoMeshs: return None
    dagPath = sg.base.getDagPath( nonIoMeshs[0] )
    
    if dagPath.node().apiTypeStr() != "kMesh": return None
    
    fnMesh = OpenMaya.MFnMesh( dagPath )
    
    follicles = []
    for point in points:
        uvPtr = sg.base.getFloat2Ptr()
        fnMesh.getUVAtPoint( point, uvPtr, OpenMaya.MSpace.kWorld )
        uvValues = sg.util.getListFromFloat2Ptr( uvPtr )
        
        follicle = cmds.createNode( 'follicle' )
        follicleTr = cmds.listRelatives( follicle, p=1, f=1 )[0]
        
        cmds.connectAttr( fnMesh.partialPathName() + '.outMesh', follicle+'.inputMesh' )
        cmds.connectAttr( fnMesh.partialPathName() + '.worldMatrix[0]', follicle+'.inputWorldMatrix' )
        cmds.connectAttr( follicle + '.outTranslate', follicleTr + '.t' )
        cmds.connectAttr( follicle + '.outRotate', follicleTr + '.r' )
        
        cmds.setAttr( follicle + '.parameterU', uvValues[0] )
        cmds.setAttr( follicle + '.parameterV', uvValues[1] )
        follicles.append( follicleTr )
    
    return follicles