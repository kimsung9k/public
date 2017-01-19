

class WinMain_Global:
    
    uiName = 'checkSkinWeight_winmain_ui'
    title  = 'Check Skin Weight'
    width   = 550
    height  = 400
    
    gridSize = 150
    gridInterval  = 3
    
    txf_rootJoint = ""
    trv_joints = ""
    tx_numOfJoints = ""
    txf_filePath = ""
    grid_thumbnail = ""
    
    indexDragFrom = 0
    orderedList = []
    
    txf_source = ''
    txf_target = ''
    
    mode = 'edit'





class WinMain_Cmd:
    
    
    @staticmethod
    def setPrepData( evt=0 ):
        
        import os, cPickle
        import maya.cmds as cmds

        mayaDocPath = os.path.expanduser('~/maya')
        if not os.path.exists( mayaDocPath ):
            os.mkdir( mayaDocPath )
        prepData = mayaDocPath + '/jcg_checkSkinWeight.prepData' 
        
        winWidth  = cmds.window( WinMain_Global.uiName, q=1, w=1 )
        winHeight = cmds.window( WinMain_Global.uiName, q=1, h=1 )
        rootJoint = cmds.textField( WinMain_Global.txf_rootJoint, q=1, tx=1 )
        filePath  = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        sourceNs  = cmds.textField( WinMain_Global.txf_source, q=1, tx=1 )
        targetNs  = cmds.textField( WinMain_Global.txf_target, q=1, tx=1 )
        gridSize  = WinMain_Global.gridSize
        
        f = open( prepData, 'w' )
        cPickle.dump( [winWidth, winHeight, rootJoint, filePath, gridSize, sourceNs, targetNs ], f )
        f.close()
    
    
    @staticmethod
    def updateStringJointInfo( evt=0 ):
        
        import maya.cmds as cmds
        import core
        
        strRootJoints = cmds.textField( WinMain_Global.txf_rootJoint, q=1, tx=1 )
        rootJoints = strRootJoints.split( ',' )
        
        targetSkinJoints = []
        for rootJoint in rootJoints:
            if not cmds.objExists( rootJoint ): continue
            skinJoints = core.getSkinJointsFromRoot( rootJoint )
            targetSkinJoints += skinJoints
        
        cmds.text( WinMain_Global.tx_numOfJoints, e=1, l='%d skin Joints Searched' % len( targetSkinJoints ))
        
        
    
    @staticmethod
    def getPrepData( evt=0 ):
        
        import os, cPickle
        import maya.cmds as cmds

        mayaDocPath = os.path.expanduser('~/maya' )
        if not os.path.exists( mayaDocPath ):
            os.mkdir( mayaDocPath )
        prepData = mayaDocPath + '/jcg_checkSkinWeight.prepData' 
        
        f = open( prepData, 'r' )
        data = cPickle.load( f )
        f.close()
        
        try:
            winWidth, winHeight, rootJoints, filePath, gridSize, srcNs, targetNs = data
        except: return None
        cmds.window( WinMain_Global.uiName, e=1, w=winWidth )
        cmds.window( WinMain_Global.uiName, e=1, h=winHeight )
        cmds.textField( WinMain_Global.txf_filePath, e=1, tx=filePath )
        
        rootJoints = rootJoints.split( '.' )
        jointExists = True
        for rootJoint in rootJoints:
            if not cmds.objExists( rootJoint ):
                jointExists = False
        if jointExists:
            cmds.textField( WinMain_Global.txf_rootJoint, e=1, tx=rootJoint )
        WinMain_Global.gridSize = gridSize
        cmds.textField( WinMain_Global.txf_source, e=1, tx=srcNs )
        cmds.textField( WinMain_Global.txf_target, e=1, tx=targetNs )
        
        WinMain_Cmd.updateStringJointInfo()
    
    
    @staticmethod
    def loadSelected( evt=0 ):
        import maya.cmds as cmds
        
        targets = cmds.ls( sl=1 )
        
        realTargets = []
        for target in targets:
            if not cmds.nodeType( target ) in ['joint', 'transform']: continue
            realTargets.append( target )
        
        strRootJointTargets = ','.join( realTargets )
        cmds.textField( WinMain_Global.txf_rootJoint, e=1, tx=strRootJointTargets )
        WinMain_Cmd.updateStringJointInfo()
    
    
    @staticmethod
    def deleteUI( evt=0 ):
        import maya.cmds as cmds
        WinMain_Cmd.setPrepData()
        cmds.deleteUI( WinMain_Global.uiName, wnd=1 )
    
    
    
    @staticmethod
    def setFolderPath( evt=0 ):
        import maya.cmds as cmds
        folderPath = cmds.fileDialog2( dialogStyle=2, fm=2, okCaption='Load' )
        if not folderPath: return None
        cmds.textField( WinMain_Global.txf_filePath, e=1, tx=folderPath[0] )
        WinMain_Cmd.updateThumbnail()
        

    @staticmethod
    def getOrderedList( orderedListFilePath ):
        import json, os
        if not os.path.exists( orderedListFilePath ): return []
        f = open( orderedListFilePath, 'r' )
        poseNames = json.load( f )
        f.close()
        return poseNames


    @staticmethod
    def updateThumbnail( evt=0 ):
        
        import maya.cmds as cmds
        import os, copy
        from functools import partial
        
        windowWidth = cmds.window( WinMain_Global.uiName, q=1, w=1 )
        thumbnailAreaWidth = windowWidth - 14
        
        numberOfColumns = thumbnailAreaWidth / WinMain_Global.gridSize
        cmds.gridLayout( WinMain_Global.grid_thumbnail, e=1, numberOfColumns=numberOfColumns,
                         cellWidth = WinMain_Global.gridSize, cellHeight = WinMain_Global.gridSize+17 )
        
        childArray = cmds.gridLayout( WinMain_Global.grid_thumbnail, q=1, childArray=1 )
        if childArray:
            for child in childArray: 
                cmds.deleteUI( child )
        
        folderPath = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )

        poseNames = WinMain_Cmd.getOrderedList( folderPath + '/orderedList.txt' )
        
        for i in range( len( poseNames ) ):
            poseName = poseNames[i]
            form = cmds.formLayout( p=WinMain_Global.grid_thumbnail )
            iconButton = cmds.iconTextButton( image1 = folderPath + '/' + poseName + '.iff',
                                              width=WinMain_Global.gridSize-WinMain_Global.gridInterval*2,
                                              height=WinMain_Global.gridSize-WinMain_Global.gridInterval*2,
                                              bgc=[0.8,0.8,0.8],
                                              c=partial( WinMain_Cmd.setPose, poseName ) )
            button = cmds.text( l=poseName, h=17 )
            buttonX = cmds.button( l='X', c= partial(WinMain_Cmd.deletePose,poseName), bgc=[.7,.4,.4], h=17, w=15)
            cmds.setParent( '..' )
            
            if WinMain_Global.mode == 'use':
                cmds.button( buttonX, e=1, vis=0 )
            
            cmds.formLayout( form, e=1, 
                             af=[ ( iconButton, 'top', WinMain_Global.gridInterval ),
                                  ( iconButton, 'left', WinMain_Global.gridInterval ),
                                  ( iconButton, 'right', WinMain_Global.gridInterval ),
                                  ( button, 'left', WinMain_Global.gridInterval ),
                                  ( button, 'bottom', WinMain_Global.gridInterval ),
                                  ( buttonX, 'right', WinMain_Global.gridInterval ),
                                  ( buttonX, 'bottom', WinMain_Global.gridInterval )],
                             ac=[ ( iconButton, 'bottom', 0, button ),
                                  ( button, 'right', 0, buttonX ) ])

    
    @staticmethod
    def plusGridSize( evt=0 ):
        
        if WinMain_Global.gridSize >= 300: return None
        WinMain_Global.gridSize += 25
        WinMain_Cmd.updateThumbnail()


    @staticmethod
    def minusGridSize( evt=0 ):
        
        if WinMain_Global.gridSize <= 75: return None
        WinMain_Global.gridSize -= 25
        WinMain_Cmd.updateThumbnail()
    

    @staticmethod
    def newPose( evt=0 ):
        
        import maya.cmds as cmds
        import os
        
        rootJoints = cmds.textField( WinMain_Global.txf_rootJoint, q=1, tx=1 )
        folderPath = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        
        if not rootJoints or not cmds.objExists( rootJoints ):
            cmds.warning( 'Check "Root Joints"' )
            return 0
        if not folderPath or not os.path.exists( folderPath ):
            cmds.warning( 'Check "Folder Path"' )
            return 0
        
        WinSnapshot( rootJoints ).create()
    
    
    @staticmethod
    def deletePose( poseName, evt=0 ):
        
        import maya.cmds as cmds
        import os, json
        
        folderPath = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        
        iffFilePath = folderPath + '/' + poseName + '.iff'
        jsonFilePath = folderPath + '/' + poseName + '.json'
        
        if cmds.confirmDialog( title='Confirm', message='Are you sure?', button=['Yes','No'] ) == "Yes":
            os.remove( iffFilePath )
            os.remove( jsonFilePath )
            
            f = open( folderPath + '/orderedList.txt', 'r' )
            poseNames = json.load( f )
            f.close()
            poseNames.remove( poseName )
            f = open( folderPath + '/orderedList.txt', 'w' )
            json.dump( poseNames, f, indent=4 )
            f.close()
            
            WinMain_Cmd.updateThumbnail()
    
    
    @staticmethod
    def setPose( poseName, evt=0 ):
        
        import core
        import maya.cmds as cmds
        import os, json
        
        rootJoints  = cmds.textField( WinMain_Global.txf_rootJoint, q=1, tx=1 )
        folderPath = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        
        sourceNs = cmds.textField( WinMain_Global.txf_source, q=1, tx=1 )
        targetNs = cmds.textField( WinMain_Global.txf_target, q=1, tx=1 )
        
        jsonFilePath = folderPath + '/' + poseName + '.json'
        f = open( jsonFilePath, 'r' )
        poseData = json.load( f )
        f.close()
        
        skinJoints = core.getSkinJointsFromRoot( rootJoints )
        for skinJoint in skinJoints:
            origSkinJoint = sourceNs + skinJoint[len(targetNs):]
            t, r, jo, s = poseData[ origSkinJoint ]
            cmds.setAttr( skinJoint + '.t', *t )
            cmds.setAttr( skinJoint + '.r', *r )
            cmds.setAttr( skinJoint + '.jo', *jo )
            cmds.setAttr( skinJoint + '.s', *s )


    @staticmethod
    def openFileBroswer( evt=0 ):
        
        import maya.cmds as cmds
        import os
        folderPath = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        os.startfile( folderPath )


    @staticmethod
    def drag( index, *args ):
        WinMain_Global.indexDragFrom = index
    
    
    @staticmethod
    def drop( index, *args ):
        import maya.cmds as cmds
        import json, os
        from functools import partial
        
        folderPath = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        orderedIndexFilePath = folderPath + '/orderedList.txt'
        
        f = open( orderedIndexFilePath, 'r' )
        poseNames = json.load( f )
        f.close()
        
        fromIndex = WinMain_Global.indexDragFrom
        toIndex    = index
        
        fromPose = poseNames.pop( fromIndex )
        poseNames.insert( toIndex, fromPose )
        
        f = open( orderedIndexFilePath, 'w' )
        json.dump( poseNames, f, indent=4 )
        f.close()
        



