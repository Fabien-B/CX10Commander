#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import cx10commander
import argparse

def main():
  app = QtWidgets.QApplication(sys.argv)
  MainWindow = QtWidgets.QMainWindow()
  commander = cx10commander.CX10Commander()
  app.aboutToQuit.connect(commander.closing)
  commander.setupUi(MainWindow)
  commander.built()
  MainWindow.show()
  sys.exit(app.exec_())


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Interface for CX10 at IMAV2018")
  #parser.add_argument('config_file', help="JSON configuration file")
  #args = parser.parse_args()
  #main(args.config_file)
  main()
