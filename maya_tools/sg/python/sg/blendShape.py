import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.convert
import sg.base




def assignBlendShape( first, second ):
    
    bl = cmds.blendShape( first, second )
    cmds.setAttr( bl[0] + '.w[0]', 1 )




def removeBlendRightWeight( blendedTargets, blendArea = 1 ):
    
    blendedTargets = sg.convert.singleToList( blendedTargets )
    
    for blendedTarget in blendedTargets:
        
        targets = sg.get.shapeTransformFromGroup( blendedTarget )
        
        for target in targets:
            print target
            blendNode = sg.get.nodeFromHistory( target, 'blendShape', pdo=1)
            if not blendNode: continue
            blendNode = blendNode[0]
            
            fnBlendNode = OpenMaya.MFnDependencyNode( sg.base.getMObject( blendNode ) )
            plugWeights = fnBlendNode.findPlug( 'inputTarget' )[0].child(1)
            
            fnMesh = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( target ) ) )
            points = OpenMaya.MPointArray()
            fnMesh.getPoints( points )
            print "fnmesh name : ", fnMesh.partialPathName()
            
            for i in range( points.length() ):
                xValue = points[i].x
                weightValue = 0
                if xValue > blendArea: continue
                if xValue < -blendArea: weightValue = 0
                elif xValue > -blendArea and xValue < blendArea:
                    weightValue = (xValue + blendArea)/(2.0*blendArea)
                
                cmds.setAttr( plugWeights.name() + '[%d]' % i, weightValue )



def removeBlendLeftWeight( blendedTargets, blendArea = 1 ):
    
    blendedTargets = sg.convert.singleToList( blendedTargets )
    
    for blendedTarget in blendedTargets:
        
        targets = sg.get.shapeTransformFromGroup( blendedTarget )
        
        for target in targets:
            blendNode = sg.get.nodeFromHistory( target, 'blendShape', pdo=1)
            if not blendNode: continue
            blendNode = blendNode[0]
            
            fnBlendNode = OpenMaya.MFnDependencyNode( sg.base.getMObject( blendNode ) )
            plugWeights = fnBlendNode.findPlug( 'inputTarget' )[0].child(1)
            
            fnMesh = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( target ) ) )
            points = OpenMaya.MPointArray()
            fnMesh.getPoints( points )
            
            for i in range( points.length() ):
                xValue = points[i].x
                weightValue = 0
                if xValue < -blendArea: continue
                if xValue > blendArea: weightValue = 0
                elif xValue > -blendArea and xValue < blendArea:
                    weightValue = (-xValue + blendArea)/(2.0*blendArea)
                
                cmds.setAttr( plugWeights.name() + '[%d]' % i, weightValue )



def copyBlendShapeWeight( srcTarget, dstTarget ):
    
    blendSrc = sg.get.nodeFromHistory( srcTarget, 'blendShape', pdo=1)
    blendDst = sg.get.nodeFromHistory( dstTarget, 'blendShape', pdo=1 )
    if not blendSrc or not blendDst: 
        if not blendSrc:
            cmds.error( "%s has no blend shape" % srcTarget )
        elif not blendDst:
            cmds.error( "%s has no blend shape" % blendDst )
        return None
    blendSrc = blendSrc[0]
    blendDst = blendDst[0]
    
    fnBlendSrc = OpenMaya.MFnDependencyNode( sg.base.getMObject( blendSrc ) )
    plugWeightsSrc = fnBlendSrc.findPlug( 'inputTarget' )[0].child(1)
    fnBlendDst = OpenMaya.MFnDependencyNode( sg.base.getMObject( blendDst ) )
    plugWeightsDst = fnBlendDst.findPlug( 'inputTarget' )[0].child(1)
    
    fnMeshSrc = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( srcTarget ) ) )
    fnMeshDst = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( dstTarget ) ) )
    
    if fnMeshSrc.numVertices() != fnMeshDst.numVertices(): 
        cmds.error( "%s and %s has not same" % fnMeshSrc.partialPathName(), fnMeshDst.partialPathName() )
        return None
    
    for i in range( fnMeshSrc.numVertices() ):
        weightValue = cmds.getAttr( plugWeightsSrc.name() + '[%d]' % i )
        cmds.setAttr( plugWeightsDst.name() + '[%d]' % i, weightValue )



def reverseBlendShapeWeight( target ):
    
    blendNode = sg.get.nodeFromHistory( target, 'blendShape', pdo=1)
    if not blendNode: 
        cmds.error( "%s has no blend shape" % target )
        return None
    blendNode = blendNode[0]
    
    fnBlendNode = OpenMaya.MFnDependencyNode( sg.base.getMObject( blendNode ) )
    plugWeights = fnBlendNode.findPlug( 'inputTarget' )[0].child(1)
    
    fnMesh = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( target ) ) )
    
    for i in range( fnMesh.numVertices() ):
        weightValue = cmds.getAttr( plugWeights.name() + '[%d]' % i )
        cmds.setAttr( plugWeights.name() + '[%d]' % i, 1-weightValue )
