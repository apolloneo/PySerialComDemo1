import sys
import threading
import time
# serial communication related imports
import serial
import serial.tools.list_ports

# import UI created by PyQt5 designer
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from UI_SerialComDemo1 import *


# Inherited to the main window class of the interface file
class MyMainWindow(QMainWindow, Ui_myMainWindow):
    threadStopEvent = threading.Event()                             # thread stop detection
    serialRecvData = ''                                             # received serial data string
    serialPortObj = serial.Serial()                                 # serial port init
    serialPortObj.baudrate = 9600                                   # serial port init baudrate
    serialPortObj.bytesize = serial.EIGHTBITS                       # serial port init data bits (default = 8)
    serialPortObj.parity = serial.PARITY_NONE                       # serial port init stop bits (default = N)
    serialPortObj.stopbits = serial.STOPBITS_ONE                    # serial port init parity bit (default = 1)
    serialPortObj.timeout = 0.5                                     # serial port init timeout (default 0.5 sec or 500 ms)

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # Timeout line input int only
        self.intOnly = QtGui.QIntValidator(1, 99999, self.lineEdit_Timeout)
        self.lineEdit_Timeout.setValidator(self.intOnly)

        # test to list out all available serial ports
        # add available serial ports to combobox
        # serial_port_list = serial.tools.list_ports.comports()
        for i in serial.tools.list_ports.comports():
            # print(i.name)
            str = i.name
            self.comboBox_SerialPort.addItem(str)

    # override the closeEvent, kill the thread, close COM port, then quit program
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.threadStopEvent.set()
        if self.serialPortObj.is_open:
            self.serialPortObj.close()

    def updateSerialParam(self):
        if self.comboBox_Baudrate.currentIndex() == 0:
            self.serialPortObj.baudrate = 600
        elif self.comboBox_Baudrate.currentIndex() == 1:
            self.serialPortObj.baudrate = 1200
        elif self.comboBox_Baudrate.currentIndex() == 2:
            self.serialPortObj.baudrate = 1800
        elif self.comboBox_Baudrate.currentIndex() == 3:
            self.serialPortObj.baudrate = 2400
        elif self.comboBox_Baudrate.currentIndex() == 4:
            self.serialPortObj.baudrate = 4800
        elif self.comboBox_Baudrate.currentIndex() == 5:
            self.serialPortObj.baudrate = 9600
        elif self.comboBox_Baudrate.currentIndex() == 6:
            self.serialPortObj.baudrate = 19200
        elif self.comboBox_Baudrate.currentIndex() == 7:
            self.serialPortObj.baudrate = 38400
        elif self.comboBox_Baudrate.currentIndex() == 8:
            self.serialPortObj.baudrate = 57600
        elif self.comboBox_Baudrate.currentIndex() == 9:
            self.serialPortObj.baudrate = 115200
        elif self.comboBox_Baudrate.currentIndex() == 10:
            self.serialPortObj.baudrate = 230400
        elif self.comboBox_Baudrate.currentIndex() == 11:
            self.serialPortObj.baudrate = 460800
        elif self.comboBox_Baudrate.currentIndex() == 12:
            self.serialPortObj.baudrate = 500000
        elif self.comboBox_Baudrate.currentIndex() == 13:
            self.serialPortObj.baudrate = 576000
        elif self.comboBox_Baudrate.currentIndex() == 14:
            self.serialPortObj.baudrate = 921600
        else:
            self.serialPortObj.baudrate = 9600

        if self.comboBox_Databits.currentIndex() == 0:
            self.serialPortObj.bytesize = serial.FIVEBITS
        elif self.comboBox_Databits.currentIndex() == 1:
            self.serialPortObj.bytesize = serial.SIXBITS
        elif self.comboBox_Databits.currentIndex() == 2:
            self.serialPortObj.bytesize = serial.SEVENBITS
        elif self.comboBox_Databits.currentIndex() == 3:
            self.serialPortObj.bytesize = serial.EIGHTBITS
        else:
            self.serialPortObj.bytesize = serial.EIGHTBITS

        if self.comboBox_Parity.currentIndex() == 0:
            self.serialPortObj.parity = serial.PARITY_NONE
        elif self.comboBox_Parity.currentIndex() == 1:
            self.serialPortObj.parity = serial.PARITY_ODD
        elif self.comboBox_Parity.currentIndex() == 2:
            self.serialPortObj.parity = serial.PARITY_EVEN
        elif self.comboBox_Parity.currentIndex() == 3:
            self.serialPortObj.parity = serial.PARITY_MARK
        elif self.comboBox_Parity.currentIndex() == 4:
            self.serialPortObj.parity = serial.PARITY_SPACE
        else:
            self.serialPortObj.parity = serial.PARITY_NONE

        if self.comboBox_Stopbits.currentIndex() == 0:
            self.serialPortObj.stopbits = serial.STOPBITS_ONE
        elif self.comboBox_Stopbits.currentIndex() == 1:
            self.serialPortObj.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        elif self.comboBox_Stopbits.currentIndex() == 2:
            self.serialPortObj.stopbits = serial.STOPBITS_TWO
        else:
            self.serialPortObj.stopbits = serial.STOPBITS_ONE

        timeout = int(self.lineEdit_Timeout.text()) / 1000
        self.serialPortObj.timeout = timeout

    def msgComPortConnectionErrorUI(self):
        # simple message box pops up if com port open failed
        QMessageBox.critical(self, "COM Port Connection Error", "COM Port Connection Failed.", QMessageBox.Ok)

    def btnSendTxtClicked(self):
        # print('send button clicked.')
        str = self.lineEdit_TRX.text() + '\r\n'
        if self.serialPortObj.is_open:
            self.serialPortObj.write(str.encode())
        else:
            self.msgComPortConnectionErrorUI()
        self.textBrowser_TRX.append(str)

    def btnConnectClicked(self):

        if self.pushButton_SerialConnect.text() == 'Connect':
            self.pushButton_SerialConnect.setText('Disconnect')

            # reset thread event back to initial state (default is false)0
            self.threadStopEvent.clear()

            # get the port number from combobox
            self.serialPortObj.port = self.comboBox_SerialPort.currentText()

            try:
                self.serialPortObj.open()
            except serial.SerialException:
                self.msgComPortConnectionErrorUI()
                sys.exit('Error: Open COM port')

            t1 = threading.Thread(target=self.readSerialData, args=(self.threadStopEvent,))
            t1.start()

            self.comboBox_SerialPort.setDisabled(True)
            self.groupBox_TRX.setEnabled(True)

        elif self.pushButton_SerialConnect.text() == 'Disconnect':
            self.threadStopEvent.set()
            self.serialPortObj.close()
            self.comboBox_SerialPort.setEnabled(True)
            self.groupBox_TRX.setDisabled(True)
            self.pushButton_SerialConnect.setText('Connect')

    def readSerialData(self, threadStopEvent):                            # passing threading.Event() type into func
        while 1:
            self.serialRecvData = self.serialPortObj.readline().decode("ascii")
            self.textBrowser_TRX.insertPlainText(self.serialRecvData)
            # Text Browser auto scroll
            self.textBrowser_TRX.moveCursor(QtGui.QTextCursor.End)
            if self.threadStopEvent.is_set():                             # always check threading event for proper quit
                break
        # sio = io.TextIOWrapper(io.BufferedRWPair(self.serialPortObj, self.serialPortObj))
        # while 1:
        #     self.serialRecvData = ''
        #     try:
        #         #time.sleep(0.5)
        #         self.serialRecvData = sio.readline()
        #         if len(self.serialRecvData):
        #             self.textBrowser_TRX.append(self.serialRecvData)
        #     except serial.SerialException as e:
        #         print('Device error: {}'.format(e))
        #         break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MyMainWindow()
    myWindow.show()
    sys.exit(app.exec_())