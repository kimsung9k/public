import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.convert
import sg.format
import sg.curve
import sg.check
import sg.node
import sg.base


def createHairJointOnHairMesh_fromRingEdge( lingEdges ):

    edgeIndices = sg.convert.singleToList( lingEdges )

    for edgeIndex in edgeIndices:
        mesh, attr = edgeIndex.split( '.' )
        
        num = int( edgeIndex.split( '[' )[1].replace( ']', '' ) )
        
        sgMesh = sg.format.Mesh( mesh )
        soltedIndices = sgMesh.getSoltedRingEdges( num )
        
        for i in soltedIndices:
            edge = mesh + '.e[%d]' % i
            vtx1, vtx2 = cmds.ls( cmds.polyListComponentConversion( edge, tv=1 ), fl=1 )
            jnt = cmds.joint()
            
            pos1 = OpenMaya.MVector( *cmds.xform( vtx1, q=1, ws=1, t=1 ) )
            pos2 = OpenMaya.MVector( *cmds.xform( vtx2, q=1, ws=1, t=1 ) )
            avPos = (pos1 + pos2)/2
            pos = [ avPos.x, avPos.y, avPos.z ]
            
            cmds.move( pos[0], pos[1], pos[2], jnt, ws=1 )



def createHairJointOnHairMesh_fromLoopEdge( loopEdges ):
    
    edgeIndices = sg.convert.singleToList( loopEdges )
    
    for edgeIndex in edgeIndices:
        mesh, attr = edgeIndex.split( '.' )
        
        num = int( edgeIndex.split( '[' )[1].replace( ']', '' ) )
        
        sgMesh = sg.format.Mesh( mesh )
        soltedIndices = sgMesh.getSoltedLoopEdges( num )
        
        for i in range( 0, len(soltedIndices)-1 ):
            edge1 = mesh + '.e[%d]' % soltedIndices[i]
            edge2 = mesh + '.e[%d]' % soltedIndices[i+1]
            
            vtxIndices1 = cmds.ls( cmds.polyListComponentConversion( edge1, tv=1 ), fl=1 )
            vtxIndices2 = cmds.ls( cmds.polyListComponentConversion( edge2, tv=1 ), fl=1 )
            
            vtx1, vtx2 = vtxIndices1
            
            targetVtx = vtx1
            if vtx1 in vtxIndices2:
                targetVtx = vtx2
            
            jnt = cmds.joint()
            pos = OpenMaya.MPoint( *cmds.xform( targetVtx, q=1, ws=1, t=1 ) )
            cmds.move( pos.x, pos.y, pos.z, jnt, ws=1 )

        lastVtx1, lastVtx2 = cmds.ls( cmds.polyListComponentConversion( mesh + '.e[%d]' % soltedIndices[-1], tv=1 ), fl=1 )
        
        pos1 = OpenMaya.MPoint( *cmds.xform( lastVtx1, q=1, ws=1, t=1 ) )
        pos2 = OpenMaya.MPoint( *cmds.xform( lastVtx2, q=1, ws=1, t=1 ) )
        
        posList = []
        
        if lastVtx1 in vtxIndices1:
            posList = [pos1, pos2]
        else:
            posList = [pos2, pos1]
        
        for pos in posList:
            jnt = cmds.joint()
            cmds.move( pos.x, pos.y, pos.z, jnt, ws=1 )
        


def createJointOnCurve( curve, numPoints, powValue = 1 ):
    
    points = sg.curve.getPointsFromCurve( curve, numPoints, powValue )
    
    rootJoint = cmds.createNode( 'joint', n= curve + '_topJnt' )
    for i in range( 1, points.length()):
        beforePoint = points[i]
        point = points[i-1]
        
        dist = beforePoint.distanceTo( point )
        
        jnt = cmds.joint( n= curve + '_jnt%d' % i )
        cmds.setAttr( jnt + '.tx', dist )
    
    cmds.ikHandle( sj=rootJoint, ee=jnt, curve =curve, sol='ikSplineSolver', ccv=False, pcv=False )



