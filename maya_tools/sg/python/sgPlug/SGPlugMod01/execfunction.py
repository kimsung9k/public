
class SGMPlugMod01_markingMenuCmd:
    
    import maya.cmds as cmds
    import maya.mel as mel
    import sg.file
    import cPickle
    
    modeFilePath = uiInfoPath = cmds.about(pd=True) + "/sg_toolInfo/SGMPlugMod01.txt"
    sg.file.makeFile( modeFilePath )
    
    f = open( modeFilePath, 'r' )
    data = cPickle.load( f )
    f.close()
    
    try:
        data['mode']; data['symmetry']
        mel.eval( "SGMPlugMod01Command -sym %d" % data['symmetry'] ) 
    except:
        f = open( modeFilePath, 'w' )
        cPickle.dump( {'mode':0, 'symmetry':0 }, f )
        f.close()

    @staticmethod
    def deleteHistory( evt=0 ):
        import maya.cmds as cmds
        import sg.mod
        import sg.get
        cuSels = cmds.ls( sl=1 )
        shapes = sg.get.shapesOfComponentSelected()
        for shape in shapes:
            sg.mod.deleteHistory( shape )
        cmds.select( cuSels );
    
    @staticmethod
    def collapseEdge( evt=0 ):
        import maya.cmds as cmds
        cmds.polyCollapseEdge()
        cmds.select( cl=1 )
    
    @staticmethod
    def extrudeFace( evt=0 ):
        import maya.cmds as cmds
        import maya.mel as mel
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.polyExtrudeFacet( ch=1, kft=1, d=1, twist=0, taper=1, off=0, tk=0, sma=30, ltz=0 )
        mel.eval( "SGMPlugMod01Command -upm" )
        pass
    
    @staticmethod
    def averageNormal( evt=0 ):
        import maya.mel as mel
        import sg.mod
        mel.eval( "SGMPlugMod01Command -upc" )
        sg.mod.averageNormal()
        mel.eval( "SGMPlugMod01Command -upc" )
    
    @staticmethod
    def averageVertex( evt=0 ):
        import maya.cmds as cmds
        import maya.mel as mel
        mel.eval( "SGMPlugMod01Command -upc" )
        cmds.polyAverageVertex()
        mel.eval( "SGMPlugMod01Command -upc" )
    
    @staticmethod
    def deleteEdge( evt=0 ):
        import maya.cmds as cmds
        cmds.DeleteEdge()
        cmds.select( cl=1 )
        
    @staticmethod
    def fillhole( evt=0 ):
        import maya.cmds as cmds
        cmds.FillHole()
        cmds.select( cl=1 )
    
    @staticmethod
    def bevelEdge( evt=0 ):
        import maya.cmds as cmds
        import maya.mel as mel
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.polyBevel( f =0.5, oaf=1, af=1, sg=1, ws=1, sa=30, fn=1, mv=0, ma=180, at=180 )
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.select( cl= 1 )
    
    @staticmethod
    def updateData( data ):
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'r' )
        origData = SGMPlugMod01_markingMenuCmd.cPickle.load( f )
        f.close()
        origData.update( data )
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'w' )
        SGMPlugMod01_markingMenuCmd.cPickle.dump( origData, f )
        f.close()
    
    @staticmethod
    def getData( key ):
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'r' )
        origData = SGMPlugMod01_markingMenuCmd.cPickle.load( f )
        f.close()
        return origData[key]
    
    
    @staticmethod
    def setDefaultMode( evt=0 ):
        SGMPlugMod01_markingMenuCmd.updateData( {'mode':0} )
        
        
    @staticmethod
    def setMoveBrushMode( evt=0 ):
        SGMPlugMod01_markingMenuCmd.updateData( {'mode':1} )


    @staticmethod
    def setSculptMode( evt=0 ):
        SGMPlugMod01_markingMenuCmd.updateData( {'mode':2} )
    
    @staticmethod
    def symmetryXOn( evt=0 ):
        import maya.mel as mel
        
        f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'r' )
        data = SGMPlugMod01_markingMenuCmd.cPickle.load( f )
        f.close()
        
        if SGMPlugMod01_markingMenuCmd.getData( 'symmetry' ) == 0:
            SGMPlugMod01_markingMenuCmd.updateData( {'symmetry':1} )
            mel.eval( "SGMPlugMod01Command -sym 1")
            data.update( {'symmetry': 1} )
        else:
            SGMPlugMod01_markingMenuCmd.updateData( {'symmetry':0} )
            mel.eval( "SGMPlugMod01Command -sym 0")
            data.update( {'symmetry': 0} )
        
        
    
    @staticmethod
    def duplicateAndAddFace( evt=0 ):
        import maya.mel as mel
        import maya.OpenMaya as OpenMaya
        import sg.get
        import sg.format
        sels = sg.get.activeSelectionApi()
        
        mel.eval( "SGMPlugMod01Command -upm" )
        commandName = "select "
        for dagPath, oComp in sels:
            singleComp = OpenMaya.MFnSingleIndexedComponent( oComp )
            compIndices = OpenMaya.MIntArray()
            singleComp.getElements( compIndices )
            sgFormatMesh = sg.format.Mesh( dagPath )
            newIndices = sgFormatMesh.duplicateAndAddFace( compIndices )
            meshName = OpenMaya.MFnMesh( dagPath ).partialPathName()
            
            for i in range( len( newIndices ) ):
                commandName += " %s.f[%d]" %( meshName, newIndices[i] )
        mel.eval( "SGMPlugMod01Command -upm" )
        
        mel.eval( commandName )
    
    @staticmethod
    def addDivision( evt=0 ):
        import maya.cmds as cmds
        import maya.mel as mel
        if not cmds.ls( sl=1 ): return None
        mel.eval( "SGMPlugMod01Command -upm" )
        cmds.polySubdivideFacet( dv=1, m=0, ch=1 )
        mel.eval( "SGMPlugMod01Command -upm" )



