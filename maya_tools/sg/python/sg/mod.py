import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.check
import sg.set
import sg.convert
import sg.format
import sg.shader
import sg.matrix
import sg._print
import sg.base
import sg.value



def deleteMeshComponent( mesh, indices, componentType, *args  ):
    
    if not sg.check.isMesh( mesh ):
        cmds.error( "%s is not 'mesh'." % mesh )
    
    indices = sg.convert.MIntArray(indices)
    if not indices.length():
        cmds.error( "indices is empty or not convertable." );
    
    dagPath = sg.base.getDagPath( mesh )        
    singleComp = OpenMaya.MFnSingleIndexedComponent()
    oComp = singleComp.create( componentType )
    singleComp.addElements( indices )
    
    cmds.select( cl=1 )
    OpenMaya.MGlobal.select( dagPath, oComp )
    cmds.delete()



def deleteSymmetryOpposite( target, symvector = OpenMaya.MVector( 1,0,0 ),*args ):
    
    import copy
    import math
    
    meshs = sg.get.nonIoMesh( target )
    if not meshs:
        cmds.error("%s has no 'mesh'." % target )
    
    bb = sg.format.BoundingBox( target )
    maxValue = sg.value.maxValue( [math.fabs(OpenMaya.MVector( bb.min() ) * symvector), math.fabs(OpenMaya.MVector( bb.max() ) * symvector)] )
    
    symvector *= -1
    
    if  maxValue < 0.001:
        cmds.error("Positive Bound Too Small" );
    
    zvector = OpenMaya.MVector( 0,0,1 )
    rot = zvector.rotateTo( symvector ).asEulerRotation().asVector()
    cmds.polyCut( target, ch=0, pc=[0,0,0], ro = [math.degrees(rot.x),math.degrees(rot.y),math.degrees(rot.z)] )
    
    sgformatMesh= sg.format.Mesh( meshs[0] )
    
    targetIndices = OpenMaya.MIntArray()
    for i in range( sgformatMesh.numPolys ):
        centerPoint = sgformatMesh.getPolygonCenter( i )
        if OpenMaya.MVector( centerPoint ) * symvector < 0 : targetIndices.append( i )
     
    if targetIndices.length(): deleteMeshComponent( meshs[0], targetIndices, OpenMaya.MFn.kMeshPolygonComponent )



def makeSymmetryMesh( target, symvector = OpenMaya.MVector( 1,0,0 ),*args ):
    
    import copy
    
    duVector = copy.copy(symvector)
    deleteSymmetryOpposite( target, duVector, *args )
    
    meshs = sg.get.nonIoMesh( target )
    sgformatMesh= sg.format.Mesh( meshs[0] )
    
    duNode1 = cmds.createNode('transform')
    duNode2 = cmds.createNode('transform')
    fnMesh = OpenMaya.MFnMesh()
    fnMesh.copy( sg.base.getMObject(meshs[0]), sg.base.getMObject(duNode1) )
    fnMesh.copy( sg.base.getMObject(meshs[0]), sg.base.getMObject(duNode2) )
    
    mirrorMatrix = sg.matrix.getMirrorMatrix( sgformatMesh.matrix, symvector )
    sg.set.worldMatrix( duNode1, sgformatMesh.matrix )
    sg.set.worldMatrix( duNode2, mirrorMatrix )
    
    resultNode = cmds.polyUnite( duNode1, duNode2, ch=0, mergeUVSets=1 )[0]
    cmds.polyMergeVertex( resultNode,  d=0.0001, ch=0 )
    cmds.refresh()
    
    sg.shader.copyShader( target, resultNode )
    
    targetTransform = sg.dag.getTransform( target )
    cmds.delete( targetTransform )
    
    resultNode = cmds.rename( resultNode, targetTransform )
    cmds.select( resultNode )
    
    return targetTransform




