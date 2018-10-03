from PyQt5 import QtCore, QtWidgets, QtGui
from collections import namedtuple
import serial
from ui.commander_ui import Ui_MainWindow
import traceback

class CX10Commander(Ui_MainWindow):
  
  def __init__(self, parent=None):
    Ui_MainWindow.__init__(self)

  
  def built(self):
    pass
  
  def closing(self):
    pass

