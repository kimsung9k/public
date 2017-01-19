
        
def addJointsToTreeView( rootJoint, ui_treeView ):
    
    import maya.cmds as cmds
    
    joints = [ cmds.ls( rootJoint )[0] ]
    jointPs = [ "", ]
    
    jointsChildren = cmds.listRelatives( rootJoint, c=1, f=1, ad=1, type='transform' )
    if not jointsChildren: jointsChildren = []
    jointsChildren.reverse()
    
    for joint in jointsChildren:
        joints.append( cmds.ls( joint )[0] )
        jointPs.append( cmds.ls( cmds.listRelatives( joints[-1], p=1, f=1 ) )[0] )
    
    for i in range( len( joints ) ):
        cmds.treeView( ui_treeView, e=1, addItem = ( joints[i], jointPs[i] ) )



def getSkinJointsFromRoot( rootJoint ):
    
    import maya.cmds as cmds
    jointsChildren = cmds.listRelatives( rootJoint, c=1, f=1, ad=1, type='transform' )
    jointsChildren.append( rootJoint )
    
    skinJoints = []
    for joint in jointsChildren:
        skinClusterNodes = cmds.listConnections( joint+'.wm', s=0, d=1, type='skinCluster' )
        if not skinClusterNodes: continue
        skinJoints.append( cmds.ls( joint )[0] )
    
    return skinJoints


def getSkinedMeshsFromRoot( rootJoint ):
    
    import maya.cmds as cmds
    jointsChildren = cmds.listRelatives( rootJoint, c=1, f=1, ad=1, type='transform' )
    jointsChildren.append( rootJoint )
    
    skinJoints = []
    skinClusters = []
    for joint in jointsChildren:
        skinClusterNodes = cmds.listConnections( joint+'.wm', s=0, d=1, type='skinCluster' )
        if not skinClusterNodes: continue
        skinClusters += skinClusterNodes
        skinJoints.append( cmds.ls( joint )[0] )
    
    skinClusters = list( set( skinClusters ) )
    
    targetMeshs = []
    for mesh in cmds.ls( type='mesh' ):
        meshHists = cmds.listHistory( mesh, pdo=1 )
        if not meshHists: continue
        for hist in meshHists:
            if not cmds.nodeType( hist )=='skinCluster': continue
            if hist in skinClusters: 
                targetMeshs.append( mesh )
                break
    
    return targetMeshs



def createSnapshotCam():
    
    import maya.cmds as cmds
    
    panel = cmds.getPanel( wf=1 )
    try:cam = cmds.modelEditor( panel, q=1, camera=1 )
    except:cam = 'persp'
    duCam = cmds.duplicate( cam )[0]
    duCamShape = cmds.listRelatives( duCam, s=1, f=1 )[0]
    
    cmds.setAttr( duCamShape+".displayFilmGate", 0)
    cmds.setAttr( duCamShape+".displayResolution", 0)
    cmds.setAttr( duCamShape+".displayGateMask", 0)
    cmds.setAttr( duCamShape+".displayFieldChart", 0)
    cmds.setAttr( duCamShape+".displaySafeAction", 0)
    cmds.setAttr( duCamShape+".displaySafeTitle", 0)
    cmds.setAttr( duCamShape+".displayFilmPivot", 0)
    cmds.setAttr( duCamShape+".displayFilmOrigin", 0)
    cmds.setAttr( duCamShape+".overscan", 1)
    cmds.setAttr( duCamShape+".focalLength", 120 )
    
    return duCam