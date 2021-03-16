# Serial COM demo 1

## Scope
This program is written in python 3.9.2. I use PyCharm + pyserial + Qt Designer (PyQt5). 
GUI screenshot:
![image](https://user-images.githubusercontent.com/14843517/111241251-bf0b2a00-85ca-11eb-9217-85bbb1f59d26.png)


## File Structure
- `UI_SerialComDemo1.ui` is the UI file created by Qt designer.
- `UI_SerialComDemo1.py` is the python file convert from .ui file by PyUIC.
- `Main_SerialComDemo1.py` is the main program.


## Future Features
- I will try to detect USB-to-serial adapter attach/dettach event in Windows 10 OS. So it will auto update the available COM port list.
  - one possible solution is here, https://stackoverflow.com/questions/59868022/detecting-usb-device-insertion-on-windows-10-using-python
  - other one I can think of is using a separate thread to polling the list change. (probably no recommended)
