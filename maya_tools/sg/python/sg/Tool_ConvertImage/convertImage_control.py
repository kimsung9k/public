

class InStandalone:
    
    @staticmethod
    def convertImage( filePath, replaceFilePath=None, convertExtension=None, width = 512, origWidth = None ):
    
        if not width: width= origWidth
        if width == origWidth and not convertExtension: return filePath
        
        import os, copy
        filePath = filePath.replace( '\\', '/' )
        
        splitFilePath = filePath.split( '/' )
        
        folderPath   = '/'.join( splitFilePath[:-1] )
        fileName = splitFilePath[-1]
        
        fileNameSplits = fileName.split( '.' )
        olnyFileName = '.'.join( fileNameSplits[:-1] )
        cuExtension  = fileNameSplits[-1]
        if width == origWidth and convertExtension==cuExtension: return filePath
        if not convertExtension: convertExtension = cuExtension
        
        if not replaceFilePath:
            replaceFilePath = folderPath + '/' + olnyFileName + '_convert.%s' % convertExtension
        batchFilePath   = folderPath + '/convertImage_%s.bat' % fileName
        height = copy.copy( width )
        
        batText = "convert %s -resize %dx%d %s" %( filePath, width, height, replaceFilePath )
        print "batText: ", batText
        
        f = open( batchFilePath, 'w' )
        f.write( batText )
        f.close()
        
        os.system( batchFilePath )
        os.remove( batchFilePath )
        
        return replaceFilePath




class InMaya:

    @classmethod
    def getMeshFromSelection( cls ):
        import maya.cmds as cmds
        selNodes = cmds.ls( sl=1 )
        if not selNodes: return None
        
        meshNodes = []
        for selNode in selNodes:
            if cmds.nodeType( selNode ) in ['transform', 'joint']:
                selShapes = cmds.listRelatives( selNode, s=1, f=1 )
                if not selShapes: continue
                for selShape in selShapes:
                    if cmds.getAttr( selShape + '.io' ): continue
                    break
                if cmds.nodeType( selShape ) == 'mesh':
                    meshNodes.append( selShape )
                else: continue
            elif cmds.nodeType( selNode ) == 'mesh':
                meshNodes.append( selShape )
        return meshNodes

    
    @staticmethod
    def getImageSize( fileNode ):
        import maya.cmds as cmds
        width  = cmds.getAttr( fileNode + '.outSizeX' )
        height = cmds.getAttr( fileNode + '.outSizeY' )
        return width, height


    @staticmethod
    def getImagePath( fileNode ):
        import maya.cmds as cmds
        return cmds.getAttr( fileNode + '.fileTextureName' )
    
    
    @staticmethod
    def getExtension( fileNode ):
        import maya.cmds as cmds
        return cmds.getAttr( fileNode + '.fileTextureName' ).split( '.' )[-1]
    

    @staticmethod
    def getFileNodesFromScene():
        import maya.cmds as cmds
        return cmds.ls( type='file' )


    @staticmethod
    def getFileNodesFormSelection():
        import maya.cmds as cmds
        meshs = InMaya.getMeshFromSelection()
        
        fileNodes = []
        
        if not meshs: return None
        
        for mesh in meshs:
            shadingEngines = cmds.listConnections( mesh + '.instObjGroups', type='shadingEngine' )
            if not shadingEngines: continue
            hists = cmds.listHistory( shadingEngines, pdo=1 )
            for hist in hists:
                if cmds.nodeType( hist ) == 'file':
                    fileNodes.append( hist )
        return fileNodes



def convertImageAndAssign( fileNode, convertExtension=None, width = None ):
    
    import maya.cmds as cmds
    filePath = InMaya.getImagePath( fileNode )
    origWidth, origHeight = InMaya.getImageSize( fileNode )
    
    replacePath = InStandalone.convertImage(filePath, None, convertExtension, width, origWidth )
    
    cmds.setAttr( fileNode + '.fileTextureName', replacePath, type='string' )