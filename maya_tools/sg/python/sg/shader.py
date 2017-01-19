import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
import sg.node
import sg.dag
import sg.attribute




def setDefaultShader( target ):
    
    cmds.select( target )
    cmds.sets( e=1, forceElement = 'initialShadingGroup' )




def setFacingShader( target ):
    
    shader, shadingSG = sg.node.shaderAndSet( "surfaceShader" )
    cmds.sets( target, e=1, forceElement= shadingSG )
    
    ramp = cmds.shadingNode( 'ramp', asTexture=1 )
    samplerInfo = cmds.shadingNode( 'samplerInfo', asUtility=1 )
    cmds.connectAttr( samplerInfo + '.facingRatio', ramp + '.vCoord', f=1 )
    
    cmds.connectAttr(ramp + '.outColor', shader + '.outColor' )




def getShaderAndEngine( shapeNode ):
    
    shapeNode = sg.dag.getShape( shapeNode )
    engines = cmds.listConnections( shapeNode, s=0, d=1, type="shadingEngine" )
    if not engines: return None
    shaders = []
    for engine in engines:
        shader = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shader: continue
        shaders += shader
    
    return shaders, engines




def opaqueToBlinn( target ):
    
    meshs = sg.get.nonIoMesh(target)
    
    for mesh in meshs:
        shaders, engines = getShaderAndEngine( mesh )
        
        for shader in shaders:
            blinn, blinnSG = sg.node.shaderAndSet( "blinn" )
            cmds.sets( mesh, e=1, forceElement=blinnSG )
            
            colorSrcs = cmds.listConnections( shader + '.diffuseColor', s=1, d=0, p=1 )
            if colorSrcs:
                cmds.connectAttr( colorSrcs[0], blinn+'.color' )
            else:
                colors = cmds.getAttr( shader + '.diffuseColor' )[0]
                cmds.setAttr( blinn+'.color', colors[0], colors[1], colors[2], type="double3" )



def opaqueToSurface( target ):
    
    meshs = sg.get.nonIoMesh(target)
    
    for mesh in meshs:
        engines = cmds.listConnections( mesh, s=0, d=1, type="shadingEngine" )
        if not engines: continue
        shaders = cmds.listConnections( engines[0]+'.surfaceShader', s=1, d=0, type='ifmOpaque' )
        if not shaders: continue
        
        surface, surfaceSG = sg.node.shaderAndSet( "surfaceShader" )
        cmds.sets( mesh, e=1, forceElement=surfaceSG )
        
        colorSrcs = cmds.listConnections( shaders[0] + '.diffuseColor', s=1, d=0, p=1 )
        if colorSrcs:
            cmds.connectAttr( colorSrcs[0], surface+'.outColor' )
        else:
            colors = cmds.getAttr( shaders[0] + '.diffuseColor' )[0]
            cmds.setAttr( surface+'.outColor', colors[0], colors[1], colors[2], type="double3" )



def resetOpaque( target ):
    
    meshs = sg.get.nonIoMesh(target)
    
    for mesh in meshs:
        engines = cmds.listConnections( mesh, s=0, d=1, type="shadingEngine" )
        if not engines: continue
        shaders = cmds.listConnections( engines[0]+'.surfaceShader', s=1, d=0, type='ifmOpaque' )
        if not shaders: continue
        
        newOpaque, newOpaqueSG = sg.node.shaderAndSet( "ifmOpaque", n=shaders[0]+"_re" )
        print newOpaque, newOpaqueSG
        cmds.sets( mesh, e=1, forceElement=newOpaqueSG )
        
        colorSrcs = cmds.listConnections( shaders[0] + '.diffuseColor', s=1, d=0, p=1 )
        if colorSrcs:
            cmds.connectAttr( colorSrcs[0], newOpaque+'.diffuseColor' )
        else:
            colors = cmds.getAttr( shaders[0] + '.diffuseColor' )[0]
            cmds.setAttr( newOpaque+'.diffuseColor', colors[0], colors[1], colors[2], type="double3" )
        
        cmds.setAttr( newOpaque + ".specularWeight",    cmds.getAttr( shaders[0] + '.specularWeight' ) )
        cmds.setAttr( newOpaque + ".specularRoughness", cmds.getAttr( shaders[0] + '.specularRoughness' ) )




