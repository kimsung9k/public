import maya.cmds as cmds
import maya.OpenMaya as OpenMaya



def vector( v ):
    
    if type( v ) == type( [] ):
        print "%f %f %f" %( v[0], v[1], v[2] )
    elif v.__class__ in [OpenMaya.MPoint, OpenMaya.MVector]:
        print "%f %f %f" %( v.x, v.y, v.z )


def point( p ):
    
    if type( p ) == type( [] ):
        print "%f %f %f %f" %( p[0], p[1], p[2], p[3] )
    elif p.__class__ == OpenMaya.MPoint:
        print "%f %f %f %f" %( p.x, p.y, p.z, p.w )



def matrix( mtx ):
    
    if type( mtx ) == type( [] ):
        for i in range( 4 ):
            print "%f %f %f %f" % (mtx[ i*4+0 ], mtx[ i*4+1 ], mtx[ i*4+2 ], mtx[ i*4+3 ])
    elif mtx.__class__ == OpenMaya.MMatrix:
        for i in range( 4 ):
            print "%f %f %f %f" % (mtx( i,0 ), mtx( i,1 ), mtx( i,2 ), mtx( i,3 ))