def cutCurve( curves, mesh ):
    
    curves = sg.convert.singleToList( curves )
    
    mesh = sg.dag.getShape( mesh )
    fnMesh = OpenMaya.MFnMesh( sg.base.getDagPath( mesh ) )
    meshIntersector = OpenMaya.MMeshIntersector()
    meshIntersector.create( fnMesh.object() )
    meshMtx  = fnMesh.dagPath().inclusiveMatrix()
    
    cutCrvs = []
    
    for curve in curves:
        curveShape = sg.dag.getShape( curve )
        
        fnCurve = OpenMaya.MFnNurbsCurve( sg.base.getDagPath( curveShape ) )
        curveMtx = fnCurve.dagPath().inclusiveMatrix()
        
        multMtx = curveMtx * meshMtx.inverse()
        
        numSpans = fnCurve.numSpans()
        degree   = fnCurve.degree()
        
        minParam = fnCurve.findParamFromLength( 0.0 )
        maxParam = fnCurve.findParamFromLength( fnCurve.length() )
        
        eachParam = (maxParam-minParam) / ( numSpans*10-1 )
        
        pointOnMesh = OpenMaya.MPointOnMesh()
        
        pointInCurve = OpenMaya.MPoint();
        pointInMesh = OpenMaya.MPoint();
    
        closestParam = 0.0;
    
        for i in range( numSpans*10 ):
            targetParam = eachParam * i + minParam
            fnCurve.getPointAtParam( targetParam, pointInCurve )
            pointInCurve*= multMtx
            meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
            normal = pointOnMesh.getNormal()
            pointInMesh = OpenMaya.MVector( pointOnMesh.getPoint() )
            
            if OpenMaya.MVector( pointInCurve - pointInMesh ) * OpenMaya.MVector( normal ) > 0:
                closestParam = targetParam
                break
        
        currentParam = targetParam
        
        if closestParam != 0:
            
            pointInCurvePlus = OpenMaya.MPoint()
            pointInCurveMinus = OpenMaya.MPoint()
            pointOnMeshPlus = OpenMaya.MPointOnMesh()
            pointOnMeshMinus = OpenMaya.MPointOnMesh()
            
            for i in range( 10 ):
                currentParamPlus  = currentParam + eachParam
                currentParamMinus = currentParam - eachParam
                
                if currentParamMinus < minParam: currentParamMinus = minParam
                
                fnCurve.getPointAtParam( currentParamPlus, pointInCurvePlus )
                fnCurve.getPointAtParam( currentParamMinus, pointInCurveMinus )
                pointInCurvePlus *= multMtx
                pointInCurveMinus *= multMtx
                meshIntersector.getClosestPoint( pointInCurvePlus, pointOnMeshPlus )
                meshIntersector.getClosestPoint( pointInCurveMinus, pointOnMeshMinus )
                pointInMeshPlus = OpenMaya.MPoint( pointOnMeshPlus.getPoint() )
                pointInMeshMinus = OpenMaya.MPoint( pointOnMeshMinus.getPoint() )
                
                if pointInMeshPlus.distanceTo( pointInCurvePlus ) < pointInMeshMinus.distanceTo( pointInCurveMinus ):
                    currentParam = currentParamPlus
                else:
                    currentParam = currentParamMinus
                
                if currentParam < minParam:
                    currentParam = minParam
                if currentParam > maxParam:
                    currentParam  = maxParam
                
                eachParam *= 0.5
        
        detachNode = cmds.createNode( 'detachCurve' )
        cmds.setAttr( detachNode+'.parameter[0]', currentParam )
        
        cutCurve  = cmds.createNode( 'nurbsCurve' )
        cutCurveP = cmds.listRelatives( cutCurve, p=1, f=1 )[0]
        
        cmds.connectAttr( curveShape+'.local', detachNode+'.inputCurve' )
        cmds.connectAttr( detachNode+'.outputCurve[1]', cutCurve+'.create' )
        
        if currentParam < 0.0001:
            fnCurve.getPointAtParam( currentParam, pointInCurve )
            pointInCurve*= multMtx
            meshIntersector.getClosestPoint( pointInCurve, pointOnMesh )
            pointClose = OpenMaya.MPoint( pointOnMesh.getPoint() ) * multMtx.inverse()
            cmds.move( pointClose.x, pointClose.y, pointClose.z, cutCurveP+'.cv[0]', os=1 )
        else:
            cmds.rebuildCurve( cutCurveP, ch=1, rpo=1, rt=0, end=1, kr=2, kcp=0, kep=1, kt=0, s=numSpans, degree=degree, tol=0.01 )

        cmds.DeleteHistory( cutCurveP )
        cmds.xform( cutCurveP, ws=1, matrix = sg.convert.matrixToList( curveMtx ) )

        curveName = curve.split( '|' )[-1]
        cutCurveP = cmds.rename( cutCurveP, curveName+'_cuted' )
        
        cutCrvs.append( cutCurveP )

    return cutCrvs



