import maya.cmds as cmds
import maya.OpenMayaUI
from PySide import QtGui, QtCore
import shiboken
import os, sys
import sg.file
import json
from functools import partial





class Window_global:
    
    mayaWin = shiboken.wrapInstance( long( maya.OpenMayaUI.MQtUtil.mainWindow() ), QtGui.QWidget )
    objectName = "sg_Tool_connectAttr"
    title = "SG Tool Connect Attr"
    width = 300
    height = 10
    
    infoPath = cmds.about(pd=True) + "/sg_toolInfo/connectAttr.txt"
    sg.file.makeFile( infoPath )
    
    mainGui = QtGui.QMainWindow()





class UI_labels( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.text_srcAttr = QtGui.QLabel('Source Attr')
        self.text_dstAttr = QtGui.QLabel('Dest Attr')
        
        self.text_srcAttr.setAlignment( QtCore.Qt.AlignCenter )
        self.text_dstAttr.setAlignment( QtCore.Qt.AlignCenter )
        
        self.layout.addWidget( self.text_srcAttr )
        self.layout.addWidget( self.text_dstAttr )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass




class UI_attrlist( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.lineEdit_srcAttr = QtGui.QLineEdit()
        self.lineEdit_dstAttr = QtGui.QLineEdit()
        
        self.layout.addWidget( self.lineEdit_srcAttr )
        self.layout.addWidget( self.lineEdit_dstAttr )

    
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass



class UI_buttons( QtGui.QWidget ):
    
    def __init__(self, *args, **kwargs):
        QtGui.QWidget.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        
        self.layout = QtGui.QHBoxLayout( self )
        self.layout.setContentsMargins( 0,0,0,0 )
        
        self.button_connect = QtGui.QPushButton("Connect")
        self.button_addLine = QtGui.QPushButton("Add Line")
        self.lineEdit_dstAttr = QtGui.QLineEdit()
        self.layout.addWidget( self.button_connect )
        self.layout.addWidget( self.button_addLine )
        
    def eventFilter( self, *args, **kwargs ):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass
    




class Window( QtGui.QMainWindow ):
    
    def __init__(self, *args, **kwargs ):
        QtGui.QMainWindow.__init__( self, *args, **kwargs )
        self.installEventFilter( self )
        self.setWindowFlags(QtCore.Qt.Drawer)
    
        self.layoutWidget = QtGui.QWidget()
        self.setCentralWidget( self.layoutWidget )
        
        self.layout = QtGui.QVBoxLayout( self.layoutWidget )
        self.layout.setContentsMargins( 5,5,5,5 )
        
        self.ui_labels     = UI_labels()
        self.ui_driverAttr = UI_attrlist()
        self.ui_buttons    = UI_buttons()
        self.layout.addWidget( self.ui_labels )
        self.layout.addWidget( self.ui_driverAttr )
        self.layout.addWidget( self.ui_buttons )
        
        
        def addLineCommand():
            
            numItems = self.layout.count()
            attrlist = UI_attrlist()
            self.layout.insertWidget( numItems-1, attrlist )
        
        
        def connectCommand():
            
            sels = cmds.ls( sl=1 )
            numItems = self.layout.count()
            
            for i in range( 1, numItems-1 ):
                targetWidget = self.layout.itemAt( i ).widget()
                
                srcAttr = targetWidget.lineEdit_srcAttr.text()
                dstAttr = targetWidget.lineEdit_dstAttr.text()
                
                print srcAttr, dstAttr
                
                if not srcAttr or not dstAttr: continue
                
                try: 
                    for sel in sels[1:]:
                        cmds.connectAttr( sels[0] + '.' + srcAttr, sel + '.' + dstAttr )
                except: pass
            
        
        self.ui_buttons.button_connect.clicked.connect( connectCommand )
        self.ui_buttons.button_addLine.clicked.connect( addLineCommand )
    
    
    def eventFilter( self, *args, **kwargs):
        event = args[1]
        if event.type() == QtCore.QEvent.LayoutRequest or event.type() == QtCore.QEvent.Move :
            pass





def show( evt=0 ):
    
    if cmds.window( Window_global.objectName, ex=1 ):
        cmds.deleteUI( Window_global.objectName )
    
    Window_global.mainGui = Window(Window_global.mayaWin)
    Window_global.mainGui.setObjectName( Window_global.objectName )
    Window_global.mainGui.resize( Window_global.width, Window_global.height )
    
    Window_global.mainGui.show()
