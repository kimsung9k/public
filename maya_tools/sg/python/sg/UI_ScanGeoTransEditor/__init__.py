import maya.cmds as cmds
import maya.OpenMaya as OpenMaya


class Win_Global:
    
    winName = 'sgui_scanGeoTransEditor'
    title = "UI - Scan Geo Trans Editor"
    width = 400
    height = 100
    
    infoPath = cmds.about(pd=True) + "/sg/sgui_scanGeoTransEditorInfo.txt"
    
    intf_lPoint = ''
    intf_fPoint = ''
    intf_rPoint = ''
    txf_baseMesh = ''



def listToMatrix( mtxList ):
    
    mtx = OpenMaya.MMatrix()
    OpenMaya.MScriptUtil.createMatrixFromList( mtxList, mtx )
    return mtx


def matrixToList( mtx ):
    
    mtxList = []
    for i in range( 4 ):
        for j in range( 4 ):
            mtxList.append( mtx(i,j) )
    return mtxList


def makeFolder( pathName ):
    
    import os
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



def copyShader( first, second ):
    
    if not cmds.objExists( first ): return None
    if not cmds.objExists( second ): return None
    
    firstShape = cmds.listRelatives( first, s=1, f=1 )[0]
    secondShapes = cmds.listRelatives( second, s=1, f=1 )
    
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
            else:
                targetObjs += secondShapes
        
        if not targetObjs: continue
        targetObjs = list( set( targetObjs ) )
        
        for targetObj in targetObjs:
            print "Target obj : ", targetObj
            cmds.sets( targetObj, e=1, forceElement=engine )



def addIOShape( target ):
    
    def getMObject( target ):
        mObject = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( target )
        selList.getDependNode( 0, mObject )
        return mObject
    
    def copyShapeToTransform( shape, target ):
        oTarget = getMObject( target )
        oMesh   = getMObject( shape )
        fnMesh  = OpenMaya.MFnMesh( oMesh )
        fnMesh.copy( oMesh, oTarget )
    
    targetShape = cmds.listRelatives( target, s=1, f=1 )[0]
    newShapeTr = cmds.createNode( 'transform' )
    copyShapeToTransform( targetShape, newShapeTr )
    copyShader( target, newShapeTr )
    newShapeName = cmds.listRelatives( newShapeTr, s=1, f=1 )[0]
    newShapeName = cmds.parent( newShapeName, target, add=1, shape=1 )
    cmds.delete( newShapeTr )
    newShapeName = cmds.rename( newShapeName, targetShape.split( '|' )[-1] + 'Cu' )
    cmds.setAttr( targetShape + '.io', 1 )
    return newShapeName



