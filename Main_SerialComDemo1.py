import sys
import threading
# serial communication related imports
import serial
import serial.tools.list_ports

# import UI created by PyQt5 designer
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from UI_SerialComDemo1 import *

#serialRecvData = ''
#serialPortObj = None

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

        # test to list out all available serial ports
        # add available serial ports to combobox
        # serial_port_list = serial.tools.list_ports.comports()
        for i in serial.tools.list_ports.comports():
            # print(i.name)
            str = i.name
            self.comboBox_SerialPort.addItem(str)

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

        if self.pushButton_SerialPort.text() == 'Connect':
            self.pushButton_SerialPort.setText('Disconnect')

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

        elif self.pushButton_SerialPort.text() == 'Disconnect':
            self.threadStopEvent.set()
            self.serialPortObj.close()
            self.comboBox_SerialPort.setEnabled(True)
            self.groupBox_TRX.setDisabled(True)
            self.pushButton_SerialPort.setText('Connect')

    def readSerialData(self, threadStopEvent):                            # passing threading.Event() type into func
        while 1:
            self.serialRecvData = self.serialPortObj.readline().decode("utf-8")
            self.textBrowser_TRX.insertPlainText(self.serialRecvData)
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
    # myWindow.pushButton_TRX.setText('TEST')
    myWindow.show()
    sys.exit(app.exec_())