class WinMain_RegisterArea:
    
    def __init__(self ):
        
        pass
    
    
    def create(self):
        import maya.cmds as cmds
        
        form = cmds.formLayout()
        tx_rootJoint  = cmds.text( l='Root Joints :', align='right', h=22, w=90 )
        txf_rootJoint = cmds.textField( h=22, w=120, editable=False )
        tx_numOfJoints = cmds.text( l='0 skin Joints searched', h=22, w=110, al='left' )
        tx_filePath = cmds.text( l='Folder Path :', align='right', h=22, w=90 )
        txf_filePath = cmds.textField( h=22, editable=False )
        bt_newPose = cmds.button( l='New Pose', h=22, w=110, c= WinMain_Cmd.newPose )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( tx_rootJoint, 'top', 0 ), ( tx_rootJoint, 'left', 0 ),
                             ( txf_rootJoint, 'top', 0 ),
                             ( tx_numOfJoints, 'top', 0 ), ( tx_numOfJoints, 'right', 0 ),
                             ( tx_filePath, 'left', 0 ),
                             ( bt_newPose, 'right', 0 ) ],
                         ac=[( txf_rootJoint, 'left', 5, tx_rootJoint ),
                             ( txf_rootJoint, 'right', 5, tx_numOfJoints ),
                             ( tx_filePath, 'top', 5, tx_numOfJoints ),
                             ( txf_filePath, 'top', 5, tx_numOfJoints ),
                             ( txf_filePath, 'left', 5, tx_filePath ),
                             ( txf_filePath, 'right', 5, bt_newPose ),
                             ( bt_newPose, 'top', 5, tx_numOfJoints )] )
        
        WinMain_Global.txf_rootJoint  = txf_rootJoint
        WinMain_Global.tx_numOfJoints = tx_numOfJoints
        WinMain_Global.txf_filePath = txf_filePath
        
        if WinMain_Global.mode == 'use':
            cmds.button( bt_newPose, e=1, vis=0 )
        
        return form
    
    

