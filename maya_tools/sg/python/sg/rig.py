import maya.cmds as cmds
import sg.attribute
import sg.value
import sg.base
import sg.skinCluster
import sg.shader
import sg.convert
import sg.transform
import sg.util
import sg.rivet
import maya.OpenMaya as OpenMaya



def setTool_putObject( evt=0 ):
    if not cmds.pluginInfo( 'SGMPlug_putObject.py', q=1, l=1 ):
        print "load plug-in 'SGMPlug_putObject.py'"
        cmds.loadPlugin( "SGMPlug_putObject.py" )
    
    cmds.setToolTo( 'PutObjectContext1' )




def setTool_putFollicle( evt=0 ):
    if not cmds.pluginInfo( 'SGMPlug_putFollicle.py', q=1, l=1 ):
        print "load plug-in 'SGMPlug_putFollicle.py'"
        cmds.loadPlugin( "SGMPlug_putFollicle.py" )
    
    cmds.setToolTo( 'PutFollicleContext1' )

    




def setJointZAxisByMesh( joints, baseMesh, evt=0 ):
    
    nonIoMeshs = sg.get.nonIoMesh( baseMesh )
    if not nonIoMeshs: return None
    dagPath = sg.base.getDagPath( nonIoMeshs[0] )
    
    if dagPath.node().apiTypeStr() != "kMesh": return None
    
    fnMesh = OpenMaya.MFnMesh( dagPath )
    for joint in joints:
        jointPos = OpenMaya.MPoint( *cmds.xform( joint, q=1, ws=1, t=1 ) )
        
        normal = OpenMaya.MVector()
        fnMesh.getClosestNormal( jointPos, normal, OpenMaya.MSpace.kWorld )
        
        rotValue = cmds.angleBetween( v1=[0,0,1], v2=[normal.x, normal.y, normal.z], er=1 )
        cmds.rotate( rotValue[0], rotValue[1], rotValue[2], joint, ws=1 )
    cmds.select( joints )





    
def createFolliclesOnMesh( joints, baseMesh, evt=0 ):
    
    joints = sg.convert.singleToList( joints )
    nonIoMeshs = sg.get.nonIoMesh( baseMesh )
    print joints, baseMesh
    if not nonIoMeshs: return None
    dagPath = sg.base.getDagPath( nonIoMeshs[0] )
    
    if dagPath.node().apiTypeStr() != "kMesh": return None
    
    fnMesh = OpenMaya.MFnMesh( dagPath )
    for joint in joints:
        jointPos = OpenMaya.MPoint( *cmds.xform( joint, q=1, ws=1, t=1 ) )
        
        uvPtr = sg.base.getFloat2Ptr()
        fnMesh.getUVAtPoint( jointPos, uvPtr, OpenMaya.MSpace.kWorld )
        uvValues = sg.util.getListFromFloat2Ptr( uvPtr )
        
        follicle = cmds.createNode( 'follicle' )
        follicleTr = cmds.listRelatives( follicle, p=1, f=1 )[0]
        
        cmds.connectAttr( fnMesh.partialPathName() + '.outMesh', follicle+'.inputMesh' )
        cmds.connectAttr( fnMesh.partialPathName() + '.worldMatrix[0]', follicle+'.inputWorldMatrix' )
        cmds.connectAttr( follicle + '.outTranslate', follicleTr + '.t' )
        cmds.connectAttr( follicle + '.outRotate', follicleTr + '.r' )
        
        cmds.setAttr( follicle + '.parameterU', uvValues[0] )
        cmds.setAttr( follicle + '.parameterV', uvValues[1] )

        follicleTr = cmds.rename( follicleTr, joint + '_follicle' )
        sg.attribute.addAttr( follicleTr, ln="sourceObject", at='message' )
        cmds.connectAttr( joint + '.message', follicleTr + '.sourceObject' )



def connectJointPositionWithFollicle( joints, evt=0 ):
    
    joints = sg.convert.singleToList( joints )
    for joint in joints:
        trFollicles = cmds.listConnections( joint +'.message', type='transform' )
        if not trFollicles: continue
        follicles = cmds.listRelatives( trFollicles, s=1 )
        if not follicles: continue
        sg.connect.constraint_point( trFollicles[0], joint )
        


