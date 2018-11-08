from PyQt5 import QtCore, QtWidgets, QtGui
from collections import namedtuple
import serial
from ui.commander_ui import Ui_MainWindow
from serial import Serial
import traceback
from time import sleep

TAKEOFF_COMMAND = ":TAKEOFF\n"
IDLE_COMMAND = ":IDLE\n"
LAND_COMMAND = ":LAND\n"
DISTANCE_COMMAND = ":DIST {}\n"
START_COMMAND = ":START\n"
START_LAND_COMMAND = ":START_LAND\n"
LIMIT_COMMAND = ":LIMIT {}\n"
START2_COMMAND = ":START2\n"
START_LAND2_COMMAND = ":START_LAND2\n"
LIMIT2_COMMAND = ":LIMIT2 {}\n"
RESET_COMMAND = ":RESET\n"

class CX10RemoteCommander(Ui_MainWindow):
  
  def __init__(self, parent=None):
    Ui_MainWindow.__init__(self)

  def built(self, port, baudrate=115200):
    # mode
    self.mire_display.mode_label = self.mode_label
    # top part
    self.takeoff_button.clicked.connect(lambda : self.send_command(TAKEOFF_COMMAND))
    self.idle_button.clicked.connect(lambda : self.send_command(IDLE_COMMAND))
    self.land_button.clicked.connect(lambda : self.send_command(LAND_COMMAND))
    self.distance_slider.valueChanged.connect(lambda x: self.distance_label.setText(str(float(x)/10.)))
    self.distance_slider.valueChanged.connect(lambda x: self.send_command(DISTANCE_COMMAND.format(float(x)/10.)))
    # mission 1
    self.start_button.clicked.connect(lambda : self.send_command(START_COMMAND))
    self.start_land_button.clicked.connect(lambda : self.send_command(START_LAND_COMMAND))
    self.limit_slider.valueChanged.connect(lambda x: self.limit_label.setText(str(float(x)/10.)))
    self.limit_slider.valueChanged.connect(lambda x: self.send_command(LIMIT_COMMAND.format(float(x)/10.)))
    # mission 2
    self.start2_button.clicked.connect(lambda : self.send_command(START2_COMMAND))
    self.start_land2_button.clicked.connect(lambda : self.send_command(START_LAND2_COMMAND))
    self.limit2_slider.valueChanged.connect(lambda x: self.limit2_label.setText(str(float(x)/10.)))
    self.limit2_slider.valueChanged.connect(lambda x: self.send_command(LIMIT2_COMMAND.format(float(x)/10.)))
    # reset
    self.reset_mission.clicked.connect(lambda : self.send_command(RESET_COMMAND))
    # serial
    self.serial_monitor = SerialMonitor(port, baudrate, self)
    if self.serial_monitor.ser is None:
        self.link_status.setText('Failed to open serial')
    else:
        self.link_status.setText('Serial opened')
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
  def __init__(self, port, baudrate, window):
    QtCore.QThread.__init__(self)
    try:
        self.ser = Serial(port, baudrate, timeout=0.1)
    except:
        print("serial port not openned")
        self.ser = None
    self.running = False
    self.window = window
    self.command = ""
  
  def run(self):
    self.running = True
    print("thread started")
    while self.running:
      if self.ser is None:
        sleep(1)
        continue
      if self.command != "":
        self.ser.write(self.command.encode())
        self.command = ""
      line = self.ser.readline().strip()
      try:
          dec = line.decode()
      except Exception as e:
          print("decode error '{}'".format(str(e)))
          dec = ''
      if dec == '':
          self.window.link_status.setText('Serial opened: not receiving data')
          continue
      if dec[0] != ':':
          self.window.link_status.setText('Serial opened: receiving wrong data')
          continue
      self.window.link_status.setText('Serial opened: receiving new data')
      data = dec[1:].split(',')
      try:
          if len(data) == 4:
              drone_info = (float(data[0]), float(data[1]), float(data[2]), int(data[3]))
              self.window.mire_display.set_drone_info(drone_info)
          elif len(data) == 3:
              self.window.distance_slider.setValue(int(float(data[0])*10.))
              self.window.limit_slider.setValue(int(float(data[1])*10.))
              self.window.limit2_slider.setValue(int(float(data[2])*10.))
      except IndexError:
          print("index error")
          pass

