#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import cx10remotecommander
import argparse

def main(port,baud):
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = QtWidgets.QMainWindow()
  commander = cx10remotecommander.CX10RemoteCommander()
  app.aboutToQuit.connect(commander.closing)
  commander.setupUi(MainWindow)
  commander.built(port,baud)
  MainWindow.show()
  sys.exit(app.exec_())


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Interface for CX10 at IMAV2018")
  parser.add_argument('port', help="serial port")
  parser.add_argument('baud', help="serial baudrate")
  args = parser.parse_args()
  main(args.port,args.baud)