def createGravitySetting( topJoints ):
    
    topJoints = sg.dag.getTopJointChildren( topJoints )
    
    for topJoint in topJoints:
        topJointParent = sg.dag.getParent( topJoint )
        if not topJointParent or not sg.check.isDefault( topJoint ) :
            topJoint, topJointParent = sg.dag.makeParent( topJoint )[0]
        
        headConstJoint = cmds.duplicate( topJointParent, n= topJointParent.split( '|' )[-1] + '_headConst' )[0]
        gravityJoint = cmds.duplicate( topJointParent, n= topJointParent.split( '|' )[-1] + '_gravity' )[0]
        
        headConstJoint = cmds.parent( headConstJoint, w=1 )[0]
        gravityJoint = cmds.parent( gravityJoint, w=1 )[0]
        
        currentJoints = cmds.listRelatives( topJointParent, c=1, ad=1, f=1 )
        gravityJoints = cmds.listRelatives( gravityJoint, c=1, ad=1, f=1 )
        headConstJoints = cmds.listRelatives( headConstJoint, c=1, ad=1, f=1 )
        
        headConstJoints.reverse()
        gravityJoints.reverse()
        currentJoints.reverse()
        
        sg.attribute.addAttr( topJointParent, ln='start', min=0, dv=0, k=1 )
        sg.attribute.addAttr( topJointParent, ln='range', min=0, dv=1, k=1 )
        sg.attribute.addAttr( topJointParent, ln='gravityWeight', min=0, max=1, dv=1, k=1 )
        addNode  = cmds.createNode( 'addDoubleLinear' )
        cmds.connectAttr( topJointParent + '.start', addNode + '.input1' )
        cmds.connectAttr( topJointParent + '.range', addNode + '.input2' )
        
        for i in range( len( currentJoints ) ):
            dcmp = sg.connect.getBlendTwoMatrixDcmpNode( headConstJoints[i], gravityJoints[i], currentJoints[i] )
            cmds.connectAttr( dcmp + '.or', currentJoints[i] + '.r' )
            sg.attribute.addAttr( currentJoints[i], ln='num', cb=1, dv= i+1 )
            rangeNode = cmds.createNode( 'setRange' )
            cmds.connectAttr( currentJoints[i] + '.num', rangeNode + '.valueX' )
            cmds.connectAttr( topJointParent + '.start', rangeNode + '.oldMinX' )
            cmds.connectAttr( addNode + '.output', rangeNode + '.oldMaxX' )
            cmds.setAttr( rangeNode + '.maxX', 1 )
            multNode = cmds.createNode( 'multDoubleLinear' )
            cmds.connectAttr( rangeNode + '.outValueX', multNode + '.input1' )
            cmds.connectAttr( topJointParent + '.gravityWeight', multNode + '.input2' )
            cmds.connectAttr( multNode + '.output', currentJoints[i] + '.blend' )
        
    

def createMeshFromJoint( topJoint, width=0.5, smoothBind=False ):    

    childrenJoints = cmds.listRelatives( topJoint, c=1, ad=1, f=1, type='joint' )
    childrenJoints.reverse()
    
    topJntChild = cmds.listRelatives( topJoint, c=1, f=1 )[0]
    xValue = cmds.getAttr( topJntChild + '.tx' )
    topJntMtx = sg.convert.listToMatrix( cmds.getAttr( topJoint + '.wm' ) )
    
    point0 = OpenMaya.MPoint( 0,0, -width ) * topJntMtx
    point1 = OpenMaya.MPoint( 0,0,  width ) * topJntMtx
    point2 = OpenMaya.MPoint( xValue,0,  width ) * topJntMtx
    point3 = OpenMaya.MPoint( xValue,0, -width ) * topJntMtx
    
    points = OpenMaya.MPointArray()
    points.append( point0 )
    points.append( point1 )
    points.append( point2 )
    points.append( point3 )
    
    vtxIndices = OpenMaya.MIntArray()
    vtxIndices.append( 0 )
    vtxIndices.append( 1 )
    vtxIndices.append( 2 )
    vtxIndices.append( 3 )
    
    vtxCounts = OpenMaya.MIntArray()
    vtxCounts.append( 4 )
    
    currentIndex = 4
    
    for jnt in childrenJoints[:-1]:
        
        childJnt = cmds.listRelatives( jnt, c=1, f=1 )[0]
        xValue = cmds.getAttr( childJnt + '.tx' )
            
        jntMatrix = sg.convert.listToMatrix( cmds.getAttr( jnt + '.wm' ) )

        point0 = points[currentIndex-2]
        point1 = points[currentIndex-1]
        point2 = OpenMaya.MPoint( xValue,0,  width ) * jntMatrix
        point3 = OpenMaya.MPoint( xValue,0, -width ) * jntMatrix
        points.append( point2 )
        points.append( point3 )
        
        vtxIndices.append( currentIndex - 1 )
        vtxIndices.append( currentIndex - 2 )
        vtxIndices.append( currentIndex )
        vtxIndices.append( currentIndex + 1 )
        
        vtxCounts.append( 4 )
        
        currentIndex += 2
    
    meshTr = cmds.createNode( 'transform' )
    oMesh = sg.base.getMObject( meshTr )
    OpenMaya.MFnMesh().create( points.length(), vtxCounts.length(), points, vtxCounts, vtxIndices, oMesh )

    sg.shader.setDefaultShader( meshTr )
    
    if smoothBind:
        childrenJoints.append( topJoint )
        childrenJoints.append( meshTr )
        cmds.skinCluster( childrenJoints, tsb=1 )
    
    return meshTr


