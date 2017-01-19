import maya.cmds as cmds


def lockAttributeFromChannelBox():
    
    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    if sma or sha:
        attrs = []
        if sma: attrs += sma
        if sha: attrs += sha
        sels = cmds.ls( sl=1 )
        for sel in sels:
            for attr in attrs:
                if not cmds.attributeQuery( attr, node= sel, ex=1 ): continue
                cmds.setAttr( sel + '.' + attr, lock=1 )



def unlockAttributeFromChannelBox():
    
    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    if sma or sha:
        attrs = []
        if sma: attrs += sma
        if sha: attrs += sha
        sels = cmds.ls( sl=1 )
        for sel in sels:
            for attr in attrs:
                if not cmds.attributeQuery( attr, node= sel, ex=1 ): continue
                cmds.setAttr( sel + '.' + attr, lock=0 )



def hideAttributeFromChannelBox():
    
    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    if sma or sha:
        attrs = []
        if sma: attrs += sma
        if sha: attrs += sha
        sels = cmds.ls( sl=1 )
        for sel in sels:
            for attr in attrs:
                if not cmds.attributeQuery( attr, node= sel, ex=1 ): continue
                cmds.setAttr( sel + '.' + attr, k=0, cb=0 )