def setOrientZero( trNodes, evt=0 ):
    
    trNodes = sg.convert.singleToList( trNodes )
    
    for trNode in trNodes:
        cmds.setAttr( trNode + '.r', 0,0,0 )
        if cmds.nodeType( trNode ):
            cmds.setAttr( trNode + '.jo', 0,0,0 )








def setWeightByBlendShape( skinedShape, blendShape ):

    import math

    skinedShape = sg.dag.getShape( skinedShape )
    blendShape  = sg.dag.getShape( blendShape )
    
    skinedHists = cmds.listHistory( skinedShape, pdo=1 )
    
    skinNode = None
    for hist in skinedHists:
        if cmds.nodeType( hist ) == 'skinCluster':
            skinNode = hist
            break
    if not skinNode: return None
    
    dagPathSkined = sg.base.getDagPath( skinedShape )
    dagPathBlend  = sg.base.getDagPath( blendShape )
    
    fnMeshSkined = OpenMaya.MFnMesh( dagPathSkined )
    fnMeshBlend  = OpenMaya.MFnMesh( dagPathBlend )
    pointsSkined = OpenMaya.MPointArray()
    pointsBlend  = OpenMaya.MPointArray()
    fnMeshSkined.getPoints( pointsSkined )
    fnMeshBlend.getPoints( pointsBlend )
    
    if pointsSkined.length() != pointsBlend.length(): return None
    
    mesh = cmds.ls( sl=1 )[0]
    skinClusterNode = sg.skinCluster.getSkinCluster( mesh )
    skinNodeInfo = sg.skinCluster.Node( skinClusterNode )
    
    baseJointIndex = 0
    movedMatIndices = []
    movedMatValues  = []
    for i in range( len( skinNodeInfo.jointMatrices ) ):
        movedMatIndices.append( i )
        movedMatValues.append( skinNodeInfo.jointBindPres[i] * skinNodeInfo.jointMatrices[i] )
    
    targetMats = skinNodeInfo.jointMatrices
    for i in range( len(targetMats) ):
        targetMat = targetMats[i]
        for j in range( 4 ):
            print "%.3f %.3f %.3f %.3f" %(targetMat( j, 0 ), targetMat( j, 1 ), targetMat( j, 2 ), targetMat( j, 3 ))
        print
    
    print len(movedMatIndices)
    
    movedVtxIndices = []
    for i in range( pointsSkined.length() ):
        diffValue  = math.fabs( pointsSkined[i].x - pointsBlend[i].x )
        diffValue += math.fabs( pointsSkined[i].y - pointsBlend[i].y )
        diffValue += math.fabs( pointsSkined[i].z - pointsBlend[i].z )
        if diffValue > 0.001:
            movedVtxIndices.append( i )
            
    
    for i in range( len( movedVtxIndices ) ):
        pointSkined = pointsSkined[ movedVtxIndices[i] ]
        pointBlend  = pointsBlend[ movedVtxIndices[i] ]
        
        targetVector = pointBlend - pointSkined
        
        jointIndices = [baseJointIndex]
        weights = [1]
        
        for j in range( len( movedMatIndices )):
            multedPoint = pointSkined * movedMatValues[j]
            movedVector = multedPoint - pointSkined
            if targetVector * movedVector <= 0: continue
            
            projVector = targetVector * (( targetVector * movedVector )/(targetVector.length()**2))
            weightValue = projVector.length()/targetVector.length()
            
            if weightValue > 1: weightValue = 1
            if weightValue < 0: weightValue = 0
            multWeights = 1 - weightValue
            for k in range( len( weights ) ):
                weights[k] *= multWeights
            jointIndices.append( movedMatIndices[j] )
            weights.append( weightValue )
        
        reIndices = []
        reWeights = []
        for j in range( len(weights) ):
            if not weights[j]: continue
            reIndices.append( jointIndices[j] )
            reWeights.append( weights[j] )
        
        skinNodeInfo.weightInfos[movedVtxIndices[i]].setWeight( reIndices, reWeights )
        


















    




def connectLocalTransformConnects( moveTarget, moveTargetP, target ):
    
    dcmp = sg.connect.getLocalDcmp( moveTarget, moveTargetP )
    cmds.connectAttr( dcmp + '.ot', target + '.t' )
    cmds.connectAttr( dcmp + '.or', target + '.r' )