class Win_Cmd:
    
    @staticmethod
    def saveInfomation():
        
        import json, os
        str_baseMesh = cmds.textField( Win_Global.txf_baseMesh, q=1, tx=1 )
        value_lPoint = cmds.intField( Win_Global.intf_lPoint, q=1, v=1 )
        value_fPoint = cmds.intField( Win_Global.intf_fPoint, q=1, v=1 )
        value_rPoint = cmds.intField( Win_Global.intf_rPoint, q=1, v=1 )
        
        makeFolder( os.path.dirname( Win_Global.infoPath ) )
        
        f = open( Win_Global.infoPath, 'w' )
        json.dump( [str_baseMesh, value_lPoint, value_fPoint, value_rPoint], f )
        f.close()
    
    
    @staticmethod
    def loadInfomation():
        
        import json
        try:
            f = open( Win_Global.infoPath, 'r' )
            str_baseMesh, value_lPoint, value_fPoint, value_rPoint = json.load( f )
            cmds.textField( Win_Global.txf_baseMesh, e=1, tx=str_baseMesh )
            cmds.intField( Win_Global.intf_lPoint, e=1, v= value_lPoint )
            cmds.intField( Win_Global.intf_fPoint, e=1, v= value_fPoint )
            cmds.intField( Win_Global.intf_rPoint, e=1, v= value_rPoint )
        except:
            pass
        
        
    
    @staticmethod
    def getVertexNum():
        
        sels = cmds.ls( sl=1, fl=1 )
        if len( sels ) != 1:
            cmds.error( "You Must Select One Vertex" )
        return int( sels[0].split( 'vtx[' )[-1].replace(']','') )
    
    @staticmethod
    def getMeshFromSelection():
        
        sels = cmds.ls( sl=1, fl=1 )
        meshName = sels[0].split( '.' )[0]
        if cmds.nodeType( meshName ) == 'transform':
            meshShapes = cmds.listRelatives( meshName, s=1, f=1 )
            for meshShape in meshShapes:
                if cmds.getAttr( meshShape + '.io' ):continue
                return cmds.ls( meshShape )[0]
        if not cmds.nodeType( meshName ) == 'mesh':
            return None
        return meshName
    
    
    @staticmethod
    def loadLeftVertexNum( *args ):
        cmds.intField( Win_Global.intf_lPoint, e=1, v= Win_Cmd.getVertexNum() )
        meshName = Win_Cmd.getMeshFromSelection()
        if meshName and not cmds.textField( Win_Global.txf_baseMesh, q=1, tx=1 ):
            cmds.textField( Win_Global.txf_baseMesh, e=1, tx=meshName )
        

    @staticmethod
    def loadFrontVertexNum( *args ):
        cmds.intField( Win_Global.intf_fPoint, e=1, v= Win_Cmd.getVertexNum() )
        meshName = Win_Cmd.getMeshFromSelection()
        if meshName and not cmds.textField( Win_Global.txf_baseMesh, q=1, tx=1 ):
            cmds.textField( Win_Global.txf_baseMesh, e=1, tx=meshName )
        

    @staticmethod
    def loadRightVertexNum( *args ):
        cmds.intField( Win_Global.intf_rPoint, e=1, v= Win_Cmd.getVertexNum() )
        meshName = Win_Cmd.getMeshFromSelection()
        if meshName and not cmds.textField( Win_Global.txf_baseMesh, q=1, tx=1 ):
            cmds.textField( Win_Global.txf_baseMesh, e=1, tx=meshName )
    

    @staticmethod
    def loadBaseMesh( *args ):
        meshName = Win_Cmd.getMeshFromSelection()
        if meshName:
            cmds.textField( Win_Global.txf_baseMesh, e=1, tx=meshName )


    @staticmethod
    def editGeometry( *args ):
        
        sels = cmds.ls( sl=1 )
        
        baseMesh = cmds.textField( Win_Global.txf_baseMesh, q=1, tx=1 )
        numVtxLeft  = cmds.intField( Win_Global.intf_lPoint, q=1, v=1 )
        numVtxFront = cmds.intField( Win_Global.intf_fPoint, q=1, v=1 )
        numVtxRight = cmds.intField( Win_Global.intf_rPoint, q=1, v=1 )
        
        baseLeft = baseMesh + '.vtx[%d]' % numVtxLeft
        baseFront = baseMesh + '.vtx[%d]' % numVtxFront
        baseRight = baseMesh + '.vtx[%d]' % numVtxRight
        
        cuMesh = Win_Cmd.getMeshFromSelection()
        
        cuLeft = cuMesh + '.vtx[%d]' % numVtxLeft
        cuFront = cuMesh + '.vtx[%d]' % numVtxFront
        cuRight = cuMesh + '.vtx[%d]' % numVtxRight
    
        point_bl = OpenMaya.MVector( *cmds.xform( baseLeft, q=1, os=1, t=1 ) )
        point_bf = OpenMaya.MVector( *cmds.xform( baseFront, q=1, os=1, t=1 ) )
        point_br = OpenMaya.MVector( *cmds.xform( baseRight, q=1, os=1, t=1 ) )
        
        point_cl = OpenMaya.MVector( *cmds.xform( cuLeft, q=1, os=1, t=1 ) )
        point_cf = OpenMaya.MVector( *cmds.xform( cuFront, q=1, os=1, t=1 ) )
        point_cr = OpenMaya.MVector( *cmds.xform( cuRight, q=1, os=1, t=1 ) )
        
        vxBase = point_bl - point_br
        vzBase = point_bf - (( vxBase )/2 + point_bl)
        
        vxBase.normalize()
        vzBase.normalize()
        vyBase = vzBase ^ vxBase
        
        baseMtxList = [ vxBase.x, vxBase.y, vxBase.z, 0,
                    vyBase.x, vyBase.y, vyBase.z, 0,
                    vzBase.x, vzBase.y, vzBase.z, 0,
                    point_bf.x, point_bf.y, point_bf.z, 1 ]
        
        vxCu = point_cl - point_cr
        vzCu = point_cf - (( vxCu )/2 + point_cl)
        
        vxCu.normalize()
        vzCu.normalize()
        vyCu = vzCu ^ vxCu
        
        cuMtxList = [ vxCu.x, vxCu.y, vxCu.z, 0,
                  vyCu.x, vyCu.y, vyCu.z, 0,
                  vzCu.x, vzCu.y, vzCu.z, 0,
                  point_cf.x, point_cf.y, point_cf.z, 1 ]
        
        baseMtx = listToMatrix( baseMtxList )
        cuMtx   = listToMatrix( cuMtxList )
        
        transformData = cuMtx.inverse() * baseMtx
        
        Win_Cmd.saveInfomation()
        
        resultMtx = matrixToList( transformData )
        for i in range( 4 ):
            print '%5.3f, %5.3f, %5.3f, %5.3f' %( resultMtx[i*4 + 0], resultMtx[i*4 + 1], resultMtx[i*4 + 2], resultMtx[i*4 + 3])
        
        meshObj = cmds.listRelatives( cuMesh, p=1, f=1 )[0]
        trGeos = cmds.listConnections( cuMesh + '.inMesh', s=1, d=0, type='transformGeometry' )
        if not trGeos:
            newShape = addIOShape( meshObj )
            trGeo = cmds.createNode( 'transformGeometry' )
            cmds.connectAttr( cuMesh + '.outMesh', trGeo + '.inputGeometry' )
            cmds.connectAttr( trGeo + '.outputGeometry', newShape + '.inMesh' )
        else:
            trGeo = trGeos[0]
        cmds.setAttr( trGeo + '.transform', resultMtx, type='matrix' )
        cmds.move( 0.0097, 2.3097, 1.4471, meshObj + '.rotatePivot', meshObj + '.scalePivot', rpr=1 )
        
        cmds.select( sels )




