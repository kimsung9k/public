from PySide import QtGui, QtCore


class SGMouse:
    
    kConditionReleased = 0
    kConditionPressed = 1
    
    kEventDefault = 0
    kEventPress = 1
    kEventRelease = 2
    kEventMove = 3
    kEventDbClick = 4
    
    def __init__(self, mouseButton ):
        self.button = mouseButton
        self.condition = SGMouse.kConditionReleased
        self.event     = SGMouse.kDefault

    def __eq__(self, other ):
        return self.button == other.button
    
    def translateEvent(self, evt ):
        
        self.event     = SGMouse.kDefault
        
        if evt.type() == QtGui.QMouseEvent.MouseButtonPress:
            self.event = SGMouse.kEventMove
            self.condition = SGMouse.kConditionPressed
        elif evt.type() == QtGui.QMouseEvent.MouseButtonRelease:
            self.event = SGMouse.kEventRelease
            self.condition = SGMouse.kConditionReleased
        elif evt.type() == QtGui.QMouseEvent.MouseButtonDblClick:
            self.event = SGMouse.kEventDbClick


class Buttons:
    
    noButton = SGMouse( QtCore.Qt.NoButton )
    leftButton = SGMouse( QtCore.Qt.LeftButton )
    rightButton = SGMouse( QtCore.Qt.RightButton )
    middleButton = SGMouse( QtCore.Qt.MiddleButton )