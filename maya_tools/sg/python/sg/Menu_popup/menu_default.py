import maya.cmds as cmds
import sg.Tool_imageLoader
import sg.Tool_loadImagePlane
import sg.Tool_pluginReload
import sg.Tool_connectAttr


def create( parent ):
    
    if cmds.ls( sl=1 ): return None
    
    cmds.menuItem( l = "Modeling Menu", rp = "W", sm=1, p=parent )
    cmds.menuItem( l = "UI Image Loader", rp="N", c = sg.Tool_imageLoader.show )
    cmds.menuItem( l = "UI Load Image Plane", rp="NW", c = sg.Tool_loadImagePlane.Window().show )
    
    cmds.menuItem( l='Rigging Menu', rp='N', sm=1, p=parent )
    cmds.menuItem( l="UI Connect Attr", rp="N", c= sg.Tool_connectAttr.show )
    
    cmds.menuItem( l="UI Plugin Debug", c= sg.Tool_pluginReload.UI().show, p=parent )