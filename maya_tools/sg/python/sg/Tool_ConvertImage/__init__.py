# -*- coding:utf-8 -*- 

import maya.cmds as cmds


class WinMain_Global:
    
    uiName = 'ConvertImage_ui'
    title  = 'Convert Image UI'
    width  = 600
    height = 200
    
    instScriptTable    = ''
    
    checkExtension     = ''
    checkResolusion    = ''
    optionExtension    = ''
    intFieldResolution = ''




class WinMain_downloadPart:
    
    def __init__( self ):
        
        pass


    def create( self ):
        
        self.form = cmds.formLayout()
        text = cmds.text( l='This Function need ImageMagick')
        button = cmds.button( l='Download ImageMagick', c=WinMain_downloadPart_Cmd.downloadImageMagick, w=150 )
        cmds.setParent( '..' )
        
        cmds.formLayout( self.form, e=1, 
                         af = [( text, 'left', 5 ), ( text, 'top', 5 ),
                               ( button, 'right', 5 ), ( text, 'top', 5 )],
                         ac = [( text, 'right', 1, button )] )
        
        return self.form
        
        





class WinMain_scriptTable:
    
    def __init__(self):
        
        self.allCheckIsOn = True
        
        self.column1Uis = []
        self.column2Uis = []
        self.column3Uis = []
        self.column4Uis = []
        self.column5Uis = []
    
    
    def create( self ):
        
        self.frame = cmds.frameLayout( l='List File Node Textures')
        self.form = cmds.formLayout()
        check      = cmds.checkBox( l='', w=20, v=1, cc= WinMain_scriptTable_Cmd.firstCheckEditFnc )
        buttonNode = cmds.button( l='Node Name', w=120 )
        buttonPath = cmds.button( l='Image Path' )
        buttonExt  = cmds.button( l='Ext',  w=50 )
        buttonSize = cmds.button( l='Size', w=80)
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        self.column1Uis.append( check )
        self.column2Uis.append( buttonNode )
        self.column3Uis.append( buttonPath )
        self.column4Uis.append( buttonExt  )
        self.column5Uis.append( buttonSize )
        
        return self.frame



class WinMain_options:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        self.form = cmds.formLayout()
        text1 = cmds.text( l='Extension  : ', al='right', w=70 )
        text2 = cmds.text( l='Resolution : ', al='right', w=70 )
        checkExtension  = cmds.checkBox( l='', v=1 )
        checkResolusion = cmds.checkBox( l='', v=1 )
        optionExtension = cmds.optionMenu( w=60 )
        cmds.menuItem( l='PNG' )
        cmds.menuItem( l='JPG' )
        intFieldResolusion = cmds.intField( v=512, min=128, max=4096, w=60 )
        cmds.setParent( '..' )
        
        cmds.formLayout( self.form, e=1,
                         af = [( checkExtension, 'left', 10 ), ( checkExtension, 'top', 5 ),
                               ( checkResolusion, 'left', 10 ), 
                               ( text1, 'top', 5 ),
                               ( optionExtension  , 'top', 5 )],
                         ac = [( checkResolusion, 'top', 10, checkExtension ), 
                               ( text1, 'left', 0, checkExtension ),
                               ( text2, 'left', 0, checkResolusion ),
                               ( text2        , 'top', 2, optionExtension ),
                               ( intFieldResolusion, 'top', 2, optionExtension ),
                               ( optionExtension  , 'left', 2, text1 ),
                               ( intFieldResolusion, 'left', 2, text2 )])
        
        WinMain_Global.checkExtension     = checkExtension
        WinMain_Global.checkResolusion    = checkResolusion
        WinMain_Global.optionExtension    = optionExtension
        WinMain_Global.intFieldResolution = intFieldResolusion
        
        return self.form



class WinMain_downloadPart_Cmd:
    
    @staticmethod
    def downloadImageMagick( *args ):
        import webbrowser
        webbrowser.open_new_tab( 'http://www.imagemagick.org/download/binaries/ImageMagick-6.9.2-6-Q16-x64-dll.exe' )




