import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import sg.get
import sg.mod
import sg.file
import sg.connect
from functools import partial


def create( parent ):
    
    print "modeling menu create"
    sels = [ sel for sel in cmds.ls( sl=1 ) if sg.get.nonIoMesh(sel) ]
    if not sels: return None
    
    if len( sels ) == 1:
        cmds.menuItem( l="<< Symmetry", rp="W", p=parent, c = partial( sg.mod.makeSymmetryMesh, sels[0], OpenMaya.MVector(-1,0,0) ) )
        cmds.menuItem( l="<< Delete -X", rp="SW", p=parent, c = partial( sg.mod.deleteSymmetryOpposite, sels[0], OpenMaya.MVector(-1,0,0) ) )
        cmds.menuItem( l="Symmetry >>", rp="E", p=parent, c = partial( sg.mod.makeSymmetryMesh, sels[0], OpenMaya.MVector(1,0,0) ) )
        cmds.menuItem( l="Delete X >>", rp="SE", p=parent, c = partial( sg.mod.deleteSymmetryOpposite, sels[0], OpenMaya.MVector(-1,0,0) ) )
    elif len( sels ) >= 2:
        cmds.menuItem( l="OutMesh to InMesh", p=parent, c=partial( sg.connect.outMeshToInMesh, sels[0], sels[1] ) )
        
        cmds.menuItem( l="project meth to mesh", p=parent, sm=1 )
        cmds.menuItem( l="project by cam", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( 0,0,0) ) )
        cmds.menuItem( d=1 )
        cmds.menuItem( l="project  X", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( -1,0,0) )  )
        cmds.menuItem( l="project  Y", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( 0,-1,0) )  )
        cmds.menuItem( l="project  Z", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( 0,0,-1) )  )
        cmds.menuItem( d=1 )
        cmds.menuItem( l="project -X", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( 1,0,0) )  )
        cmds.menuItem( l="project -Y", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( 0,1,0) )  )
        cmds.menuItem( l="project -Z", c= partial( sg.mod.projectMeshToMesh, sels[:-1], sels[-1], OpenMaya.MVector( 0,0,1) )  )
            
    cmds.menuItem( l="Export parts",    p=parent, c=partial( lambda x, y : sg.file.exportParts(x, options="v=0", typ="FBX export", pr=1, es=1), sels ) )
    cmds.menuItem( l="Create Out Mesh", p=parent, c=partial( lambda x, y : map( sg.mod.createOutMesh, x ), sels ) )