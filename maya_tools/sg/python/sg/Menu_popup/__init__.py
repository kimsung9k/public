import maya.cmds as cmds
import sg.get
import sg.file
import menu_dg
import menu_dag
import menu_default
import menu_channelConnect
import os

'''
class Popup_Global:
    
    name = 'SGMTool_popupMenu'
    infoPath = cmds.about(pd=True) + "/sg_toolInfo/popupMode.txt"
    
    if not os.path.exists( infoPath ):
        sg.file.makeFile( infoPath )
    
    popupMode = "default"
    
    @staticmethod
    def saveInfo():
        pass
    
    @staticmethod
    def loadInfo():
        pass



def create():
    
    if cmds.popupMenu( Popup_Global.name, ex=1 ):
        cmds.deleteUI( Popup_Global.name )
    cmds.popupMenu( Popup_Global.name, alt=1, ctl=1, mm=1, p="viewPanes", pmc=show )



def show(*args):
    
    cmds.popupMenu( Popup_Global.name, e=1, deleteAllItems=1 )
    menu_default.create( Popup_Global.name )

    sma = cmds.channelBox( 'mainChannelBox', q=1, sma=1 )
    sha = cmds.channelBox( 'mainChannelBox', q=1, sha=1 )
    
    sels = cmds.ls( sl=1 )
    dagNodes = []
    dgNodes = []
    
    for sel in sels:
        if cmds.nodeType( sel ) in ['transform', 'joint', 'mesh']:
            dagNodes.append( sel )
        else:
            dgNodes.append( sel )
    
    if sma or sha:
        menu_channelConnect.create( Popup_Global.name )
    elif dagNodes:
        menu_dag.create( Popup_Global.name )
    elif dgNodes:
        menu_dg.create( Popup_Global.name )
    '''
    