class WinMain_namespaceArea:
    
    def __init__(self):
        
        pass
    

    def create(self):
        import maya.cmds as cmds
        
        frame = cmds.frameLayout( l='Namespace' )
        form = cmds.formLayout()
        tx_source = cmds.text( l='In File :', h=22 )
        txf_source = cmds.textField( h=22 )
        tx_target = cmds.text( l='Current :', h=22 )
        txf_target = cmds.textField( h=22 )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        cmds.formLayout( form, e=1,
                         af = [ ( tx_source, 'left' , 20 ),
                                ( txf_target, 'right', 0 ) ],
                         ap= [ ( txf_source, 'right', 5, 50 ),
                               ( tx_target, 'left', 5, 50 )],
                         ac= [ ( txf_source, 'left', 5, tx_source ),
                               ( txf_target, 'left', 5, tx_target )] )
        
        WinMain_Global.txf_source = txf_source
        WinMain_Global.txf_target = txf_target
        
        if WinMain_Global.mode != 'use':
            cmds.frameLayout( frame, e=1, vis=0 )
        
        return frame
        



class WinMain_ThumbnailArea:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        import maya.cmds as cmds
        
        form = cmds.scrollLayout( bgc=[0,0,0] )
        grid = cmds.gridLayout( cellWidth = WinMain_Global.gridSize, cellHeight = WinMain_Global.gridSize+22 )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        WinMain_Global.grid_thumbnail = grid
        
        return form



