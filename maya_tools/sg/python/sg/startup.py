import maya.cmds as cmds


def pluginDebugMode():
    
    from sga import Tool_pluginReload
    Tool_pluginReload.UI().show()
    
    cmds.ScriptEditor()