def connectSquash( aimTarget, scaleTarget, evt=0 ):
    
    mm = cmds.createNode( 'multMatrix' )
    dcmp = cmds.createNode( 'decomposeMatrix' )
    dist = cmds.createNode( 'distanceBetween' )
    divNode = cmds.createNode( 'multiplyDivide' )
    
    cmds.connectAttr( mm + '.o', dcmp + '.imat' )
    
    cmds.connectAttr( aimTarget + '.wm', mm+'.i[0]' )
    cmds.connectAttr( scaleTarget + '.pim', mm + '.i[1]' )
    
    cmds.connectAttr( dcmp + '.ot', dist + '.point2' )
    
    sg.attribute.addAttr( scaleTarget, ln='origDist', cb=1, dv=cmds.getAttr( dist + '.distance' ) )
    cmds.connectAttr( dist + '.distance', divNode + '.input1X')
    cmds.connectAttr( scaleTarget + '.origDist', divNode + '.input2X' )
    
    maxDotValue, maxDotIndex = sg.value.maxDotIndexAndValue( OpenMaya.MVector(*cmds.getAttr( dcmp + '.ot')[0] ), OpenMaya.MMatrix() )
    
    targetAttrs = ['sx', 'sy', 'sz']
    cmds.connectAttr( divNode + '.outputX', scaleTarget + '.' + targetAttrs[maxDotIndex], f=1 )
    cmds.setAttr( divNode +'.op',2 )
    
    otherIndices = [0,1,2]
    otherIndices.remove( maxDotIndex )
    
    divNode2 = cmds.createNode( 'multiplyDivide' )
    powNode = cmds.createNode( 'multiplyDivide' )
    cmds.setAttr( divNode2 + '.op', 2 )
    cmds.setAttr( powNode + '.op', 3 )
    cmds.setAttr( divNode2 + '.input1X', 1 )
    cmds.connectAttr( divNode + '.outputX', divNode2 + '.input2X' )
    cmds.connectAttr( divNode2  + '.outputX', powNode + '.input1X' )
    cmds.setAttr( powNode + '.input2X', 0.5 );
    
    for otherIndex in otherIndices:
        cmds.connectAttr( powNode+'.outputX', scaleTarget + '.' + targetAttrs[ otherIndex ] )


def resetDistance( scaleTargets, evt=0 ):
    
    scaleTargets = sg.convert.singleToList( scaleTargets )
    
    for scaleTarget in scaleTargets:
        if not cmds.attributeQuery( 'origDist', node = scaleTarget, ex=1 ): continue
        divNode = cmds.listConnections( scaleTarget + '.origDist' )
        if not divNode: continue
        distNode = cmds.listConnections( divNode, type='distanceBetween' )
        if not distNode: continue
        dist = cmds.getAttr( distNode[0] + '.distance' )
        cmds.setAttr( scaleTarget + '.origDist', dist ) 




    


#----------------facial rig----------------------------


def connectFixBlend( resultShape, beforeShape, fixAddShape ):
    
    blendShapeNode = cmds.blendShape( resultShape, beforeShape, fixAddShape )[0]

    cmds.setAttr( blendShapeNode + '.w[0]',  1 )
    cmds.setAttr( blendShapeNode + '.w[1]', -1 )
    
    return blendShapeNode



def fixPointsAsSource( source, target ):
    
    srcFnMesh = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( source ) ) )
    dstFnMesh = OpenMaya.MFnMesh( sg.base.getDagPath( sg.dag.getShape( target ) ) )
    
    if srcFnMesh.numVertices() != dstFnMesh.numVertices():
        cmds.error( "Topology is not same" )
    
    points = OpenMaya.MPointArray()
    srcFnMesh.getPoints( points )
    dstFnMesh.setPoints( points )