class WinMain_FootArea:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        import maya.cmds as cmds
        
        form = cmds.formLayout()
        bt_minus    = cmds.button( l='-', w=30,h=30, c = WinMain_Cmd.minusGridSize )
        bt_plus     = cmds.button( l='+', w=30,h=30, c = WinMain_Cmd.plusGridSize )
        bt_refresh  = cmds.button( l='Refresh', w=80, h=30, c = WinMain_Cmd.updateThumbnail )
        bt_close    = cmds.button( l='Close',h=30, c = WinMain_Cmd.deleteUI )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ (bt_minus, 'top', 0), (bt_minus, 'left', 0),
                              (bt_plus , 'top', 0),
                              (bt_refresh, 'top', 0),
                              (bt_close, 'top', 0), (bt_close, 'right', 0) ],
                         ac=[ (bt_plus, 'left', 3, bt_minus ),
                              (bt_refresh, 'left', 3, bt_plus ),
                              (bt_close, 'left', 3, bt_refresh ) ] )
        return form
        




class WinMain:
    
    def __init__(self):
        
        self.registerArea = WinMain_RegisterArea()
        self.namespaceArea = WinMain_namespaceArea()
        self.thumbnailArea = WinMain_ThumbnailArea()
        self.footArea = WinMain_FootArea()
    
    
    def create(self):
        import maya.cmds as cmds
        
        if cmds.window( WinMain_Global.uiName, ex=1 ):
            cmds.deleteUI( WinMain_Global.uiName, wnd=1 )
        editTitle = WinMain_Global.title
        if WinMain_Global.mode != 'use':
            editTitle += ' - BUILD MODE'
        cmds.window( WinMain_Global.uiName, title=editTitle, titleBarMenu=0 )
        
        form = cmds.formLayout()
        registerArea = self.registerArea.create()
        namespaceArea = self.namespaceArea.create()
        thumbnailArea = self.thumbnailArea.create()
        footArea = self.footArea.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ (registerArea, 'top', 5 ), (registerArea, 'left', 5 ), (registerArea, 'right', 5 ),
                              (namespaceArea, 'left', 5 ), (namespaceArea, 'right', 5 ),
                              (thumbnailArea, 'left', 5 ), (thumbnailArea, 'right', 5 ),
                              (footArea, 'bottom', 5 ), (footArea, 'left', 5 ), (footArea, 'right', 5 )],
                         ac=[ (thumbnailArea, 'top', 5, namespaceArea ),(thumbnailArea, 'bottom', 5, footArea ),
                              (namespaceArea, 'top', 5, registerArea )] )
        
        cmds.window( WinMain_Global.uiName, e=1,
                     width  = WinMain_Global.width,
                     height = WinMain_Global.height )
        cmds.showWindow( WinMain_Global.uiName )
        
        cmds.popupMenu( p=WinMain_Global.txf_rootJoint )
        cmds.menuItem( l='Load Selected', c= WinMain_Cmd.loadSelected )
        
        cmds.popupMenu( p=WinMain_Global.txf_filePath )
        cmds.menuItem( l='Set Folder Path', c= WinMain_Cmd.setFolderPath )
        cmds.menuItem( dividerLabel = ' ', d=1 )
        cmds.menuItem( l='Open File Browser', c= WinMain_Cmd.openFileBroswer )
        
        WinMain_Cmd.getPrepData()
        WinMain_Cmd.updateThumbnail()