def projectMeshToMesh( target, base, direction = OpenMaya.MVector(0,0,-1),*args  ):
    
    targetShapes = sg.get.nonIoMesh( target )
    baseShapes   = sg.get.nonIoMesh( base )
    
    if not len( targetShapes ) or not len( baseShapes ): return None
    
    dagTarget = sg.base.getDagPath( targetShapes[0] )
    dagBase   = sg.base.getDagPath( baseShapes[0] )
    
    fnMeshTarget = OpenMaya.MFnMesh( dagTarget )
    points = OpenMaya.MPointArray()
    fnMeshTarget.getPoints( points, OpenMaya.MSpace.kWorld )
    
    fnMeshBase = OpenMaya.MFnMesh( dagBase )
    baseMatrix = dagBase.inclusiveMatrix()
    baseMatrixInverse= dagBase.inclusiveMatrixInverse()
    
    meshName = targetShapes[0]
    
    if direction.length() == 0: 
        pointSrcs, rays = sg.matrix.getCamRaysFromWorldPoints( points )
        for i in range( points.length() ):
            resultPoints = OpenMaya.MPointArray()
            if not fnMeshBase.intersect( pointSrcs[i] * baseMatrixInverse, rays[i] * baseMatrixInverse, resultPoints ): continue
            resultPoint = resultPoints[0] * baseMatrix
            cmds.move( resultPoint.x, resultPoint.y, resultPoint.z, meshName + ".vtx[%d]" % i, ws=1  )
    else:
        direction *= baseMatrixInverse
        for i in range( points.length() ):
            resultPoints = OpenMaya.MPointArray()
            if not fnMeshBase.intersect( points[i] * baseMatrixInverse, direction, resultPoints ): continue
            resultPoint = resultPoints[0] * baseMatrix
            cmds.move( resultPoint.x, resultPoint.y, resultPoint.z, meshName + ".vtx[%d]" % i, ws=1  )
    


def averageNormal( *args ):
    
    for dagPath, vtxList in sg.selection.selectedVertices():
        fnMesh = OpenMaya.MFnMesh( dagPath )
        
        points = OpenMaya.MPointArray()
        normals = OpenMaya.MFloatVectorArray()
        
        fnMesh.getPoints( points )
        fnMesh.getVertexNormals( True, normals )
        
        itMeshVtx = OpenMaya.MItMeshVertex( dagPath )
        
        resultPoints = []
        for i in range( vtxList.length() ):
            pPrevIndex = sg.base.getIntPtr()
            itMeshVtx.setIndex( vtxList[i], pPrevIndex )
            conVertices = OpenMaya.MIntArray();
            itMeshVtx.getConnectedVertices(conVertices)
            
            bb = OpenMaya.MBoundingBox()
            for j in range( conVertices.length() ):
                bb.expand( points[conVertices[j]] )
            
            center = bb.center()
            centerVector = points[ vtxList[i] ] - center
            normal       = normals[ vtxList[i] ]
            normal.normalize()
            projVector = normal * ( normal * OpenMaya.MFloatVector(centerVector) )
            
            resultPoint = -OpenMaya.MVector(projVector)/3.0 + OpenMaya.MVector( points[ vtxList[i] ] )
            resultPoints.append( resultPoint )
        
        meshName = fnMesh.partialPathName()
        for i in range( vtxList.length() ):
            cmds.move( resultPoints[i].x, resultPoints[i].y, resultPoints[i].z, meshName + ".vtx[%d]" % vtxList[i], os=1 )




def createOutMesh( meshObject, *args ):
    
    nonIoMeshs = sg.get.nonIoMesh( meshObject )
    if not nonIoMeshs: 
        cmds.error( "No meshs are selected" )
        return None
    
    srcMesh = nonIoMeshs[0]
    srcMeshTransform = cmds.listRelatives( srcMesh, p=1, f=1 )[0]
    
    newMesh = cmds.createNode( "mesh" )
    newMeshTransform = cmds.listRelatives( newMesh, p=1, f=1 )[0]
    
    cmds.connectAttr( srcMesh + ".outMesh", newMesh + ".inMesh" )
    cmds.xform( newMeshTransform, ws=1, matrix= cmds.getAttr( srcMeshTransform + ".wm" ) )

    newMeshTransform = cmds.rename( newMeshTransform, 'out_'+srcMeshTransform.split( '|' )[-1] )
    return newMeshTransform


def deleteHistory( target, evt=0 ):

    meshs = sg.get.nonIoMesh( target )
    
    for mesh in meshs:
        srcPlug = cmds.listConnections( mesh + '.inMesh', s=1, d=0, p=1 )
        cmds.disconnectAttr( srcPlug[0], mesh + '.inMesh' )
        srcNode = srcPlug[0].split( '.' )[0]
        cmds.delete( srcNode )