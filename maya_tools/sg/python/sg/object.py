import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
from sg import base as sgbase
from sg import data as sgdata



class SGPoint:
    
    def __init__(self, *args, **options ):
        
        if type( args[0] ) in [type([]), type(())]:
            self.m = OpenMaya.MPoint( *args[0] )
        elif type( args[0] ) == type(OpenMaya.MPoint()):
            self.m = args[0]
        elif type( args[0] ) in [type(1), type(1.0)]:
            self.m = OpenMaya.MPoint( *args )
        
    
    def list(self):
        return [ self.m.x, self.m.y, self.m.z ]
    
    
    def x(self):
        return self.m.x
    def y(self):
        return self.m.y
    def z(self):
        return self.m.z



class SGVector:
    
    def __init__(self, *args, **options ):
        
        if type( args[0] ) in [type([]), type(())]:
            self.m = OpenMaya.MVector( *args[0] )
        elif type( args[0] ) == type(OpenMaya.MVector()):
            self.m = args[0]
        elif type( args[0] ) in [type(1), type(1.0)]:
            self.m = OpenMaya.MVector( *args )
        
    
    def list(self):
        return [ self.m.x, self.m.y, self.m.z ]
    
    
    def x(self):
        return self.m.x
    def y(self):
        return self.m.y
    def z(self):
        return self.m.z




class SGMatrix:
    
    def __init__(self, *args, **options ):
        
        if type( args[0] ) in [type([]), type(())]:
            self.matrix = OpenMaya.MMatrix()
            OpenMaya.MScriptUtil.createMatrixFromList( args[0], self.matrix )
        elif type( args[0] ) == type(OpenMaya.MMatrix()):
            self.matrix = args[0]
        
    def list(self):
        mtxList = range( 16 )
        for i in range( 4 ):
            for j in range( 4 ):
                mtxList[ i * 4 + j ] = self.matrix( i, j )
        return mtxList





class SGAttribute:
    
    def __init__(self, *args ):
        
        if type( args[0] ) == SGNode:
            self.sgnode = args[0]
            self.attrName = args[1]
        elif type( args[0] ) == str:
            if args[0].find( '.' ) != -1:
                splits = args[0].split( '.' )
                self.sgnode = SGNode( splits[0] )
                self.attrName = splits[1]
            else:
                self.sgnode = SGNode( args[0] )
                self.attrName = args[1]


    def set(self, *values, **options ):
        cmds.setAttr( self.sgnode.name() + '.' +self. attrName, *values, **options )
        return self
        
    
    def setKeyable(self, keyValue=True):
        cmds.setAttr( self.sgnode.name()+'.'+self.attrName, e=1, k=keyValue )
        return self


    def setChannelBox(self, attrName, channelBoxValue=True):
        cmds.setAttr( self.sgnode.name()+'.'+self.attrName, e=1, cb=channelBoxValue )
        return self


    def get(self):
        return cmds.getAttr( self.sgnode.name() + '.' + self.attrName )
    
    
    def name(self):
        return self.sgnode.name() + '.' + self.attrName
    
    def node(self):
        return self.sgnode





