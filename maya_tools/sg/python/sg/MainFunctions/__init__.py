import maya.cmds as cmds
import sg.node
import sg.connect


def getConnectedAnimCurve( evt=0 ):
    
    import sg.Tool_createAnimCurve
    
    sels = cmds.ls( sl=1 )
    node = sels[0]
    attrs = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    
    targetAnimCurves = []
    for attr in attrs:
        destCons = cmds.listConnections( node + '.' + attr, s=0, d=1 )
        attrValue = cmds.getAttr( node + '.' + attr )
        
        if destCons:
            for con in destCons:
                if cmds.nodeType( con ) == 'unitConversion':
                    animCurves = cmds.listConnections( con + '.output', s=0, d=1, type='animCurve' )
                    if not animCurves: continue
                    for animCurve in animCurves:
                        animCurveValue = sg.connect.getAnimCurveValueAtFloatInput( animCurve, attrValue )
                        if animCurveValue > 0:
                            targetAnimCurves.append( animCurve )
                elif cmds.nodeType( con ).find( 'animCurve' ) != -1:
                    animCurveValue = sg.connect.getAnimCurveValueAtFloatInput( con, attrValue )
                    if animCurveValue > 0:
                        targetAnimCurves.append( con )
                        
                            
    if not targetAnimCurves:
        sg.Tool_createAnimCurve.show()
    
    cmds.select( targetAnimCurves )
    return targetAnimCurves
    
    
    
def connectNodeOutputToChannel( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    node = ''
    for sel in sels:
        nodeType = cmds.nodeType( sel )
        if nodeType.find( 'animCurve' ) != -1:
            node = sel
        elif nodeType in ['multDoubleLinear']:
            node = sel 
    
    if not node: return None
    
    selTarget = sels[-1]
    
    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    hol = cmds.channelBox( 'mainChannelBox', q=1, hol=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    if sma:
        cmds.connectAttr( node + '.output', selTarget + '.' + sma[0], f=1 )
    elif sha:
        cmds.connectAttr( node + '.output', hol[0] + '.' + sha[0], f=1 )



def addMultDoubleLinear( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    mds = []
    for sel in sels:
        nodeType = cmds.nodeType( sel )
        if nodeType.find( 'animCurve' ) == -1 and nodeType in ['multDoubleLinear','addDoubleLinear']: continue
        md = cmds.createNode( 'multDoubleLinear' )
        cmds.connectAttr( sel + '.output', md + '.input1' )
        mds.append( md )
    
    return mds



def addReverseNode( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    revNodes = []
    for sel in sels:
        nodeType = cmds.nodeType( sel )
        if nodeType.find( 'animCurve' ) == -1 and nodeType in ['multDoubleLinear','addDoubleLinear']: continue
        revNode = cmds.createNode( 'reverse' )
        cmds.connectAttr( sel + '.output', revNode + '.inputX' )
        revNodes.append( revNode )
    
    return revNodes



def getGreaterValue( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    second = sels[1]
    
    node = cmds.createNode( 'condition' )
    cmds.setAttr( node + '.operation', 2 )
    
    cmds.connectAttr( first + '.output', node + '.firstTerm' )
    cmds.connectAttr( second + '.output', node + '.secondTerm' )
    cmds.connectAttr( first + '.output', node + '.colorIfTrueR')
    cmds.connectAttr( second + '.output', node + '.colorIfFalseR' )
    
    
    
def replaceConnection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    if len( sels ) < 3: return None
    
    first = sels[0]
    second = sels[1]
    third = sels[2]
    
    sg.connect.replace( first, second, third )




def getSourceConnection( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    if len( sels ) < 2: return None
    
    targets = sels[:-1]
    src = sels[-1]
    
    sg.connect.getSourceConnection(targets, src )





def getConnectionFromChannelBox( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    hol = cmds.channelBox( 'mainChannelBox', q=1, hol=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    node = ''
    attrs = []
    
    if sha:
        node = hol[0]
        attrs = sha
    else:
        for sel in sels:
            if hol and sel in hol: continue
            node = sel
            break
        attrs = sma
    
    cons = []
    for attr in attrs:
        cons += cmds.listConnections( node + '.' + attr, s=1, d=0 )
    
    cmds.select( cons )
    return cons
    
    
    
    
    


