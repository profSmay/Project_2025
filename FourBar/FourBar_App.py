#region imports
from FourBar_GUI import Ui_Form
from FourBarLinkage_MVC import FourBarLinkage_Controller
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw
import math
import sys
import numpy as np
import scipy as sp
from scipy import optimize
from copy import deepcopy as dc
#endregion

#region class definitions
class MainWindow(Ui_Form, qtw.QWidget):
    def __init__(self):
        """
        This program illustrates the use of the graphics view framework.  The QGraphicsView widget is created in
        designer.  The QGraphicsView displays a QGraphicsScene.  A QGraphicsScene contains QGraphicsItem objects.
        """
        super().__init__()
        self.setupUi(self)
        #region UserInterface stuff here

        #create a four bar linkage controller object and pass widgets for interaction
        widgets = [self.gv_Main, self.nud_InputAngle, self.lbl_OutputAngle_Val, self.nud_Link1Length, self.nud_Link3Length, self.spnd_Zoom]
        self.FBL_C=FourBarLinkage_Controller(widgets)

        #set up graphics view, add a scene and build pens and brushes
        self.FBL_C.setupGraphics()

        #turning on mouse tracking on the graphics view
        self.gv_Main.setMouseTracking(True)
        #turning on mouse tracking for the MainWindow widget
        self.setMouseTracking(True)

        #draws a scene
        self.FBL_C.buildScene()
        self.prevAlpha = self.FBL_C.FBL_M.InputLink.angle
        self.prevBeta = self.FBL_C.FBL_M.OutputLink.angle
        self.angle1=math.pi
        self.angle2=math.pi
        self.lbl_OutputAngle_Val.setText("{:0.3f}".format(self.FBL_C.FBL_M.OutputLink.AngleDeg()))
        self.nud_Link1Length.setValue(self.FBL_C.FBL_M.InputLink.length)
        self.nud_Link3Length.setValue(self.FBL_C.FBL_M.OutputLink.length)

        #signals/slots
        self.spnd_Zoom.valueChanged.connect(self.setZoom)
        self.nud_Link1Length.valueChanged.connect(self.setInputLinkLength)
        self.nud_Link3Length.valueChanged.connect(self.setOutputLinkLength)
        self.FBL_C.FBL_V.scene.installEventFilter(self)
        self.mouseDown = False
        self.show()

    def setInputLinkLength(self):
        self.FBL_C.setInputLinkLength()

    def setOutputLinkLength(self):
        self.FBL_C.setOutputLinkLength()

    def mouseMoveEvent(self, a0: qtg.QMouseEvent):
        w=app.widgetAt(a0.globalPos())
        if w is None:
            name='none'
        else:
            name=w.objectName()
        self.setWindowTitle(str(a0.x())+','+ str(a0.y())+name)

    def eventFilter(self, obj, event):
        # I set up an event filter to track mouse position and illustrate difference between scene and screen coords.
        if obj == self.FBL_C.FBL_V.scene:
            et=event.type()
            if event.type() == qtc.QEvent.GraphicsSceneMouseMove:
                w=app.topLevelAt(event.screenPos())
                screenPos=event.screenPos()
                scenePos=event.scenePos()
                strScreen="screen x = {}, screen y = {}".format(screenPos.x(), screenPos.y())
                strScene=":  scene x = {}, scene y = {}".format(scenePos.x(), scenePos.y())
                self.setWindowTitle(strScreen+strScene)
                if self.mouseDown:
                    self.FBL_C.moveLinkage(scenePos)

            if event.type() == qtc.QEvent.GraphicsSceneWheel:
                if event.delta()>0:
                    self.spnd_Zoom.stepUp()
                else:
                    self.spnd_Zoom.stepDown()
            if event.type() ==qtc.QEvent.GraphicsSceneMousePress:
                if event.button() == qtc.Qt.LeftButton:
                    self.mouseDown = True
            if event.type() == qtc.QEvent.GraphicsSceneMouseRelease:
                self.mouseDown = False
        # pass the event along to the parent widget if there is one.
        return super(MainWindow, self).eventFilter(obj, event)

    def setZoom(self):
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())
#endregion

#region function calls
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.setWindowTitle('Four Bar Linkage')
    sys.exit(app.exec())
#endregion