def SGMPlugMod01Command_markingMenu_defaultMenu( parentName ):
    import maya.cmds as cmds
    import maya.mel as mel
    import cPickle
    cmds.menuItem( l="Mode", p=parentName, sm=1, rp='N')
    cmds.radioMenuItemCollection()
    modeFirst = cmds.menuItem( l="Default Mode", rp='NE',c= SGMPlugMod01_markingMenuCmd.setDefaultMode, rb=1 )
    modeSecond = cmds.menuItem( l="Move Brush Mode", rp='E', c = SGMPlugMod01_markingMenuCmd.setMoveBrushMode, rb=0 )
    modeThird = cmds.menuItem( l="Sculpt Mode", rp='SE', c= SGMPlugMod01_markingMenuCmd.setSculptMode, rb=0 )
    f = open( SGMPlugMod01_markingMenuCmd.modeFilePath, 'r' )
    data = cPickle.load(f)
    f.close()
    try:
        if data['mode'] == 0: cmds.menuItem( modeFirst, e=1, rb=1 )
        elif data['mode'] == 1: cmds.menuItem( modeSecond, e=1, rb=1 )
        elif data['mode'] == 2: cmds.menuItem( modeThird, e=1, rb=1 )
    except:pass
    symmetryX = cmds.menuItem( "Symmetry X", cb=0, rp="W", c=SGMPlugMod01_markingMenuCmd.symmetryXOn  )
    try:
        if data['symmetry'] == 0: 
            cmds.menuItem( symmetryX, e=1, cb=0 )
            mel.eval( "SGMPlugMod01Command -sym 0")
        elif data['symmetry'] == 1: 
            cmds.menuItem( symmetryX, e=1, cb=1 )
            mel.eval( "SGMPlugMod01Command -sym 1")
    except:pass
    
    cmds.menuItem( l="Average", p=parentName, sm=1, rp='NW' )
    cmds.menuItem( l="Average Normal", rp="NW", c = SGMPlugMod01_markingMenuCmd.averageNormal )
    cmds.menuItem( l="Average Vertex", rp="W",  c = SGMPlugMod01_markingMenuCmd.averageVertex )
    cmds.menuItem( l="Delete History", p = parentName, c = SGMPlugMod01_markingMenuCmd.deleteHistory )


def SGMPlugMod01Command_markingMenu_edgeMenu( parentName ):
    import maya.cmds as cmds
    SGMPlugMod01Command_markingMenu_defaultMenu( parentName )
    cmds.menuItem( l="Collapse Edge",  p = parentName, rp="NE", c = SGMPlugMod01_markingMenuCmd.collapseEdge )
    cmds.menuItem( l="Bevel Edge", p=parentName, rp="E", c= SGMPlugMod01_markingMenuCmd.bevelEdge )
    cmds.menuItem( l="Delete Edge",  p = parentName, rp="SW", c = SGMPlugMod01_markingMenuCmd.deleteEdge )
    cmds.menuItem( l="Fill Hole", p = parentName, c= SGMPlugMod01_markingMenuCmd.fillhole )
    
    cmds.menuItem( l="Convert Selection", p=parentName, sm=1, rp='W' )
    cmds.menuItem( l="")
    

def SGMPlugMod01Command_markingMenu_polyMenu( parentName ):
    import maya.cmds as cmds
    SGMPlugMod01Command_markingMenu_defaultMenu( parentName )
    cmds.menuItem( l="Extrude Face",  p = parentName, rp="NE", c = SGMPlugMod01_markingMenuCmd.extrudeFace )
    cmds.menuItem( l="Duplicate and Add Face",  p = parentName, rp="E", c = SGMPlugMod01_markingMenuCmd.duplicateAndAddFace )
    cmds.menuItem( l="Add division", p= parentName, rp="SE", c= SGMPlugMod01_markingMenuCmd.addDivision )


def SGMPlugMod01Command_markingMenu_vtxMenu( parentName ):
    SGMPlugMod01Command_markingMenu_defaultMenu( parentName )