class ShaderInfo:
    
    def __init__(self, shapeNode ):
        
        engines = cmds.listConnections( shapeNode, s=0, d=1, type="shadingEngine" )
        if not engines: return None
        shaders = cmds.listConnections( engines[0]+'.surfaceShader', s=1, d=0, type='ifmOpaque' )
        if not shaders: return None
        
        shader = shaders[0]
        shaderType = cmds.nodeType(shader)
        attrList = ShaderInfo.getAttrList( shaderType )
        
        self.nodeDict = {'shapeNode':shapeNode, 'shaderType':shaderType, 'attrDicts':[] }
        for attr in attrList:
            attrDict = ShaderInfo.attrInfoDict( shader + '.' + attr )
            self.nodeDict['attrDicts'].append( attrDict )


    @staticmethod
    def getShaderAttrDict( attrName ):
    
        attr = attrName.split( '.' )[-1]
        returnDict = {'attr':attr}
        attrConnections = cmds.listConnections( attrName, s=1, d=0, p=1 )
    
        returnDict.update( {'attrType':cmds.getAttr( attrName, type=1 )} )
        if not attrConnections:
            returnDict.update( {'attrValue':cmds.getAttr( attrName )})
        else:
            srcNode, srcAttr = attrConnections[0].split( '.' )
            returnDict.update( {'srcType':cmds.nodeType(srcNode)} )
            returnDict.update( {'srcAttr':srcAttr} )
        
        return returnDict


    @staticmethod
    def getAttrList( nodeType ):
        
        if nodeType == "ifmOpaque":
            attrList = ['diffuseColor', 'specularWeight', 'specularRoughness' ]
        elif nodeType == "surfaceShader":
            attrList = ['outColor']
        return attrList
    
    
    @staticmethod
    def setShaderByInfo( shaderInfo, srcPrefix=None, dstPrefix=None ):
        
        shapeNode  = shaderInfo.nodeDict['shapeNode']
        shaderType = shaderInfo.nodeDict['shaderType']
        attrDicts  = shaderInfo.nodeDict['attrDicts']
        
        if srcPrefix: shapeNode = shapeNode.replace( srcPrefix, dstPrefix )
        if not cmds.objExists( shapeNode ): cmds.error( "'%s' is not exists" % shapeNode )
        
        shaders, engines = getShaderAndEngine( shapeNode )
        
        if cmds.nodeType( shaders[0] ) == shaderType:
            targetShader = shaders[0]
        else:
            targetShader, engine = getShaderAndEngine( shaderType )
        
        for attrDict in attrDicts:
            if attrDict.has_key('srcType'):
                srcType = attrDict['srcType']
            

def copyShader( first, second ):
    
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    first  = sg.dag.getTransform( first )
    second = sg.dag.getTransform( second )
    firstShape = sg.dag.getShape( first )
    secondShape = sg.dag.getShape( second )
    
    engines = cmds.listConnections( firstShape, type='shadingEngine' )
    
    if not engines: return None
    
    engines = list( set( engines ) )
    
    for engine in engines:
        shaders = cmds.listConnections( engine+'.surfaceShader', s=1, d=0 )
        if not shaders: continue
        shader = shaders[0]
        cmds.hyperShade( objects = shader )
        selObjs = cmds.ls( sl=1 )
        
        targetObjs = []
        for selObj in selObjs:
            if selObj.find( '.' ) != -1:
                trNode, components = selObj.split( '.' )
                if trNode == first:
                    targetObjs.append( second+'.'+components )
            elif selObj == firstShape:
                targetObjs.append( secondShape )
        
        if not targetObjs: continue
        
        for targetObj in targetObjs:
            cmds.sets( targetObj, e=1, forceElement=engine )



def getBumpNode( shader ):
    
    srcAttrs = cmds.listConnections( shader + '.normalCamera', s=1, d=0, p=1 )
    if not srcAttrs:
        bumpNode = cmds.shadingNode( 'bump2d', asUtility=1 )
        cmds.connectAttr( bumpNode + '.outNormal', shader + '.normalCamera' )
        cmds.setAttr( bumpNode + '.bumpInterp', 1 )
        return bumpNode
    bumpNode, outputAttr = srcAttrs[0].split( '.' )
    
    return bumpNode



def getBumpTexture( bumpNode ):
    
    srcAttr = cmds.listConnections( bumpNode + '.bumpValue', s=1, d=0, p=1 )
    if not srcAttr:
        fileNode = cmds.shadingNode( 'file', asTexture=1, isColorManaged=1 )
        cmds.connectAttr( fileNode + '.outAlpha', bumpNode + '.bumpValue' )
        return fileNode
    return srcAttr[0].split( '.' )[0]



def getBlendNormalTexture( shape ):
    
    shape = sg.dag.getShape( shape )
    if not shape: return None
    shaders, engines = getShaderAndEngine( shape )
    
    bumpNode = getBumpNode( shaders[0] )
    texture = getBumpTexture( bumpNode )
    
    if cmds.nodeType( texture ) != 'layeredTexture':
        layeredNode = cmds.shadingNode( 'layeredTexture', asTexture=1 )
        cmds.connectAttr( texture + '.outColor', layeredNode + '.inputs[0].color' )
        cmds.connectAttr( layeredNode + '.outAlpha', bumpNode + '.bumpValue', f=1 )
        return layeredNode
    else:
        return texture




