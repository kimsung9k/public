import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import convert
import sg.check



def getProjectionVector( vectorBase, vectorTarget ):
    
    v1 = vectorBase
    v2 = vectorTarget
    
    return v1 * ( v1 * v2 / pow( v1.length(), 2 ) )



def getOrigMatrix():
    
    return OpenMaya.MMatrix()



def getMirrorMatrix( mtx, vectorBase ):
    
    mtxList = convert.matrixToList( OpenMaya.MMatrix() )
    for i in range( 4 ):
        vElement = OpenMaya.MVector( mtx[i] )
        vProj = getProjectionVector( vectorBase, vElement )
        vResult = vElement - vProj * 2
        mtxList[ i*4 + 0 ] = vResult.x
        mtxList[ i*4 + 1 ] = vResult.y
        mtxList[ i*4 + 2 ] = vResult.z
    return convert.listToMatrix( mtxList )    
    


def activeCamMatrix():
    
    panel = cmds.getPanel( wf=1 )
    if not panel in cmds.getPanel( type='modelPanel' ):
        return None
    
    cam = cmds.modelPanel( panel, q=1, cam=1 )
    return convert.listToMatrix( cmds.getAttr( cam + ".wm") )



def worldToViewPoint( point, camMatrixInverse=None ):
    
    if not camMatrixInverse:
        camMatrixInverse = activeCamMatrix().inverse()
    
    activeView = OpenMayaUI.M3dView().active3dView()
    viewWidth = activeView.portWidth()
    viewHeight = activeView.portHeight()
    
    projMatrix = OpenMaya.MMatrix()
    activeView.projectionMatrix(projMatrix)
    projPoint = point * camMatrixInverse * projMatrix
    
    projPoint.x /= projPoint.w; projPoint.y /= projPoint.w; projPoint.z /= projPoint.w
    viewPointX = (projPoint.x + 1)/2.0 * viewWidth
    viewPointY = (projPoint.y + 1)/2.0 * viewHeight
    
    return OpenMaya.MPoint( viewPointX, viewPointY, projPoint.z )



def worldToViewPoints( points, camMatrixInverse=None ):
    
    if not camMatrixInverse:
        camMatrixInverse = activeCamMatrix().inverse()
    
    activeView = OpenMayaUI.M3dView().active3dView()
    viewWidth = activeView.portWidth()
    viewHeight = activeView.portHeight()
    
    projMatrix = OpenMaya.MMatrix()
    activeView.projectionMatrix(projMatrix)
    multMtx = camMatrixInverse * projMatrix
    
    resultPoints = OpenMaya.MPointArray()
    resultPoints.setLength( points.length() )
    for i in range( points.length() ):
        projPoint = points[i] * multMtx
        projPoint.x /= projPoint.w; projPoint.y /= projPoint.w; projPoint.z /= projPoint.w
        viewPointX = (projPoint.x + 1)/2.0 * viewWidth
        viewPointY = (projPoint.y + 1)/2.0 * viewHeight
        resultPoints.set( OpenMaya.MPoint( viewPointX, viewPointY, projPoint.z ), i )
    return resultPoints;



def getCamRayFromWorldPoint( worldPoint ):
    
    viewPoint = worldToViewPoint( worldPoint )
    activeView = OpenMayaUI.M3dView().active3dView()
    
    pointSrc = OpenMaya.MPoint()
    ray      = OpenMaya.MVector()
    activeView.viewToWorld( int(viewPoint.x), int(viewPoint.y), pointSrc, ray )
    
    return pointSrc, ray



def getCamRaysFromWorldPoints( worldPoints ):
    
    viewPoints = worldToViewPoints( worldPoints )
    activeView = OpenMayaUI.M3dView().active3dView()
    
    pointSrcs = OpenMaya.MPointArray()
    rays      = OpenMaya.MVectorArray()
    pointSrcs.setLength( worldPoints.length() )
    rays.setLength( worldPoints.length() )
    
    for i in range( viewPoints.length() ):
        activeView.viewToWorld( int( viewPoints[i].x ), int( viewPoints[i].y ), pointSrcs[i], rays[i] )
    
    return pointSrcs, rays


def setWorldMatrix( target, matrix ):
    if not sg.check.isTransformNode( target ): return None
    if type( matrix ) == type( OpenMaya.MMatrix() ):
        matrix = sg.convert.matrixToList( matrix )
    cmds.xform( target, matrix=matrix, ws=1 )



def setLocalMatrix( target, matrix ):
    if not sg.check.isTransformNode(target) : return None
    if type( matrix ) == type( OpenMaya.MMatrix() ):
        matrix = sg.convert.matrixToList( matrix )
    cmds.xform( target, matrix=matrix )