def connectBlendShape( controller, targetMesh, skinedMesh ):
    
    import math
    
    blendShapeNode = sg.get.nodeFromHistory(skinedMesh, "blendShape", pdo=1 )
    
    if not blendShapeNode:
        blendShapeNode = cmds.blendShape( targetMesh, skinedMesh, par=1 )
    else:
        cuNum = len( cmds.ls( blendShapeNode[-1] + '.w[*]' ) )
        cmds.blendShape( blendShapeNode[-1], e=1, t=( skinedMesh, cuNum, targetMesh, 1 ) )
    
    dstAttr = cmds.ls( blendShapeNode[-1] + '.w[*]' )[-1]
    srcAttr = ''
    
    animCurveNode = cmds.createNode( 'animCurveUU')
    
    tValue = cmds.getAttr( controller + '.t' )[0]
    keyValue = 0
    if math.fabs(tValue[0]) > 0.001: 
        srcAttr = controller + '.tx'
        keyValue = tValue[0]
    elif math.fabs(tValue[1]) > 0.001:
        srcAttr = controller + '.ty'
        keyValue = tValue[1]
    elif math.fabs(tValue[2]) > 0.001:
        srcAttr = controller + '.tz'
        keyValue = tValue[2]
    
    cmds.connectAttr( srcAttr, animCurveNode + '.input' )
    cmds.connectAttr( animCurveNode + '.output', dstAttr )
    
    cmds.setKeyframe( animCurveNode, f=0,  v=0 )
    cmds.setKeyframe( animCurveNode, f=keyValue, v=1 )
    
    cmds.keyTangent( animCurveNode, f=(0,0), itt='linear', ott = 'linear' )
    cmds.keyTangent( animCurveNode, f=(keyValue,keyValue), itt='clamped', ott = 'clamped' )
    
    



def connectFixRig( controller, targetMesh, skinedMesh ):

    import math

    duSkinShape = cmds.createNode('mesh' )
    duSkin = cmds.listRelatives( duSkinShape, p=1 )[0]
    
    duOrigShape = cmds.createNode( 'mesh' )
    duOrig = cmds.listRelatives( duOrigShape, p=1 )[0]
    
    cmds.connectAttr( sg.get.nonIoMesh( skinedMesh )[0] + '.outMesh', duSkinShape + '.inMesh' )
    cmds.connectAttr( sg.get.ioMesh( skinedMesh )[0] + '.outMesh', duOrigShape + '.inMesh' )
    cmds.refresh()
    cmds.disconnectAttr( sg.get.nonIoMesh( skinedMesh )[0] + '.outMesh', duSkinShape + '.inMesh' )
    cmds.disconnectAttr( sg.get.ioMesh( skinedMesh )[0] + '.outMesh', duOrigShape + '.inMesh' )
    
    duOrig = cmds.rename( duOrig, (targetMesh + '_fix').replace('__', '_' ) )
    duSkin = cmds.rename( duSkin, (targetMesh + '_skinShape').replace('__', '_' ) )
    
    connectFixBlend( targetMesh, duSkin, duOrig )
    
    blendShapeNode = sg.get.nodeFromHistory(skinedMesh, "blendShape", pdo=1 )
    
    sg.shader.copyShader( skinedMesh, duOrig )
    sg.shader.copyShader( skinedMesh, duSkin )
    
    if not blendShapeNode:
        blendShapeNode = cmds.blendShape( duOrig, skinedMesh, par=1 )
    else:
        cuNum = len( cmds.ls( blendShapeNode[-1] + '.w[*]' ) )
        cmds.blendShape( blendShapeNode[-1], e=1, t=( skinedMesh, cuNum, duOrig, 1 ) )
    
    dstAttr = cmds.ls( blendShapeNode[-1] + '.w[*]' )[-1]
    srcAttr = ''
    
    animCurveNode = cmds.createNode( 'animCurveUU')
    
    tValue = cmds.getAttr( controller + '.t' )[0]
    rValue = cmds.getAttr( controller + '.r' )[0]
    keyValue = 0
    if math.fabs(tValue[0]) > 0.001: 
        srcAttr = controller + '.tx'
        keyValue = tValue[0]
    elif math.fabs(tValue[1]) > 0.001:
        srcAttr = controller + '.ty'
        keyValue = tValue[1]
    elif math.fabs(tValue[2]) > 0.001:
        srcAttr = controller + '.tz'
        keyValue = tValue[2]
    elif math.fabs(rValue[0]) > 0.1:
        srcAttr = controller + '.rx'
        keyValue = rValue[0]
    elif math.fabs(rValue[1]) > 0.1:
        srcAttr = controller + '.ry'
        keyValue = rValue[1]
    elif math.fabs(rValue[2]) > 0.1:
        srcAttr = controller + '.rz'
        keyValue = rValue[2]
        
    
    cmds.connectAttr( srcAttr, animCurveNode + '.input' )
    cmds.connectAttr( animCurveNode + '.output', dstAttr )
    
    cmds.setKeyframe( animCurveNode, f=0,  v=0 )
    cmds.setKeyframe( animCurveNode, f=keyValue, v=1 )
    
    cmds.keyTangent( animCurveNode, f=(0,0), itt='linear', ott = 'linear' )
    cmds.keyTangent( animCurveNode, f=(keyValue,keyValue), itt='clamped', ott = 'clamped' )
    
    return duOrig, duSkin




