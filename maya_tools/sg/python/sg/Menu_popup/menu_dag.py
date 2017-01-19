import maya.cmds as cmds
from functools import partial
import sg.get
import sg.rig
import sg.check
import sg.nodeEdit
import sg.MainFunctions.dag
import sg.MainFunctions.transform
import sg.MainFunctions.connect



def create( parent ):
    
    sels = cmds.ls( sl=1 )
    meshs      = [ sel for sel in cmds.ls( sl=1 ) if sg.get.nonIoMesh(sel) ]
    joints     = [ sel for sel in cmds.ls( sl=1 ) if sg.check.isJoint( sel ) ]
    transforms = [ sel for sel in cmds.ls( sl=1 ) if sg.check.isTransformNode( sel ) ]
    
    if not sels: return None
    
    cmds.menuItem( l="Put Object", rp='N', p=parent, sm=1 )
    cmds.menuItem( l="Put Joint", rp='N', c= sg.MainFunctions.dag.putJoint )
    cmds.menuItem( l="Put Locator", rp='NW', c= sg.MainFunctions.dag.putLocator )
    cmds.menuItem( l="Put NULL", rp='NE', c= sg.MainFunctions.dag.putNull )
    cmds.menuItem( l="Put child", rp='S', sm=1 )
    cmds.menuItem( l='Put Child Null', rp='SE', c= sg.MainFunctions.dag.putChild )
    cmds.menuItem( l='Put Child Joint', rp='S', c= sg.MainFunctions.dag.putChildJoint )
    cmds.menuItem( l='Put Child Locator', rp='SW', c= sg.MainFunctions.dag.putChildLocator )
    
    miConnection = cmds.menuItem( l="Connection", rp='NE', p=parent, sm=1 )
    cmds.menuItem( l="Look At", rp='N', c= sg.MainFunctions.connect.lookAt )
    
    cmds.menuItem( l='Squash', rp='S', p=miConnection, sm=1 )
    cmds.menuItem( l='Squash reset', rp='SE', c=partial( sg.rig.resetDistance, sels ) )
    if len( sels ) == 2 :
        cmds.menuItem( l='Squash', rp='SW', c=partial( sg.rig.connectSquash, sels[0],  sels[1] ) )
        cmds.menuItem( l='Get Source Connection', p=miConnection, rp='SE', c= sg.MainFunctions.getSourceConnection )
    elif len( sels ) == 3:
        cmds.menuItem( l='replace', rp='SW', p=miConnection, c= sg.MainFunctions.replaceConnection )
    
    cmds.menuItem( l='Constraint', rp='NE', p=miConnection, sm=1 )
    cmds.menuItem( l="Point",  rp='NE', c= sg.MainFunctions.connect.constraint_point )
    cmds.menuItem( l="Orient",  rp='E', c= sg.MainFunctions.connect.constraint_orient )
    cmds.menuItem( l="Parent", rp='SE', c= sg.MainFunctions.connect.constraint_parent )
    
    cmds.menuItem( l='Blend Matrix', rp='E', p=miConnection, sm=1 )
    if len( sels ) >= 3:
        cmds.menuItem( l='Blend Two Matrix', rp='NW', c= sg.MainFunctions.connect.blendTwoMatrixConnect )
    cmds.menuItem( l='Blend Matrix Connection', rp='W', c= sg.MainFunctions.connect.blendMatrixConnect )
    cmds.menuItem( l='Blend Matrix Connection - mo', rp='SW', c=sg.MainFunctions.connect.blendMatrixConnect_mo )
    
    cmds.menuItem( l='Node Editor', rp='NW', p=miConnection, sm=1 )      
    cmds.menuItem( l='Get Source Connection', rp='NW', c=partial( sg.connect.getSourceConnection, sels[:-1], sels[-1] ) )
    cmds.menuItem( l='Optimize Connection', rp='W', c=partial( sg.connect.opptimizeConnection, sels[0] ) )
    cmds.menuItem( l='Create Zero To One And Reverse Nodes', rp='SW', c= partial( sg.nodeEdit.createZroToOneAndReverseNodes_cb, sels[0] ) )
    
    cmds.menuItem( l='Dag', rp='W', p=parent, sm=1 )
    cmds.menuItem( l='Make Parent', rp='N', c = sg.MainFunctions.dag.makeParent )
    cmds.menuItem( l='Parent Selected Older', rp='W', c= sg.MainFunctions.dag.parentSelectedOlder )
    cmds.menuItem( l='Parent To Constrained Object', rp='NW', c=sg.MainFunctions.connect.parentToConstrainedObject )
    
    cmds.menuItem( l="Freeze", rp='SW', p=parent, sm=1 )
    cmds.menuItem( l="Freeze Orient", rp='W', c= sg.MainFunctions.transform.freezeJoint )
    cmds.menuItem( l="Set Joint Orient Zero", rp="NW", c= sg.MainFunctions.transform.setJointOrientZero )
    cmds.menuItem( l="Freeze by Parent", rp='SW', c= sg.MainFunctions.transform.freezeByParent )
    
    
    if joints or transforms:
        cmds.menuItem( l='Set Position', rp='NW', p=parent, sm=1 )
        cmds.menuItem( l="Set Orient Zero", rp="NW", c= partial( sg.rig.setOrientZero, sels ) )
        cmds.menuItem( l="Set Orient By child", rp='SW', c= sg.MainFunctions.transform.setOrientByChild )
        cmds.menuItem( l='Set Orient By Target', rp='W', c= sg.MainFunctions.transform.setOrientAsTarget )
        
        cmds.menuItem( l='Make Center', rp='NE', c= sg.MainFunctions.transform.makeCenter )
        cmds.menuItem( l='Make Mirror', rp='E', c= sg.MainFunctions.transform.makeMirror )
        
        if len( sels ) >= 2:
            cmds.menuItem( l='Go to Target', rp='N', c = sg.MainFunctions.transform.setTransformAsTarget )
        
        if meshs:
            cmds.menuItem( l='Set Joint Normal By Mesh', p=parent, c=partial( sg.rig.setJointZAxisByMesh, joints, meshs[0] ) )
            cmds.menuItem( l='Create Follicle On Mesh', p=parent,  c=partial( sg.rig.createFolliclesOnMesh, joints, meshs[0] ) )
        
    cmds.menuItem( l='Init setting', p=parent, rp='S', sm=1 )
    if len( sels ) >= 2:
        cmds.menuItem( l='Get Local Dcmp', rp='N', c = sg.MainFunctions.connect.getLocalDcmp )
        cmds.menuItem( l='Get Look At Connect Node', rp='NE', c= sg.MainFunctions.connect.getLookAtConnectNode )
        cmds.menuItem( l='Get Local Dcmp distance', rp='NW', c= sg.MainFunctions.connect.getLocalDcmpDistance )
    
    
    cmds.menuItem( l="Naming", rp="E", sm=1, p=parent )
    cmds.menuItem( l="Rename Parent", rp="SE", c= sg.MainFunctions.dag.renameParent )
    cmds.menuItem( l="Rename Other Side", rp="E", c= sg.MainFunctions.dag.renameOtherSide )
    
    cmds.menuItem( l='Curve', sm=1, p=parent )
    
    