class UI_baseMesh:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        tx_mesh = cmds.text( l="Base Mesh", width= 80, h=25 )
        txf_mesh = cmds.textField( h=25 )
        bt_loadMesh = cmds.button( l="Load Mesh", width=90, h=25, c=Win_Cmd.loadBaseMesh )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ ( tx_mesh, 'left', 0 ), ( tx_mesh, 'top', 0 ),
                              ( txf_mesh, 'top', 0 ), 
                              ( bt_loadMesh, 'right', 0 ), ( bt_loadMesh, 'top', 0 ) ],
                         ac=[ ( txf_mesh, 'left', 0, tx_mesh ), ( txf_mesh, 'right', 0, bt_loadMesh ) ] )
        
        Win_Global.txf_baseMesh = txf_mesh
        
        return form
    



class UI_vertexList:
    
    def __init__(self):
        
        pass 
    
    
    def create(self):
        
        form = cmds.formLayout()
        
        tx_lPoint = cmds.button( l="Load Left", c=Win_Cmd.loadLeftVertexNum )
        tx_fPoint = cmds.button( l="Load Front", c=Win_Cmd.loadFrontVertexNum )
        tx_rPoint = cmds.button( l="Load Right", c=Win_Cmd.loadRightVertexNum )
        intf_lPoint = cmds.intField( h=25 )
        intf_fPoint = cmds.intField( h=25 )
        intf_rPoint = cmds.intField( h=25 )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( tx_lPoint, 'right', 0 ), ( tx_lPoint, 'top', 0 ),
                              ( tx_fPoint, 'top', 0 ),
                              ( tx_rPoint, 'left', 0 ), ( tx_rPoint, 'top', 0 ),
                              ( intf_lPoint, 'right', 0 ),
                              ( intf_rPoint, 'left', 0 )],
                         ap=[ ( tx_lPoint, 'left', 0, 66.666 ), ( tx_rPoint, 'right', 0, 33.333 ),
                              ( intf_lPoint, 'left', 0, 66.666 ), ( intf_rPoint, 'right', 0, 33.333 ) ],
                         ac=[ ( tx_fPoint, 'right', 0, tx_lPoint ), ( tx_fPoint, 'left', 0, tx_rPoint ),
                              ( intf_fPoint, 'right', 0, intf_lPoint ), ( intf_fPoint, 'left', 0, intf_rPoint ),
                              ( intf_lPoint, 'top', 0, tx_lPoint ),
                              ( intf_fPoint, 'top', 0, tx_lPoint ),
                              ( intf_rPoint, 'top', 0, tx_lPoint ) ] )
        self.form = form
        
        Win_Global.intf_lPoint = intf_lPoint
        Win_Global.intf_fPoint = intf_fPoint
        Win_Global.intf_rPoint = intf_rPoint
        
        return form
        




class Win:
    
    def __init__(self):
        
        self.ui_baseMesh   = UI_baseMesh()
        self.ui_vertexList = UI_vertexList()
    
    
    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName, wnd=1 )
        
        cmds.window( Win_Global.winName, title= Win_Global.title )
        
        form = cmds.formLayout()
        ui_baseMesh = self.ui_baseMesh.create()
        ui_vertexListFrom = self.ui_vertexList.create()
        ui_editButton = cmds.button( l='Edit Selected Mesh Transform', c= Win_Cmd.editGeometry )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[ ( ui_baseMesh, 'top', 5 ), ( ui_baseMesh, 'right', 5 ), ( ui_baseMesh, 'left', 5 ),
                              ( ui_vertexListFrom, 'right', 5 ), ( ui_vertexListFrom, 'left', 5 ),
                              ( ui_editButton, 'right', 5 ), ( ui_editButton, 'left', 5 ), ( ui_editButton, 'bottom', 5 ) ],
                         ac=[ ( ui_vertexListFrom, 'top', 5, ui_baseMesh ),
                              ( ui_editButton, 'top', 5, ui_vertexListFrom ) ] )
        
        cmds.window( Win_Global.winName, e=1, width= Win_Global.width, height= Win_Global.height )
        cmds.showWindow( Win_Global.winName )
        
        Win_Cmd.loadInfomation()




