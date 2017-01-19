import maya.cmds as cmds
import sg.MainFunctions


def create( parent ):
    
    cmds.menuItem( l = "Get Connected AnimCurve", rp = "N", p=parent, c = sg.MainFunctions.getConnectedAnimCurve )
    cmds.menuItem( l = "Connect Node Output To Channel", rp='NE', p=parent, c = sg.MainFunctions.connectNodeOutputToChannel )
    cmds.menuItem( l = "Get Connection from Channel Box", rp= "NW", p=parent, c= sg.MainFunctions.getConnectionFromChannelBox )