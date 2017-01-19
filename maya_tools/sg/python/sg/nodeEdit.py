import maya.cmds as cmds
import sg.attribute


def createZeroToOneAndReverseNodes( node, attrName ):
    
    sg.attribute.addAttr( node, ln=attrName, min=0, max=1, k=1 )

    md1 = cmds.createNode( 'multDoubleLinear' )
    md2 = cmds.createNode( 'multDoubleLinear' )
    rev = cmds.createNode( 'reverse' )
    
    cmds.connectAttr( node + '.' + attrName, md1 + '.input1' )
    cmds.connectAttr( node + '.' + attrName, rev + '.inputX' )
    cmds.connectAttr( rev + '.outputX', md2 + '.input1' )
    
    return md1, md2



def createZroToOneAndReverseNodes_cb( node, evt=0 ):
    
    attr = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )[0]
    return createZeroToOneAndReverseNodes( node, attr )



def getSetRange( node, rangeValues=[0,1] ):
    
    connectedNode = cmds.listConnections( node + '.output', type= 'setRange' )
    
    if connectedNode:
       
        setRangeNode = connectedNode[0]
        minValue = cmds.getAttr( setRangeNode + '.minX' )
        maxValue = cmds.getAttr( setRangeNode + '.maxX' )
        
        if minValue == rangeValues[0] and maxValue == rangeValues[1]:
            return connectedNode[0]
        
    
    setRange = cmds.createNode( 'setRange' )
    
    cmds.connectAttr( node + '.output', setRange + '.valueX' )
    cmds.setAttr( setRange + '.minX', rangeValues[0] )
    cmds.setAttr( setRange + '.maxX', rangeValues[1] )
    
    return setRange



def getAttributeBlender( node, attr ):
    
    pass
    