import maya.cmds as cmds
import sg.dag
import sg



def putNull( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.dag.putObject( sels, 'null' )
    


def putJoint( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.dag.putObject( sels, 'joint' )



def putLocator( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.dag.putObject( sels, 'locator' )



def makeParent( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    sg.dag.makeParent( sels )



def parentSelectedOlder( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for i in range( len( sels ) -1 ):
        sels[i] = cmds.parent( sels[i], sels[i+1] )[0]




def putChild( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        putTarget = sg.dag.putObject( sel, 'transform' )
        putTarget = cmds.parent( putTarget, sel )
        
        selName = sel.split('|')[-1]
        childName = ''
        if selName[-1] == '_':
            childName = sel.split('|')[-1] + 'child'
        else:
            childName = sel.split('|')[-1] + '_child'
            
        putTarget = cmds.rename( putTarget, childName )
        


def putChildJoint( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        putTarget = sg.dag.putObject( sel, 'joint' )
        putTarget = cmds.parent( putTarget, sel )
        
        selName = sel.split('|')[-1]
        childName = ''
        if selName[-1] == '_':
            childName = sel.split('|')[-1] + 'child'
        else:
            childName = sel.split('|')[-1] + '_child'
            
        putTarget = cmds.rename( putTarget, childName )


def putChildLocator( evt=0 ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        putTarget = sg.dag.putObject( sel, 'locator' )
        putTarget = cmds.parent( putTarget, sel )
        
        selName = sel.split('|')[-1]
        childName = ''
        if selName[-1] == '_':
            childName = sel.split('|')[-1] + 'child'
        else:
            childName = sel.split('|')[-1] + '_child'
            
        putTarget = cmds.rename( putTarget, childName )



def renameOtherSide( evt=0 ):
    
    sels = sg.listNodes( sl=1 )
    
    if sels[0].name().find( '_L_' ) != -1:
        sels[1].rename( sels[0].localName().replace( '_L_', '_R_' ) )
    elif sels[0].name().find( '_R_' ) != -1:
        sels[1].rename( sels[0].localName().replace( '_R_', '_L_' ) )



def renameParent( evt=0 ):
    
    sels = sg.listNodes( sl=1 )
    for sel in sels:
        selP = sel.parent()
        if not selP: continue
        selP.rename( 'P' + sel.localName() )
    
        
    
    