class WinSnapshot_Global:
    
    uiName = 'checkSkinWeight_winsnapshot_ui'
    title  = 'Check Skin Weight - Snapshot'
    width  = 300
    height = 354
    
    snapshotCamName = 'cam_checkSkinWeight'
    
    txf_poseName = ''




class WinSnapshot_Cmd:
    
    @staticmethod
    def appendToOrderedList( folderPath, poseName ):
        import os, json
        orderedListFilePath = folderPath + '/orderedList.txt'
        if not os.path.exists( orderedListFilePath ):
            f = open( orderedListFilePath, 'w' )
            json.dump( [], f, indent=4 )
            f.close()
        f = open( orderedListFilePath, 'r' )
        orderedList = json.load(f)
        f.close()
        orderedList.append( poseName )
        f = open( orderedListFilePath, 'w' )
        json.dump( orderedList, f, indent=4 )
        f.close()
        return len( orderedList )
        
    
    @staticmethod
    def createPose( evt=0 ):
        import maya.cmds as cmds
        import os, shutil, json
        import core

        rootJoints = cmds.textField( WinMain_Global.txf_rootJoint, q=1, tx=1 )
        poseName = cmds.textField( WinSnapshot_Global.txf_poseName, q=1, tx=1 )
        
        renderImagePath = cmds.hwRender( cam=WinSnapshot_Global.snapshotCamName, width=300, height=300 )
        
        targetFolder = cmds.textField( WinMain_Global.txf_filePath, q=1, tx=1 )
        targetImagePath = targetFolder + '/' + poseName + '.iff'
        targetPosInfoPath = targetFolder + '/' + poseName + '.json'
        
        doMakeFile = False
        
        if os.path.exists( targetImagePath ):
            if cmds.confirmDialog( title='Confirm', message='"%s" is already exists\nDo you want replace it?' % poseName, button=['Yes','No'] ) == "Yes":
                doMakeFile = True
        else:
            doMakeFile = True
            WinSnapshot_Cmd.appendToOrderedList( targetFolder , poseName )
        
        if doMakeFile:
            skinJoints = core.getSkinJointsFromRoot(rootJoints)
            dictData = {}
            for skinJoint in skinJoints:
                values = []
                values.append( cmds.getAttr( skinJoint + '.t' )[0] )
                values.append( cmds.getAttr( skinJoint + '.r' )[0] )
                values.append( cmds.getAttr( skinJoint + '.jo' )[0] )
                values.append( cmds.getAttr( skinJoint + '.s' )[0] )
                dictData.update( { skinJoint : values } )
            f = open( targetPosInfoPath, 'w' )
            json.dump( dictData, f, indent=4 )
            f.close()
            
            shutil.copy2( renderImagePath, targetImagePath )
            cmds.deleteUI( WinSnapshot_Global.uiName, wnd=1 )
            
        
        core
        WinMain_Cmd.updateThumbnail()
        
        
        