def connectBlendShapeRig( controller, targetMesh, skinedMesh ):

    import math
    
    blendShapeNode = sg.get.nodeFromHistory(skinedMesh, "blendShape", pdo=1 )
    
    if not blendShapeNode:
        blendShapeNode = cmds.blendShape( targetMesh, skinedMesh, par=1 )
    else:
        cuNum = len( cmds.ls( blendShapeNode[-1] + '.w[*]' ) )
        cmds.blendShape( blendShapeNode[-1], e=1, t=( skinedMesh, cuNum, targetMesh, 1 ) )
    
    dstAttr = cmds.ls( blendShapeNode[-1] + '.w[*]' )[-1]
    srcAttr = ''
    
    animCurveNode = cmds.createNode( 'animCurveUU')
    
    tValue = cmds.getAttr( controller + '.t' )[0]
    rValue = cmds.getAttr( controller + '.r' )[0]
    keyValue = 0
    if math.fabs(tValue[0]) > 0.001: 
        srcAttr = controller + '.tx'
        keyValue = tValue[0]
    elif math.fabs(tValue[1]) > 0.001:
        srcAttr = controller + '.ty'
        keyValue = tValue[1]
    elif math.fabs(tValue[2]) > 0.001:
        srcAttr = controller + '.tz'
        keyValue = tValue[2]
    elif math.fabs(rValue[0]) > 0.1:
        srcAttr = controller + '.rx'
        keyValue = rValue[0]
    elif math.fabs(rValue[1]) > 0.1:
        srcAttr = controller + '.ry'
        keyValue = rValue[1]
    elif math.fabs(rValue[2]) > 0.1:
        srcAttr = controller + '.rz'
        keyValue = rValue[2]
        
    
    cmds.connectAttr( srcAttr, animCurveNode + '.input' )
    cmds.connectAttr( animCurveNode + '.output', dstAttr )
    
    cmds.setKeyframe( animCurveNode, f=0,  v=0 )
    cmds.setKeyframe( animCurveNode, f=keyValue, v=1 )
    
    cmds.keyTangent( animCurveNode, f=(0,0), itt='linear', ott = 'linear' )
    cmds.keyTangent( animCurveNode, f=(keyValue,keyValue), itt='clamped', ott = 'clamped' )
    
    return targetMesh





def getSymIndices( symMesh ):
    
    fnSymMesh = OpenMaya.MFnMesh( sg.base.getDagPath( symMesh ) )
    
    pointsSymMesh = OpenMaya.MPointArray()
    
    fnSymMesh.getPoints( pointsSymMesh )
    symIndices = [-1 for i in range( pointsSymMesh.length() ) ]
    
    intersector = OpenMaya.MMeshIntersector()
    intersector.create( fnSymMesh.object() )

    pointOnMesh = OpenMaya.MPointOnMesh()
    vtxIndices = OpenMaya.MIntArray()
    for i in range( pointsSymMesh.length() ):
        if symIndices[i] != -1: continue
        pointMirror = OpenMaya.MPoint( -pointsSymMesh[i].x, pointsSymMesh[i].y, pointsSymMesh[i].z )
        intersector.getClosestPoint( pointMirror, pointOnMesh )
        faceIndex = pointOnMesh.faceIndex()
        
        fnSymMesh.getPolygonVertices( faceIndex, vtxIndices )
        
        minIndex = -1
        minDist = 100000.0
        for j in range( vtxIndices.length() ):
            dist = pointsSymMesh[vtxIndices[j]].distanceTo( pointMirror )
            if dist < minDist:
                minDist = dist
                minIndex = vtxIndices[j]
        
        if minIndex == -1: symIndices[i] = i
        else:symIndices[i] = minIndex
    
    return symIndices