class WinMain_scriptTable_Cmd:
    
    @staticmethod
    def updateTable():
        
        instScriptTable = WinMain_Global.instScriptTable
        
        for i in range( len( instScriptTable.column1Uis ) ):
            if i == 0:
                cmds.formLayout( instScriptTable.form, e=1,
                                 af = [(instScriptTable.column1Uis[i], 'top', 10),(instScriptTable.column2Uis[i], 'top', 5),
                                       (instScriptTable.column3Uis[i], 'top', 5),(instScriptTable.column4Uis[i], 'top', 5)
                                       ,(instScriptTable.column5Uis[i], 'top', 5)])
                cmds.formLayout( instScriptTable.form, e=1,
                             af=[( instScriptTable.column1Uis[i], 'left',5 ), ( instScriptTable.column5Uis[i], 'right',5 ) ],
                             ac=[( instScriptTable.column2Uis[i], 'left', 1, instScriptTable.column1Uis[i] ),
                                 ( instScriptTable.column3Uis[i], 'left',1,  instScriptTable.column2Uis[i] ),
                                 ( instScriptTable.column3Uis[i], 'right',1, instScriptTable.column4Uis[i] ),
                                 ( instScriptTable.column4Uis[i], 'right',1, instScriptTable.column5Uis[i] ) ] )
            else:
                cmds.formLayout( instScriptTable.form, e=1,
                                 ac=[( instScriptTable.column1Uis[i], 'top', 6, instScriptTable.column2Uis[i-1] ),
                                     ( instScriptTable.column2Uis[i], 'top', 3, instScriptTable.column2Uis[i-1] ),
                                     ( instScriptTable.column3Uis[i], 'top', 3, instScriptTable.column3Uis[i-1] ),
                                     ( instScriptTable.column4Uis[i], 'top', 3, instScriptTable.column4Uis[i-1] ),
                                     ( instScriptTable.column5Uis[i], 'top', 3, instScriptTable.column5Uis[i-1] )] )
                cmds.formLayout( instScriptTable.form, e=1,
                             af=[( instScriptTable.column1Uis[i], 'left',5 ), ( instScriptTable.column5Uis[i], 'right',5 ) ],
                             ac=[( instScriptTable.column1Uis[i], 'right',1, instScriptTable.column2Uis[i-1] ),
                                 ( instScriptTable.column2Uis[i], 'left', 1, instScriptTable.column1Uis[i-1] ),
                                 ( instScriptTable.column2Uis[i], 'right',1, instScriptTable.column3Uis[i-1] ),
                                 ( instScriptTable.column3Uis[i], 'left' ,1, instScriptTable.column2Uis[i-1] ),
                                 ( instScriptTable.column3Uis[i], 'right',1, instScriptTable.column4Uis[i-1] ),
                                 ( instScriptTable.column4Uis[i], 'left' ,1, instScriptTable.column3Uis[i-1] ),
                                 ( instScriptTable.column4Uis[i], 'right' ,1, instScriptTable.column5Uis[i-1] ),
                                 ( instScriptTable.column5Uis[i], 'left' ,1, instScriptTable.column4Uis[i-1] )] )
    
    @staticmethod
    def appendScriptTable( nodeInfo ):
        
        instScriptTable = WinMain_Global.instScriptTable
        nodeName, filePath, ext, size = nodeInfo
        
        cmds.checkBox( instScriptTable.column1Uis[0], e=1, v=1 )
        checkBox      = cmds.checkBox( l='', v=1, p= instScriptTable.form, cc= WinMain_scriptTable_Cmd.checkEditFnc )
        fieldNodeName = cmds.textField( 'txf_' + nodeName, tx=nodeName, p= instScriptTable.form )
        fieldFilePath = cmds.textField( 'txf_' + nodeName + '_filePath', tx=filePath, p= instScriptTable.form )
        fieldExt      = cmds.textField( 'txf_' + nodeName + '_ext',      tx=ext, p= instScriptTable.form )
        fieldSize     = cmds.textField( 'txf_' + nodeName + '_size',     tx=size, p= instScriptTable.form )
        
        instScriptTable.column1Uis.append( checkBox )
        instScriptTable.column2Uis.append( fieldNodeName )
        instScriptTable.column3Uis.append( fieldFilePath )
        instScriptTable.column4Uis.append( fieldExt )
        instScriptTable.column5Uis.append( fieldSize )
    
    
    @staticmethod
    def clearTable():
        
        instScriptTable = WinMain_Global.instScriptTable
        
        for i in range( 1, len( instScriptTable.column1Uis ) ):
            cmds.deleteUI( instScriptTable.column1Uis[i] )
            cmds.deleteUI( instScriptTable.column2Uis[i] )
            cmds.deleteUI( instScriptTable.column3Uis[i] )
            cmds.deleteUI( instScriptTable.column4Uis[i] )
            cmds.deleteUI( instScriptTable.column5Uis[i] )
        
        instScriptTable.column1Uis = instScriptTable.column1Uis[:1]
        instScriptTable.column2Uis = instScriptTable.column2Uis[:1]
        instScriptTable.column3Uis = instScriptTable.column3Uis[:1]
        instScriptTable.column4Uis = instScriptTable.column4Uis[:1]
        instScriptTable.column5Uis = instScriptTable.column5Uis[:1]
    
    
    @staticmethod
    def checkEditFnc( *args ):
        
        instScriptTable = WinMain_Global.instScriptTable 
        
        allChecked = True
        for i in range( 1, len( instScriptTable.column1Uis ) ):
            value = cmds.checkBox( instScriptTable.column1Uis[i], q=1, v=1 )
            if value: continue
            allChecked = False
        if allChecked:
            cmds.checkBox( instScriptTable.column1Uis[0], e=1, v=1 )
        else:
            cmds.checkBox( instScriptTable.column1Uis[0], e=1, v=0 )
    
    @staticmethod
    def firstCheckEditFnc( *args ):
        
        instScriptTable = WinMain_Global.instScriptTable 
        
        value = cmds.checkBox( instScriptTable.column1Uis[0], q=1, v=1 )
        
        for i in range( 1, len( instScriptTable.column1Uis ) ):
            cmds.checkBox( instScriptTable.column1Uis[i], e=1, v=value )




