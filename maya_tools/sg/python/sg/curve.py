import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.format
import sg.dag



def getCurveLength( curve ):
    
    dagCurve = sg.dag.getDagPath( curve )
    fnCurve = OpenMaya.MFnNurbsCurve( dagCurve )
    
    return fnCurve.length()




def getPointsFromCurve( curve, numPoints, powValue = 1 ):
    
    dagCurve = sg.dag.getDagPath( curve )
    fnCurve = OpenMaya.MFnNurbsCurve( dagCurve )
    
    curveLength = fnCurve.length()
    eachLength = curveLength / (numPoints-1)
    
    eachLengthNormalValue = eachLength / curveLength
    
    points = OpenMaya.MPointArray()
    points.setLength( numPoints )
    
    for i in range( numPoints ):
        editNormalValue = pow( eachLengthNormalValue * i , powValue )
        targetParam = fnCurve.findParamFromLength( editNormalValue * curveLength )
        
        point = OpenMaya.MPoint()
        fnCurve.getPointAtParam( targetParam, point, OpenMaya.MSpace.kWorld )
        points.set( point, i )
            
    return points



def createCurveByDagNodes( dagNodes, degree=3, ep=False ):
    
    posList = []
    for dagNode in dagNodes:
        pos = cmds.xform( dagNode, q=1, ws=1, t=1 )
        posList.append( pos )
    
    if ep:
        curve = cmds.curve( ep = posList, d=degree )
    else:
        curve = cmds.curve( p = posList, d=degree )
        curveShape = cmds.listRelatives( curve, s=1 )[0]
        
        for i in range( len( dagNodes ) ):
            dcmp = cmds.createNode( 'decomposeMatrix' )
            cmds.connectAttr( dagNodes[i] + '.wm', dcmp + '.imat' )
            cmds.connectAttr( dcmp + '.ot', curveShape + '.controlPoints[%d]' % i )
    
    cmds.setAttr( curve + '.inheritsTransform', 0 )

            
        
        

def createPointOnCurveByClosestPosition( dagNodes, curve, setOrient=False, aimVector=[1,0,0], upVector=[0,1,0], worldUp=[0,1,0] ):

    curveShape = cmds.listRelatives( curve, s=1, f=1 )[0]
    
    sgCurve = sg.format.Curve( curveShape )
    
    for i in range( len( dagNodes )):
        
        dagPoint = OpenMaya.MPoint( *cmds.xform( dagNodes[i], q=1, ws=1, t=1 ))
        param = sgCurve.getClosestParamAtPoint( dagPoint )
        
        curveInfo = cmds.createNode( 'pointOnCurveInfo' )
        cmds.connectAttr( curveShape + '.local', curveInfo + '.inputCurve')
        cmds.setAttr( curveInfo + '.parameter', param )
        trNode = cmds.createNode( 'transform' )
        cmds.setAttr( trNode + '.dh', 1 )
        cmds.connectAttr( curveInfo + '.position', trNode + '.t' )
        