def insertBlendNormalTexture( shape ):
    
    layeredTexture = getBlendNormalTexture( shape )
    
    fnNode = OpenMaya.MFnDependencyNode( sg.base.getMObject( layeredTexture ) )
    plugInputs = fnNode.findPlug( 'inputs' )
    
    numInputs = plugInputs.numElements()
    
    colorSrcs = [ None for i in range( numInputs ) ]
    alphaSrcs = [ None for i in range( numInputs ) ]
    logicalIndices = []
    for i in range( numInputs ):
        colorAttr = plugInputs[i].child( 0 ).name()
        colorAttrSrcs = cmds.listConnections( colorAttr, s=1, p=1, d=0 )
        if colorAttrSrcs:
            colorSrcs[i] = colorAttrSrcs[0]
            cmds.disconnectAttr( colorAttrSrcs[0], colorAttr )
        alphaAttr = plugInputs[i].child( 1 ).name()
        alphaAttrSrcs = cmds.listConnections( alphaAttr, s=1, p=1, d=0 )
        if alphaAttrSrcs:
            alphaSrcs[i] = alphaAttrSrcs[0]
            cmds.disconnectAttr( alphaAttrSrcs[0], alphaAttr )
        logicalIndices.append( plugInputs[i].logicalIndex() )
        
    ranges = range( numInputs )
    ranges.reverse()
    for i in ranges:
        logicalIndex = plugInputs[i].logicalIndex()
        cmds.removeMultiInstance( plugInputs.name() + '[%d]' % logicalIndex )
    
    newFile  = cmds.shadingNode( 'file', asTexture=1, isColorManaged=1 )
    maskFile = cmds.shadingNode( 'file', asTexture=1, isColorManaged=1 )
    cmds.connectAttr( newFile + '.outColor', plugInputs.name() + '[0].color' )
    cmds.connectAttr( maskFile + '.outColorR', plugInputs.name() + '[0].alpha' )
    
    for i in range( 1, numInputs + 1 ):
        if colorSrcs[i-1]:
            cmds.connectAttr( colorSrcs[i-1], plugInputs.name() + '[%d].color' % i )
        if alphaSrcs[i-1]:
            cmds.connectAttr( alphaSrcs[i-1], plugInputs.name() + '[%d].alpha' % i )




def addAlphaBlendTexture( shape ):
    
    layeredTexture = getBlendNormalTexture( shape )
    
    fnNode = OpenMaya.MFnDependencyNode( sg.base.getMObject( layeredTexture ) )
    plugInputs = fnNode.findPlug( 'inputs' )
    
    numInputs = plugInputs.numElements()
    
    for i in range( numInputs ):
        alphaAttr = plugInputs[i].child( 1 ).name()
        alphaAttrSrc = cmds.listConnections( alphaAttr, s=1, p=1, d=0 )
        if not alphaAttrSrc:
            maskFile = cmds.shadingNode( 'file', asTexture=1, isColorManaged=1 )
            cmds.connectAttr( maskFile + '.outColorR', plugInputs[i].name() + '.alpha' )
            alphaAttrSrc = [maskFile + '.outColorR']
        
        if cmds.nodeType( alphaAttrSrc[0].split( '.' )[0] ) != 'plusMinusAverage':
            plusNode = cmds.shadingNode( 'plusMinusAverage', asUtility=1 )
            multNode = cmds.shadingNode( 'multDoubleLinear', asUtility=1 )
            cmds.connectAttr( alphaAttrSrc[0], multNode + '.input1' )
            cmds.connectAttr( multNode + '.output', plusNode + '.input1D[0]' )
            cmds.connectAttr( plusNode + '.output1D', alphaAttr, f=1 )
        else:
            plusNode = alphaAttrSrc[0].split( '.' )[0]
        
        lastIndex = sg.attribute.getLastElementIndex( plusNode + '.input1D' )
        print plusNode + '.input1D', lastIndex
        
        maskfile = cmds.shadingNode( 'file', asTexture=1, isColorManaged=1 )
        multNode = cmds.shadingNode( 'multDoubleLinear', asUtility=1 )
        cmds.connectAttr( maskfile + '.outColorR', multNode + '.input1' )
        cmds.connectAttr( multNode + '.output', plusNode + '.input1D[%d]' % (lastIndex+1) )
        
        break




def clearNormalBlendConnection( shape ):
    
    shaders, engines = getShaderAndEngine( shape )
    layeredTexture = getBlendNormalTexture( shape )
    
    fnNode = OpenMaya.MFnDependencyNode( sg.base.getMObject( layeredTexture ) )
    plugInputs = fnNode.findPlug( 'inputs' )
    
    numInputs = plugInputs.numElements()
    lastIndex = plugInputs[numInputs-1].logicalIndex()
    
    fileNode = cmds.listConnections( fnNode.name() + '.inputs[%d].color' % lastIndex )[0]
    bumpNode = getBumpNode( shaders[0] )
    
    cmds.connectAttr( fileNode + '.outAlpha', bumpNode + '.bumpValue', f=1 )
    sg.node.deleteSources( layeredTexture, [fileNode] )
    cmds.delete( layeredTexture )