class WinMain_Cmd:
    
    @staticmethod
    def updateTableBySceneInfo():
        import convertImage_control
        
        fileNodes = convertImage_control.InMaya.getFileNodesFromScene()
        WinMain_scriptTable_Cmd.clearTable()
        for fileNode in fileNodes:
            width, height = convertImage_control.InMaya.getImageSize(fileNode)
            imagePath     = convertImage_control.InMaya.getImagePath( fileNode )
            ext = imagePath.split( '.' )[-1]
            
            info = ( fileNode, imagePath, ext, '%dx%d' % (width, height) )
            WinMain_scriptTable_Cmd.appendScriptTable(info)

        WinMain_scriptTable_Cmd.updateTable()


    @staticmethod
    def updateTableBySelection( *args ):
        import convertImage_control
        
        fileNodes = convertImage_control.InMaya.getFileNodesFormSelection()
        if not fileNodes: return WinMain_Cmd.updateTableBySceneInfo()
        
        WinMain_scriptTable_Cmd.clearTable()
        for fileNode in fileNodes:
            width, height = convertImage_control.InMaya.getImageSize(fileNode)
            imagePath     = convertImage_control.InMaya.getImagePath( fileNode )
            ext = imagePath.split( '.' )[-1]
            
            info = ( fileNode, imagePath, ext, '%dx%d' % (width, height) )
            WinMain_scriptTable_Cmd.appendScriptTable(info)

        WinMain_scriptTable_Cmd.updateTable()


    @staticmethod
    def convertImages( *args ):
        import convertImage_control
        
        instScriptTable = WinMain_Global.instScriptTable
        
        optionSelection = cmds.optionMenu( WinMain_Global.optionExtension, q=1, sl=1 )
        itemList  = cmds.optionMenu( WinMain_Global.optionExtension, q=1, ill=1 )
        extension  = cmds.menuItem( itemList[ optionSelection-1 ], q=1, l=1 ).lower()
        resolution = cmds.intField( WinMain_Global.intFieldResolution, q=1, v=1 )
        
        for i in range( 1, len( instScriptTable.column1Uis ) ):
            checkBox = instScriptTable.column1Uis[i]
            if not cmds.checkBox( checkBox, q=1, v=1 ): continue
            fileNode = cmds.textField( instScriptTable.column2Uis[i], q=1, tx=1 )
            
            convertExtension  = cmds.checkBox( WinMain_Global.checkExtension, q=1, v=1 )
            convertResolution = cmds.checkBox( WinMain_Global.checkResolusion, q=1, v=1 )
            
            convertImage_control.convertImageAndAssign( fileNode, extension if convertExtension else None, resolution if convertResolution else None )
        
        WinMain_Cmd.updateTableBySelection()



class WinMain:
    
    def __init__(self):
        
        self.instDownloadPart = WinMain_downloadPart()
        self.instScriptTable  = WinMain_scriptTable()
        self.instOption       = WinMain_options()
        
        WinMain_Global.instScriptTable = self.instScriptTable
    
    
    def scriptJob(self):
        cmds.scriptJob( e=['SelectionChanged', WinMain_Cmd.updateTableBySelection ],
                        p = WinMain_Global.uiName )
        cmds.scriptJob( e=['Undo', WinMain_Cmd.updateTableBySelection ],
                        p = WinMain_Global.uiName )
        cmds.scriptJob( e=['Redo', WinMain_Cmd.updateTableBySelection ],
                        p = WinMain_Global.uiName )
    
    
    def create(self):
        
        if cmds.window( WinMain_Global.uiName, ex=1 ):
            cmds.deleteUI( WinMain_Global.uiName, wnd=1 )
        cmds.window( WinMain_Global.uiName, title= WinMain_Global.title )
        
        form = cmds.formLayout()
        downloadPartForm = self.instDownloadPart.create()
        scriptTableForm  = self.instScriptTable.create()
        optionsForm      = self.instOption.create()
        buttonForm       = cmds.button( l='CONVERT', c=WinMain_Cmd.convertImages )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( downloadPartForm, 'top', 5 ),
                             ( downloadPartForm, 'left', 5 ), ( downloadPartForm, 'right', 5 ),
                             ( scriptTableForm, 'left', 5 ), ( scriptTableForm, 'right', 5 ),
                             ( optionsForm, 'left', 5 ),  ( optionsForm, 'bottom', 10 ),
                             ( buttonForm , 'right', 10 ), ( buttonForm , 'bottom', 10 ) ],
                         ac=[ ( scriptTableForm, 'top', 5, downloadPartForm ),( scriptTableForm, 'bottom', 5, optionsForm ),
                              ( buttonForm     , 'top'   , 5, scriptTableForm ), ( buttonForm, 'left', 15, optionsForm )] )
        
        cmds.window( WinMain_Global.uiName, e=1,
                     width = WinMain_Global.width,
                     height = WinMain_Global.height )
        cmds.showWindow( WinMain_Global.uiName )
        
        self.scriptJob()
        WinMain_Cmd.updateTableBySelection()