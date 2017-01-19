import maya.cmds as cmds
from sg import data as sgdata
from sg import object as sgo



def loadPlugin( pluginName ):
    
    if not cmds.pluginInfo( pluginName, q=1, l=1 ):
        cmds.loadPlugin( pluginName )

loadPlugin( 'matrixNodes' )



def convertArgs( args ):
    newArgs = []
    for arg in args:
        if type( arg ) in [str, unicode]:
            newArgs.append( arg )
        else:
            newArgs.append( arg.name() )
    return newArgs



def convertSg( nodeName ):
    if not type( nodeName ) in [str, unicode]: return nodeName
    nodeType = cmds.nodeType( nodeName )
    if nodeType in sgdata.NodeType.dag:
        sgNode = sgo.SGDagNode( nodeName )
    else:
        sgNode = sgo.SGNode( nodeName )
    return sgNode



def convertName( node ):
    if type( node ) in [str, unicode]:
        return node.name()
    return node




def listNodes( *args, **options ):
    
    nodes = cmds.ls( *args, **options )
    
    sgNodes = []
    for node in nodes:
        sgNodes.append( convertSg( node ) )
    
    return sgNodes



def listConnections( *args, **options ):
    
    newArgs = convertArgs( args )
    cons = cmds.listConnections( *newArgs, **options )
    if not cons: return []
    
    sgcons = []
    for con in cons:
        if con.find( '.' ) != -1:
            sgcons.append( sgo.SGAttribute( con ) )
        else:
            sgcons.append( sgo.SGNode( con ) )
    
    return sgcons



def createNode( *args, **options ):
    
    nodeName = cmds.createNode( *args, **options )
    return convertSg( nodeName )