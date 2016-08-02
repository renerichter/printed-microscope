position = [0,0,0]

def MotorMove(steps,direction):

    if direction == 0:
        position[0] = position[0] + steps

    if direction == 1:
        position[1] = position[1] + steps

    if direction == 2:
        position[2] = position[2] + steps

    print (position)

def Prompt_MotorMove():

    user_direction = int(input("Please enter the desired direction (0 ===> x,1 ===> y,2 ===> z):"))
    user_steps = int(input("Please enter the desired number of steps (integer valued):"))

    MotorMove(user_steps,user_direction)


#     def initUI(self):
#
#         # lcd = QLCDNumber(self)
#         # sld = QSlider(Qt.Horizontal, self)
#
#         vbox = QVBoxLayout()
#         # vbox.addWidget(lcd)
#         # vbox.addWidget(sld)
#
#         self.setLayout(vbox)
#         # sld.valueChanged.connect(lcd.display)
#
#         okButton = QPushButton("OK")
#         cancelButton = QPushButton("Cancel")
#
#         hbox = QHBoxLayout()
#         hbox.addStretch(1)
#         hbox.addWidget(okButton)
#         hbox.addWidget(cancelButton)
#
#         vbox = QVBoxLayout()
#         vbox.addStretch(1)
#         vbox.addLayout(hbox)
#
#         # self.setLayout(vbox)

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QPushButton, QLCDNumber, QSlider, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication, QDesktopWidget,
                             QLineEdit, QInputDialog)

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # okButton = QPushButton("OK")
        # cancelButton = QPushButton("Cancel")

        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(okButton)
        # hbox.addWidget(cancelButton)

        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        #
        # self.setLayout(vbox)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.resize(800,800)
        self.center()
        self.setWindowTitle('3D Microscope')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.le.setText(str(text))

    """
    This part defines the WASD control method for moving
    the microscope stage in the xy plane, using Q and E
    to move in the z direction, as well as some
    other keyboard shortcuts for the application

    W = Up      ++ y
    S = Down    -- y
    A = Left    -- x
    D = Right   ++ x

    Q = Z Up    ++ z
    E = Z Down  -- z

    F1 = Help Menu
    Escape = Close Window

    """
    def keyPressEvent(self, eventQKeyEvent):
        key = eventQKeyEvent.key()

        if key == Qt.Key_F1:
            print ('Help')
        elif key == Qt.Key_Escape:
            self.close()

        elif key == Qt.Key_A:
            MotorMove(-1,0)
        elif key == Qt.Key_W:
            MotorMove(1, 1)
        elif key == Qt.Key_D:
            MotorMove(1, 0)
        elif key == Qt.Key_S:
            MotorMove(-1, 1)
        elif key == Qt.Key_Q:
            MotorMove(1,2)
        elif key == Qt.Key_E:
            MotorMove(-1,2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())