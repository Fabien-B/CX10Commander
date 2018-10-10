from PyQt5 import QtCore, QtWidgets, QtGui
from collections import namedtuple
import serial
from ui.commander_ui import Ui_MainWindow
from serial import Serial
import traceback

TAKEOFF_COMMAND = ":TAKEOFF\n"
IDLE_COMMAND = ":IDLE\n"
LAND_COMMAND = ":LAND\n"
START_COMMAND = ":START\n"
DISTANCE_THRESHOLD = ":DIST {}\n"
LIMIT = ":LIMIT {}\n"

class CX10RemoteCommander(Ui_MainWindow):
  
  def __init__(self, parent=None):
    Ui_MainWindow.__init__(self)

  def built(self, port, baudrate=115200):
    self.takeoff_button.clicked.connect(lambda : self.send_command(TAKEOFF_COMMAND))
    self.idle_button.clicked.connect(lambda : self.send_command(IDLE_COMMAND))
    self.land_button.clicked.connect(lambda : self.send_command(LAND_COMMAND))
    self.start_button.clicked.connect(lambda : self.send_command(START_COMMAND))
    self.distance_slider.valueChanged.connect(lambda x: self.send_command(DISTANCE_THRESHOLD.format(x)))
    self.limit_slider.valueChanged.connect(lambda x: self.send_command(LIMIT.format(x)))
    self.mire_display.mode_label = self.mode_label
    self.serial_monitor = SerialMonitor(port, baudrate, self.mire_display)
    self.serial_monitor.start()

  def closing(self):
    self.serial_monitor.running = False
    self.serial_monitor.wait()
    if self.serial_monitor.ser is not None:
      self.serial_monitor.ser.close()
  
  def send_command(self, command):
    self.serial_monitor.command = command
    print(command)
 

class SerialMonitor(QtCore.QThread):
  def __init__(self, port, baudrate, mire_display):
    QtCore.QThread.__init__(self)
    self.ser = Serial(port, baudrate, timeout=0.1)
    self.running = False
    self.mire_display = mire_display
    self.command = ""
  
  def run(self):
    self.running = True
    print("thread started")
    while self.running:
      if self.command != "":
        self.ser.write(self.command.encode())
        self.command = ""
      line = self.ser.readline().strip().decode()
      if line == '' or line[0] != ':':
        continue
      data = line[1:].split(',')
      try:
        drone_info = (int(data[0]), int(data[1]), int(data[2]), int(data[3]))
        self.mire_display.set_drone_info(drone_info)
      except IndexError:
        pass
    
