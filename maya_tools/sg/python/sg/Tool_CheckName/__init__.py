

class WinMain_Global:
    
    uiName = 'checkName_ui'
    title  = 'Check Name UI'
    width   = 300
    height  = 200
    
    textScroll = ''
    
    pattern  = ''
    
    jobIds = []
    




class WinMain_textScroll:
    
    def __init__(self):
        
        pass
    
    def create(self):
        
        import maya.cmds as cmds
        
        frame = cmds.frameLayout( l='Incorrect name list' )
        form  = cmds.formLayout()
        scroll = cmds.textScrollList( ams=1, sc=WinMain_Cmd.selectItem )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( scroll, 'top', 0 ), ( scroll, 'left', 0 ), ( scroll, 'right', 0 ), ( scroll, 'bottom', 0 )])
        
        WinMain_Global.textScroll = scroll
        
        return frame



class WinMain_JobCmd:
    
    
    @staticmethod
    def createSceneJob():
        
        import checkName_staticData
        import maya.OpenMaya as om

        if checkName_staticData.callbackIds.length():
            try:om.MMessage_removeCallbacks( checkName_staticData.callbackIds )
            except:pass
            checkName_staticData.callbackIds.clear()
            
        dagMessage   = om.MDagMessage()
        dgMessage    = om.MDGMessage()
        
        cbId01 = dgMessage.addNodeAddedCallback( WinMain_Cmd.checkName )
        cbId02 = dagMessage.addAllDagChangesCallback( WinMain_Cmd.checkName )
        checkName_staticData.callbackIds.append( cbId01 )
        checkName_staticData.callbackIds.append( cbId02 )
    

    @staticmethod
    def createScriptJob( *args ):
        
        import maya.cmds as cmds
        
        id01 = cmds.scriptJob( e=['SelectionChanged', WinMain_Cmd.checkName],
                                               p=WinMain_Global.uiName )
        id02 = cmds.scriptJob( e=['NameChanged', WinMain_Cmd.checkName],
                                               p=WinMain_Global.uiName )
        
        WinMain_Global.jobIds     = [ id01, id02 ]
        


    @staticmethod
    def deleteScriptJob( *args ):
        
        import maya.cmds as cmds
        for jobId in WinMain_Global.jobIds:
            cmds.scriptJob( k= jobId )




class WinMain_Cmd:
    
    
    @staticmethod
    def getPattern():
        
        import checkName_core
        import sys, os
        
        jsonPath = None
        for path in sys.path:
            for root, dirs, names in os.walk( path ):
                for name in names:
                    if name == 'checkName_ruls.json':
                        jsonPath = root + '\\' + name
                        break
                break
            if jsonPath: break
        
        WinMain_Global.pattern = checkName_core.getPatternFromJsonFile( jsonPath )
    
    
    @staticmethod
    def checkName( *args ):
        
        import checkName_core
        import maya.cmds as cmds
        
        targets = checkName_core.getIncorrectNamesFromPattern( WinMain_Global.pattern )
        cmds.textScrollList( WinMain_Global.textScroll, e=1, ra=1, a=targets )
        sels = cmds.ls( sl=1 )
        selectedTargets = []
        for sel in sels:
            if not sel in targets: continue
            selectedTargets.append( sel )
        cmds.textScrollList( WinMain_Global.textScroll, e=1, si=selectedTargets )
    
    
    @staticmethod
    def selectItem( evt=0 ):
        
        import maya.cmds as cmds
        selTargets = cmds.textScrollList( WinMain_Global.textScroll, q=1, si=1 )
        WinMain_JobCmd.deleteScriptJob()
        cmds.select( selTargets )
        WinMain_JobCmd.createScriptJob()
        




class WinMain:
    
    def __init__(self):
        
        WinMain_Cmd.getPattern()
        self.scrollList = WinMain_textScroll()
    
    
    def create(self):
        
        import maya.cmds as cmds
        
        if cmds.window( WinMain_Global.uiName, ex=1 ):
            cmds.deleteUI( WinMain_Global.uiName, wnd=1 )
        cmds.window( WinMain_Global.uiName, title=WinMain_Global.title )
        
        form = cmds.formLayout()
        textScrollForm = self.scrollList.create()
        buttonForm     = cmds.button( l='Refresh', c=WinMain_Cmd.checkName )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( textScrollForm, 'top', 5 ), ( textScrollForm, 'left', 5 ), ( textScrollForm, 'right', 5 ),
                               ( buttonForm, 'bottom', 5 ), ( buttonForm, 'left', 5 ), ( buttonForm, 'right', 5 )],
                         ac = [( textScrollForm, 'bottom', 5, buttonForm )] )
        
        cmds.window( WinMain_Global.uiName, e=1,
                     width  = WinMain_Global.width,
                     height = WinMain_Global.height )
        cmds.showWindow( WinMain_Global.uiName )
        
        WinMain_JobCmd.createSceneJob()
        WinMain_JobCmd.createScriptJob()
        WinMain_Cmd.checkName()