def createMeshFromJoint_bySelection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    topJoints = sg.dag.getTopJointChildren( sels )
    
    for topJoint in topJoints:
        meshTr = createMeshFromJoint( topJoint, 0.5, 1 )




def createCurveFromJoint( topJoint ):
    
    fnNode = OpenMaya.MFnDagNode( sg.base.getDagPath( topJoint ) )
    topJoint = fnNode.partialPathName()
    children = cmds.listRelatives( topJoint, c=1, ad=1 )
    children.append( topJoint )
    children.reverse()
    
    posList = []
    for i in range( len( children ) ):
        pos = cmds.xform( children[i], q=1, t=1, ws=1 )
        posList.append( pos )
    
    return cmds.curve( p = posList, d=3, n=topJoint + '_to_curve' )
    
    

def createCurveFromJoint_bySelection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    topJoints = sg.dag.getTopJointChildren( sels )
    
    curves = []
    for topJoint in topJoints:
        curve = createCurveFromJoint( topJoint )
        curves.append( curve )
    
    cmds.select( curves )
    
    

def makeBlendCurve( topJointGroup, addName, root ):
    
    import sg.dag

    topJoints =  sg.dag.getTopJointChildren( topJointGroup )
    
    curves = []
    
    for topJoint in topJoints:
        childJoints = cmds.listRelatives( topJoint, c=1, ad=1, type='joint' )
        childJoints.append( topJoint )
        childJoints.reverse()
        
        points = []
        for childJoint in childJoints:
            pos = cmds.xform( childJoint, q=1, ws=1, t=1 )
            points.append( pos )
        
        num = int( topJoint.split( '|' )[-1].split( '_' )[1] )
        crv = cmds.curve( ep=points, n='hairCurve_%d_%s' % ( num, addName ) )
        curves.append( crv )
    
    
    grp = cmds.group( n='hairCurve_%s' % addName, em=1 )
    cmds.xform( grp, ws=1, matrix= cmds.getAttr( root + '.wm' ) )
    curves = cmds.parent( curves, grp )
    cmds.makeIdentity( curves, apply=True, t=1, r=1, s=1, n=0, pn=0 )
    for curve in curves:
        cmds.setAttr( curve + '.rotatePivot', 0,0,0 )
        cmds.setAttr( curve + '.scalePivot', 0,0,0 )
        
        

def createLookAtCache( headCtl, attrs, hairSystem ):
    
    import maya.mel as mel
    import sg.file
    
    sceneName = cmds.file( sn=1, q=1 )
    splits = sceneName.split( '/' )
    newFolder = '/'.join( splits[:-1] ) + '/' + splits[-1].split( '.' )[0]
    sg.file.makeFolder( newFolder ) 
    
    hairSystem = cmds.listRelatives( hairSystem, s=1 )[0]
    
    for attr in attrs:
        
        for delTargetAttr in attrs:
            cons = cmds.listConnections( headCtl + '.' + delTargetAttr, s=1, d=0 )
            if not cons:
                cmds.setAttr( headCtl + '.' + delTargetAttr, 0 ) 
                continue
            cmds.setAttr( headCtl + '.' + delTargetAttr, 0 )
            cmds.delete( cons )
        
        cmds.setKeyframe( headCtl + '.' + attr, t=min, value=0 )
        cmds.setKeyframe( headCtl + '.' + attr, t=max, value=1 )
        
        cmds.select( hairSystem )
        try:mel.eval('deleteCacheFile 3 { "keep", "", "nCloth" } ;')
        except:pass
        mel.eval( 'doCreateNclothCache 5 { "2", "1", "10", "OneFile", "1", "","0","hini_hair_%s","0", "add", "0", "1", "1","0","1","mcx" } ;' % attr )

#createLookAtCache( cmds.ls( sl=1 )[0], ['left','right','top','bottom','topLeft','topRight','bottomLeft','bottomRight'], 'Dynamic_HairSystem' )


def setLookAtCache( headCtl, attr, hairSystem ):
    
    pass




