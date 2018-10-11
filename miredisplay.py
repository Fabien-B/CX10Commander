from typing import Tuple
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt

W = 968
H = 608
DRONE_SIZE = 10

class MireDisplay(QtWidgets.QWidget):
  def __init__(self, parent=None):
    QtWidgets.QWidget.__init__(self)
    #self.drone_info = (50,70,20, 0)
    self.drone_info = (0,0,42, 0)
    self.mode_label = None
    
  
  def paintEvent(self, event):
    mode = "MANU" if self.drone_info[3] == 0 else "AUTO"
    self.mode_label.setText(mode)
    qp = QPainter()
    qp.begin(self)
    
    self.draw_mire(qp, event)
    self.draw_drone(qp, event)
    self.draw_distance(qp, event)
    
    qp.end()
  
  def draw_mire(self, qp, event):
    qp.drawLine(0, H/2, W, H/2)
    qp.drawLine(W/2, 0, W/2, H)
  
  def draw_drone(self, qp, event):
    qp.setPen(QColor(168, 34, 3))
    qp.setBrush(QColor(168, 34, 3))
    x, y, d, status = self.drone_info
    xd = (x + W - DRONE_SIZE)/2.
    yd = (-y + H - DRONE_SIZE)/2.
    #print("pos",xd,yd)
    qp.drawRect(int(xd), int(yd), DRONE_SIZE, DRONE_SIZE)
    
  def draw_distance(self, qp, event):
    qp.setPen(Qt.black)
    qp.drawText(850, 40, "Dist: {:.2f}".format(self.drone_info[2]))
  
  def set_drone_info(self, info :Tuple):
    self.drone_info = info
    self.update()

