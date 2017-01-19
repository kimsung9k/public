import maya.cmds as cmds
import sg.MainFunctions
import sg.MainFunctions.connect
import sg


def create( parent ):
    
    sels = sg.listNodes( sl=1 )
    
    getMenu = False
    getMenu_getAngle = False
    optimizeMenu = False
    
    
    for sel in sels:
        srcCon = sg.listConnections( sel, s=1, d=0 )
        dstCon = sg.listConnections( sel, s=0, d=1 )
        if srcCon and dstCon:
            optimizeMenu = True
        
        if sel.nodeType() == "decomposeMatrix":
            getMenu = True
            getMenu_getAngle = True
    
    if optimizeMenu: cmds.menuItem( l='Optimize Connection', rp='NE', p=parent, c= sg.MainFunctions.connect.optimizeConnection )
    if getMenu: cmds.menuItem( l="Get", rp='N', p=parent, sm=1 )
    if getMenu_getAngle: cmds.menuItem( l="Get Angle", rp='N', c=sg.MainFunctions.connect.getAngle )
    
    cmds.menuItem( l='replace', rp='S', p=parent, c= sg.MainFunctions.replaceConnection )