def makeMirrorMesh( target, symBase ):
    
    fnTarget  = OpenMaya.MFnMesh( sg.base.getDagPath( target ) )

    pointsTarget  = OpenMaya.MPointArray()
    
    fnTarget.getPoints( pointsTarget )
    symIndices = getSymIndices( symBase )
    
    newPoints = OpenMaya.MPointArray()
    newPoints.setLength( pointsTarget.length() )
    for i in range( newPoints.length() ):
        newPoints.set( OpenMaya.MPoint( -pointsTarget[i].x, pointsTarget[i].y, pointsTarget[i].z ), symIndices[i] )
    
    newMesh = cmds.duplicate( sg.get.nonIoMesh(symBase)[0] )
    newMesh = sg.get.nonIoMesh( newMesh )[0]
    
    fnNewMesh = OpenMaya.MFnMesh( sg.base.getDagPath( newMesh ) )
    fnNewMesh.setPoints( newPoints )



def makeSymetryMesh( target, symBase, side='L' ):
    
    fnTarget  = OpenMaya.MFnMesh( sg.base.getDagPath( target ) )

    pointsTarget  = OpenMaya.MPointArray()
    
    fnTarget.getPoints( pointsTarget )
    symIndices = getSymIndices( symBase )
    
    newPoints = OpenMaya.MPointArray()
    newPoints.setLength( pointsTarget.length() )

    for i in range( newPoints.length() ):
        simMode = False
        if side == 'L' and pointsTarget[i].x >= 0: simMode = True
        if side == 'R' and pointsTarget[i].x <= 0: simMode = True
        
        symIndex = symIndices[i]
        if simMode : newPoints.set( OpenMaya.MPoint( -pointsTarget[symIndex].x, pointsTarget[symIndex].y, pointsTarget[symIndex].z ), i )
        else: newPoints.set( pointsTarget[i], i )
    
    newMesh = cmds.duplicate( sg.get.nonIoMesh(symBase)[0] )
    newMesh = sg.get.nonIoMesh( newMesh )[0]
    
    fnNewMesh = OpenMaya.MFnMesh( sg.base.getDagPath( newMesh ) )
    fnNewMesh.setPoints( newPoints )
    


def reverseParent( target ):
    
    targets = sg.convert.singleToList( target )
    
    for target in targets:
        dcmp = cmds.createNode( 'decomposeMatrix' )
        targetP = cmds.listRelatives( target, p=1, f=1 )[0]
        cmds.connectAttr( target + '.inverseMatrix', dcmp + '.imat' )
        cmds.connectAttr( dcmp + '.ot', targetP + '.t' )
        cmds.connectAttr( dcmp + '.or', targetP + '.r' )



def makeController( driver, meshComponent, radius = 1 ):
    
    meshComponents = sg.convert.singleToList( meshComponent )
    
    cmds.select( meshComponents )
    position = sg.selection.getCenter( meshComponents )
    mesh = meshComponents[0].split( '.' )[0]
    
    follicles = sg.rivet.createFollicleOnMeshByPositions( position, mesh )
    if not follicles: return None
    
    follicle = follicles[0]
    sphereObj, sphereShape = cmds.sphere( o=1, ch=1, nsp=4, radius=radius )
    
    sphereObj, sphereObjP = sg.dag.makeParent( sphereObj )[0]
    sphereObjP, sphereObjPP = sg.dag.makeParent( sphereObjP )[0]
    
    sg.connect.constraint_point( follicle, sphereObjPP )
    sg.transform.setOrientAsTarget( sphereObjPP, driver)
    
    cmds.connectAttr( sphereObj + '.tx', driver + '.tx' )
    cmds.connectAttr( sphereObj + '.ty', driver + '.ty' )
    cmds.connectAttr( sphereObj + '.tz', driver + '.tz' )
    reverseParent( sphereObj )
    
    return sphereObj, sphereObjP, sphereObjPP
    


def makeControllerMirror( controllers ):
    
    controllers = sg.convert.singleToList( controllers )
    
    for controller in controllers:
        controllerP = cmds.listRelatives( controller, p=1, f=1 )[0]
        controllerPP = cmds.listRelatives( controllerP, p=1, f=1 )[0]
        
        cmds.setAttr( controllerPP + '.sx', -1 )
        
        driverAttr = cmds.listConnections( controller+'.tx', p=1 )[0]
        md = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( controller + '.tx', md + '.input1' )
        cmds.setAttr( md + '.input2', -1 )
        cmds.connectAttr( md + '.output', driverAttr, f=1 )




    


