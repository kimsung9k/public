import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import os
import shutil
import cPickle
import sg.get
import sg.shader
import sg.scene




def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName


def makeFile( filePath ):
    if os.path.exists( filePath ): return None
    filePath = filePath.replace( "\\", "/" )
    splits = filePath.split( '/' )
    folder = '/'.join( splits[:-1] )
    makeFolder( folder )
    f = open( filePath, "w" )
    f.close()
    



def getProjectDir():
    return cmds.about(pd=True)




def exportModel( target, fileName, replace = False ):
    
    sceneName = cmds.file( q=1, sceneName=1 )
    targetPath = "/".join( sceneName.split( '/' )[:-1] ) + "/" + fileName +".mb"

    if replace:
        cmds.file( targetPath, f=1, options="v=0;", typ="mayaBinary", es=1 )
    else:
        cmds.file( targetPath, options="v=0;", typ="mayaBinary", es=1 )




def exportParts( targets, **options ):
    
    sceneName = cmds.file( q=1, sceneName=1 )
    splits = sceneName.split( '/' )
    folderPath = '/'.join( splits[:-1] ) + "/" + splits[-1].split( '.' )[0]
    
    makeFolder( folderPath )
    
    for target in targets:
        cmds.select( target )
        cmds.file( folderPath + "/" + target , **options )





def exportShaderInfo( targets, filePath ):
    
    meshs = []
    for target in targets:
        meshs += sg.get.nonIoMesh(target)
    
    shaderInfos = []
    for mesh in meshs:
        shaderInfo = sg.shader.ShaderInfo( mesh )
        shaderInfos.append( shaderInfo )
    
    filePath = filePath.replace( '\\', '/' )
    splits = filePath.split( '/' )
    
    folderPath = '/'.join( splits[:-1] )
    makeFolder( folderPath )
    
    confirmFile = False
    if os.path.exists( filePath ):
        confirmFile = cmds.confirmDialog( title='Confirm', message='File is exists.\nDo you want to replace it?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    else:
        confirmFile = True
    
    if not confirmFile: return False
    
    f = open( filePath, 'w' )
    cPickle.dump( shaderInfos, f )
    f.close()



def importShaderInfo( filePath, replaceSrc=None, replaceDst=None ):

    if not os.path.exists( filePath ): 
        cmds.error( 'Path is not exists' )
        return False
    
    f = open( filePath, 'r' )
    shaderInfos = cPickle.load( f )
    f.close()
    
    for shaderInfo in shaderInfos:
        sg.shader.ShaderInfo.setShaderByInfo( shaderInfo, replaceSrc, replaceDst )



def exportTransform():
    
    import json
    
    transformNode = cmds.ls( sl=1 )[0]
    
    filePath = getProjectDir() + '/sg_toolInfo/transformInfo.txt'
    makeFile( filePath )
    trPos = cmds.xform( transformNode, q=1, ws=1, matrix=1 )
    f = open( filePath, 'w' )
    json.dump( trPos, f )
    f.close()
    
    
def importTransform():
    
    import json
    
    filePath = getProjectDir() + '/sg_toolInfo/transformInfo.txt'
    if not os.path.exists( filePath ): return None
    f = open( filePath, 'r' )
    data = json.load( f )
    sels = cmds.ls( sl=1 )
    for sel in sels:
        cmds.xform( sel, ws=1, matrix= data )



def exportAnimation( topTransforms, ns='bake', exportPath=None ):
    
    import cPickle
    
    sg.convert.singleToList( topTransforms )
    
    hidedObjs = []
    for topTransform in topTransforms:
        if cmds.getAttr( topTransform + '.v' ):
            try:
                cmds.setAttr( topTransform + '.v', 0 )
                hidedObjs.append( topTransform )
            except:pass
    cmds.showHidden( topTransforms, a=1 )

    sceneName = cmds.file( q=1, sceneName=1 )
    sceneFolderName = '/'.join( sceneName.split( '/' )[:-1] )
    
    if exportPath:
        fileName = exportPath
    else:
        fileName = getProjectDir() + '/animation/bake.txt'

    makeFile( fileName )
    panel = sg.scene.getCurrentPanel()    
    
    try:cmds.isolateSelect( panel, state=1 )
    except:pass
    
    minTime = cmds.playbackOptions( q=1, minTime=1 )
    maxTime = cmds.playbackOptions( q=1, maxTime=1 )
    
    children = cmds.listRelatives( topTransforms, c=1, ad=1 )
    
    bakeInfos = []
    for child in children:
        attrs = cmds.listAttr( child, k=1 )
        childDict = {}
        childDict.update( {"attrs" : attrs} )
        values = []
        conExists = []
        for attr in attrs:
            value = cmds.getAttr( child + '.' + attr )
            values.append( value )
            cons = cmds.listConnections( child + '.' + attr, s=1, d=0, p=1, c=1 )
            conExist = False
            if not cons:
                parentAttrs = cmds.attributeQuery( attr, node=child, listParent=1 )
                if parentAttrs and cmds.listConnections( child + '.' + parentAttrs[0], s=1, d=0 ):
                    conExist = True
            else:
                conExist = True
            conExists.append( conExist )
        childDict.update( {"values" : values } )
        childDict.update( {"conExits" : conExists } )
        bakeInfos.append( childDict )

    for i in range( int(minTime), int(maxTime) + 1 ):
        cmds.currentTime( i )
        
        for bakeInfo in bakeInfos:
            attrs = bakeInfo['attrs']
            conExists = bakeInfo['conExists']
            valuesPerFrame = bakeInfo['valuesPerFrame']
            
        
    
    f = open( fileName, 'w' )
    f.write( fileName )
    f.close()
    
    try:cmds.isolateSelect( panel, state=0 )
    except:pass




def importAnimation( setGroup, importPath=None, *skipTargets ):

    import cPickle
    
    if importPath:
        fileName = importPath
    else:
        fileName = getProjectDir() + '/animation/bake.txt'
    
    
    


def reloadModules( pythonPath='' ):

    import os, imp, sys
    
    if not pythonPath:
        pythonPath = __file__.split( '\\' )[0]
    
    for root, folders, names in os.walk( pythonPath ):
        root = root.replace( '\\', '/' )
        for name in names:
            try:onlyName, extension = name.split( '.' )
            except:continue
            if extension.lower() != 'py': continue
            
            if name == '__init__.py':
                fileName = root
            else:
                fileName = root + '/' + name
                
            moduleName = fileName.replace( pythonPath, '' ).split( '.' )[0].replace( '/', '.' )[1:]
            moduleEx =False
            try:
                sys.modules[moduleName]
                moduleEx = True
            except:
                pass
            
            if moduleEx:
                reload( sys.modules[moduleName] )
    
    
    


    