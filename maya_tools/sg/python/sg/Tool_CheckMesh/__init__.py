import maya.cmds as cmds
import checkMesh_control


class WinMain_Global:
    
    uiName = 'checkMesh_ui'
    title = 'Check Mesh UI'
    width = 300
    height = 200



class WinMain_Cmd_fnc:
    
    @staticmethod
    def getMeshFromSelection():
        
        selNodes = cmds.ls( sl=1 )
        if not selNodes: return None
        
        for selNode in selNodes:
            if cmds.nodeType( selNode ) in ['transform', 'joint']:
                selShapes = cmds.listRelatives( selNode, s=1, f=1 )
                if not selShapes: continue
                for selShape in selShapes:
                    if cmds.getAttr( selShape + '.io' ): continue
                    break
                if cmds.nodeType( selShape ) == 'mesh':
                    return selShape
                else: continue
            elif cmds.nodeType( selNode ) == 'mesh':
                return selShape



class WinMain_Cmd:
    
    @staticmethod
    def cmdGetCrossedUVs( *args ):
        
        meshName = WinMain_Cmd_fnc.getMeshFromSelection()
        uvIds = checkMesh_control.getCrossedUVIds( meshName, select=True )
        print "Crossed UVs:", uvIds
        
    @staticmethod
    def cmdGetTwistedFaces( *args ):
        
        meshName = WinMain_Cmd_fnc.getMeshFromSelection()
        faceIds = checkMesh_control.getTwistedFaceIds( meshName, select=True )
        print "Twisted Faces :", faceIds
    
    @staticmethod
    def cmdGetWeldVerties( *args ):
        
        meshName = WinMain_Cmd_fnc.getMeshFromSelection()
        vertexIds = checkMesh_control.getWeldVertexIds(meshName, select=True)
        print "Weld Vertices :", vertexIds
    
    @staticmethod
    def cmdGetCloseVertices( *args ):
        
        meshName = WinMain_Cmd_fnc.getMeshFromSelection()
        vertexIds = checkMesh_control.getCloseVerticeIds(meshName, select=True, tol=0.001)
        print "Close Vertices :", vertexIds



class WinMain:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        if cmds.window( WinMain_Global.uiName, q=1, ex=1 ):
            cmds.deleteUI( WinMain_Global.uiName, wnd=1 )
        cmds.window( WinMain_Global.uiName, title=WinMain_Global.title )
        
        form = cmds.formLayout()
        b1 = cmds.button( l='Check Crossed UVs', c=WinMain_Cmd.cmdGetCrossedUVs )
        b2 = cmds.button( l='Check Twisted Faces', c=WinMain_Cmd.cmdGetTwistedFaces )
        b3 = cmds.button( l='Check Weld Vertices', c=WinMain_Cmd.cmdGetWeldVerties )
        b4 = cmds.button( l='Check Close Vertices', c=WinMain_Cmd.cmdGetCloseVertices )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ ( b1, 'left', 5 ), ( b1, 'right', 5 ), ( b1, 'top', 5 ),
                              ( b2, 'left', 5 ), ( b2, 'right', 5 ),
                              ( b3, 'left', 5 ), ( b3, 'right', 5 ),
                              ( b4, 'left', 5 ), ( b4, 'right', 5 ), ( b4, 'bottom', 5 ) ],
                         ap=[ ( b1, 'bottom', 2, 25 ), ( b2, 'top', 2, 25 ),
                              ( b2, 'bottom', 2, 50 ), ( b3, 'top', 2, 50 ),
                              ( b3, 'bottom', 2, 75 ), ( b4, 'top', 2, 75 ) ] )
        
        cmds.window( WinMain_Global.uiName, e=1,
                     width = WinMain_Global.width, height = WinMain_Global.height  )
        cmds.showWindow( WinMain_Global.uiName )