class SGNode( object ):
    
    def __init__(self, nodeName ):
        
        self.mObject  = sgbase.getMObject( nodeName )
        self.mDagPath = sgbase.getDagPath( nodeName )


    def name(self):
        
        if self.mDagPath:
            fnDagNode = OpenMaya.MFnDagNode( self.mDagPath )
            return fnDagNode.partialPathName()
        else:
            fnNode = OpenMaya.MFnDependencyNode( self.mObject )
            return fnNode.name()
    
    
    def rename(self, inputName ):
        cmds.rename( self.name(), inputName )
    
    
    def apiType(self):
        return self.mObject.apiType()


    def apiTypeStr(self):
        return self.mObject.apiTypeStr()
    
    
    def nodeType(self):
        return cmds.nodeType( self.name() )
    
    
    def addAttr(self, *attrNames, **options ):
        
        defaultOptions = {}
        if len( attrNames ) > 2:
            defaultOptions.update( {'ln':attrNames[0]} )
            defaultOptions.update( {'sn':attrNames[1]} )
        elif len( attrNames ) == 1:
            defaultOptions.update( {'ln':attrNames[0]} )        
        options.update( defaultOptions )
        
        keys = options.keys()
        longName = None
        shortName = None
        if 'ln' in keys:
            longName = options['ln']
        elif 'longName' in keys:
            longName = options['longName']
        if 'sn' in keys:
            shortName = options['sn']
        elif 'shortName' in keys:
            shortName = options['shortName']
        
        attrExists = False
        if longName:
            if cmds.attributeQuery( longName, node= self.name(), ex=1 ):
                cmds.warning( "%s has already '%s'" %( self.name(), longName ))
                attrExists = True
        if shortName:
            if cmds.attributeQuery( shortName, node= self.name(), ex=1 ):
                cmds.warning( "%s has already '%s'" %( self.name(), shortName ))
                attrExists = True
        
        attrName = longName
        if shortName: attrName = shortName
        
        channelValue = None
        keyableValue = None
        for key, value in options.items():
            if key in ['cb', 'channelBox']:
                channelValue = value
                options.pop( key )
            elif key in ['k', 'keyable']:
                keyableValue = value 
                options.pop( key )
        
        if not attrExists:cmds.addAttr( self.name(), **options )
        if channelValue != None:
            cmds.setAttr( self.name()+'.'+attrName, e=1, cb=channelValue )
        if keyableValue != None:
            cmds.setAttr( self.name()+'.'+attrName, e=1, k=keyableValue )
        return self
    
    
    def setAttr(self, attrName, *values, **options ):
        cmds.setAttr( self.name() + '.' + attrName, *values, **options )
        return self
        
    
    def setKeyable(self, attrName, keyValue=True):
        cmds.setAttr( self.name()+'.'+attrName, e=1, k=keyValue )
        return self


    def setChannelBox(self, attrName, channelBoxValue=True):
        cmds.setAttr( self.name()+'.'+attrName, e=1, cb=channelBoxValue )
        return self
    
    
    def getAttr(self, attrName ):
        return cmds.getAttr( self.name() + '.' + attrName )
        
        
    def attr(self, attrName ):
        return SGAttribute( self, attrName )
        




class SGDagNode( SGNode ):
    
    def __init__(self, nodeName ):
        SGNode.__init__(self, nodeName)


    def position(self, **options ):
        defaultOptions = {'q':1, 't':1 }
        defaultOptions.update( options )
        return OpenMaya.MPoint( *cmds.xform( self.name(), **defaultOptions ) )
    
    
    def localName(self):
        fnDagNode = OpenMaya.MFnDagNode( self.mDagPath )
        return fnDagNode.name()
    
    
    def fullPathName(self):
        fnDagNode = OpenMaya.MFnDagNode( self.mDagPath )
        return fnDagNode.fullPathName()

    
    def matrix(self):
        return SGMatrix(cmds.getAttr( self.name() + '.m' ))


    def worldMatrix(self):
        return SGMatrix(cmds.getAttr( self.name() + '.wm' ))
    
    
    def parent(self):
        parents = cmds.listRelatives( self.name(), p=1, f=1 )
        if not parents: return None
        return SGDagNode( parents[0] )
    
    
    def transform(self):
        if self.apiTypeStr() in sgdata.ApiType.transform:
            return self
        return self.parent()


    def shape(self):
        if self.apiTypeStr() in sgdata.ApiType.shape:
            return self
        children = cmds.listRelatives( self.name(), c=1, s=1, f=1 )
        if not children: return None
        for child in children:
            if cmds.getAttr( child + '.io' ): continue
            return SGDagNode( child )
        
        for child in children:
            return SGDagNode( child )
    


    def shapes(self):
        if self.apiTypeStr() in sgdata.ApiType.shape:
            return [self]
        children = cmds.listRelatives( self.name(), c=1, s=1, f=1 )
        if not children: return []
        dagNodes = []
        for child in children:
            dagNodes.append( SGDagNode( child ) )
        return dagNodes
    


    def getNodeFromHistory( self, historyType, **options ):
    
        hists = cmds.listHistory( self.name(), **options )
        
        if not hists: return []
        
        returnTargets = []
        for hist in hists:
            if cmds.nodeType( hist ) == historyType:
                node = None
                if cmds.nodeType( hist ) in sgdata.NodeType.dag:
                    node = SGDagNode( hist )
                else:
                    node = SGNode( hist )
                returnTargets.append( node )
        return returnTargets
        