class WinSnapshot_option:
    
    def __init__(self ):
        
        pass
    
    def create(self):
        import maya.cmds as cmds
        
        form = cmds.formLayout()
        tx_poseName = cmds.text( l='Pose Name', h=25 )
        txf_poseName = cmds.textField( h=25 )
        bt_create = cmds.button( l='Create Pose', h=25, c=WinSnapshot_Cmd.createPose )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( tx_poseName, 'top', 0 ), ( tx_poseName, 'left', 5 ),
                              ( txf_poseName, 'top', 0 ), ( txf_poseName, 'right', 0 ),
                              ( bt_create, 'left', 0 ), ( bt_create, 'right', 0 ), ( bt_create, 'bottom', 0 ) ],
                         ac=[ ( txf_poseName, 'left', 5, tx_poseName ),
                              ( bt_create, 'top', 0, tx_poseName ) ] )
        
        WinSnapshot_Global.txf_poseName = txf_poseName
        
        return form





class WinSnapshot:
    
    def __init__(self, targetObjects ):
        import maya.cmds as cmds
        import core
        
        if not cmds.objExists( WinSnapshot_Global.snapshotCamName ):
            cam = core.createSnapshotCam()
            cmds.rename( cam, WinSnapshot_Global.snapshotCamName )
            self.camJustCreated = True
        else:
            self.camJustCreated = False
        
        self.targetObjs = targetObjects
        self.optionArea = WinSnapshot_option()
    
    
    def create(self):
        
        import maya.cmds as cmds
        if cmds.window( WinSnapshot_Global.uiName, q=1, ex=1 ):
            cmds.deleteUI( WinSnapshot_Global.uiName, wnd=1 )
        cmds.window( WinSnapshot_Global.uiName, title=WinSnapshot_Global.title )
        
        form = cmds.formLayout()
        
        modelEditor = cmds.modelEditor( camera=WinSnapshot_Global.snapshotCamName, hud=0, 
                                              cameras=0, dynamics=0, ikHandles=0, nurbsCurves=0, displayTextures=True, grid=False,
                                              da='smoothShaded', td='modulate', rnm='hwRender_OpenGL_Renderer' )
        optionArea = self.optionArea.create()
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( modelEditor, 'left', 0 ), ( modelEditor, 'top', 0), ( modelEditor, 'right', 0 ),
                              ( optionArea, 'left', 0 ), ( optionArea, 'right', 0 ), ( optionArea, 'bottom', 0 ) ],
                         ac=[ ( modelEditor, 'bottom', 0, optionArea ) ] )
        
        cmds.window( WinSnapshot_Global.uiName, e=1,
                     width  = WinSnapshot_Global.width,
                     height = WinSnapshot_Global.height )
        cmds.showWindow( WinSnapshot_Global.uiName )
        
        selObjs = cmds.ls( sl=1 )
        cmds.select( self.targetObjs )
        if self.camJustCreated:
            cmds.viewFit( WinSnapshot_Global.snapshotCamName )
        cmds.select( selObjs )


def showEditMode():
    
    WinMain_Global.mode = 'edit'
    WinMain().create()



def showUseMode():
    
    WinMain_Global.mode = 'use'
    WinMain().create()