def makeDetailJointRig( follicle, joint ):
    
    ctlNode = cmds.createNode( 'transform' )
    ctlNodeP = cmds.createNode( 'transform' )
    ctlNodeP = cmds.parent( ctlNodeP, follicle )[0]
    ctlNode = cmds.parent( ctlNode, ctlNodeP )[0]
    
    cmds.setAttr( ctlNodeP + '.t', 0,0,0 )
    cmds.setAttr( ctlNode + '.dh', 1 )
    
    dcmpCtlP = cmds.createNode( 'decomposeMatrix' )
    cmpCtlP  = cmds.createNode( 'composeMatrix' )
    invCtlP = cmds.createNode( 'inverseMatrix' )
    
    mm = cmds.createNode( 'multMatrix' )
    
    dcmp = cmds.createNode( 'decomposeMatrix' )
    
    cmds.connectAttr( ctlNodeP + '.wm', dcmpCtlP + '.imat' )
    cmds.connectAttr( dcmpCtlP + '.ot', cmpCtlP + '.it' )
    cmds.connectAttr( cmpCtlP + '.outputMatrix', invCtlP + '.inputMatrix' )
    
    cmds.connectAttr( ctlNode + '.wm', mm + '.i[0]' )
    cmds.connectAttr( invCtlP + '.outputMatrix', mm + '.i[1]' )
    
    cmds.connectAttr( mm + '.o', dcmp + '.imat' )
    
    cmds.connectAttr( dcmp + '.ot', joint + '.t' ) 
    



def mirrorConnect( first, second, evt=0 ):
    
    cmds.connectAttr( first +'.tx', second + '.tx' )
    cmds.connectAttr( first +'.ty', second + '.ty' )
    cmds.connectAttr( first +'.tz', second + '.tz' )
    cmds.connectAttr( first +'.rx', second + '.rx' )
    cmds.connectAttr( first +'.ry', second + '.ry' )
    cmds.connectAttr( first +'.rz', second + '.rz' )
    
    sg.connect.addMultDoubleLinear( second + '.tx', -1 )
    sg.connect.addMultDoubleLinear( second + '.ry', -1 )
    sg.connect.addMultDoubleLinear( second + '.rz', -1 )




def makeBlendShapeTarget( origTargets, blendTargets ):
    
    origTargets  = sg.convert.singleToList( origTargets )
    blendTargets = sg.convert.singleToList( blendTargets )
    
    for i in range( len( blendTargets ) ):
        
        origTarget  = origTargets[i]
        blendTarget = blendTargets[i]
        
        blendChildren = cmds.listRelatives( blendTarget, c=1, ad=1, type='transform', f=1 )
        if not blendChildren: blendChildren = []
        blendChildren.append( blendTarget )
        
        blendMeshs = []
        for blendChild in blendChildren:
            shapes = sg.get.nonIoMesh( blendChild )
            if not shapes: continue
            blendMeshs.append( blendChild )
        
        duBlendTarget = cmds.duplicate( origTarget )[0]
        duChildren = cmds.listRelatives( duBlendTarget, c=1, ad=1, type='transform', f=1 )
        if not duChildren: duChildren = []
        duChildren.append( duBlendTarget )
        
        duMeshs = []
        for duChild in duChildren:
            shapes = sg.get.nonIoMesh( duChild )
            if not shapes: continue
            duMeshs.append( duChild )
        
        for j in range( len( blendMeshs ) ):
            blendNode = cmds.blendShape( blendMeshs[j], duMeshs[j] )[0]
            cmds.setAttr( blendNode + '.w[0]', 1 )

    
    

#------------------------------------------------------



def duplicateAnimCurveAsUA( animCurveUU ):
    
    fValues = cmds.keyframe( cmds.ls( sl=1 )[0], q=1, fc=1 )
    vValues = cmds.keyframe( cmds.ls( sl=1 )[0], q=1, vc=1 )
    
    animCurveUA = cmds.createNode( 'animCurveUA' )
    
    for i in range( len( fValues ) ):
        cmds.setKeyframe( animCurveUA, f=fValues[i], v=vValues[i] )
