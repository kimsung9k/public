import maya.cmds as cmds

def getCurrentPanel():
    return cmds.getPanel( wf=1 )