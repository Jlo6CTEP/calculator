import ctypes
import os
import sys
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, \
    QGridLayout, QHBoxLayout, QVBoxLayout, QSizePolicy, QShortcut, QLabel


class Window(QWidget):

    def make_resizeable(self, widget):
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return widget

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        if os.name == 'nt':
            my_app_id = 'InnoUI.DE_Solver.smart_solver.101'  # arbitrary string
            ctypes.windll.shell32. \
                SetCurrentProcessExplicitAppUserModelID(my_app_id)

        # widgets and layouts for main window

        self.equation = self.make_resizeable(QLineEdit())
        self.result = self.make_resizeable(QLineEdit('Result'))
        self.result.setReadOnly(True)
        self.submit = self.make_resizeable(QPushButton("Calculate"))
        self.delete = self.make_resizeable(QPushButton("Delete"))
        self.keys = [self.make_resizeable(QPushButton(str(x)))
                     for x in range(10)]

        self.plus = self.make_resizeable(QPushButton("+"))
        self.minus = self.make_resizeable(QPushButton("-"))
        self.divide = self.make_resizeable(QPushButton("/"))
        self.multiply = self.make_resizeable(QPushButton("*"))

        self.create_main_window()

    def create_main_window(self):
        self.setWindowIcon(QtGui.QIcon('DE.png'))
        self.setWindowTitle('Calculator')
        equation_bar = QVBoxLayout()
        equation_bar.addWidget(self.equation)
        equation_bar.addWidget(self.result)

        keypad = QGridLayout()

        for x in enumerate(self.keys[1:]):
            keypad.addWidget(x[1], x[0] // 3, x[0] % 3)
        keypad.addWidget(self.keys[0], 3, 1)
        keypad.addWidget(self.submit, 3, 2)
        keypad.addWidget(self.delete, 3, 0)
        keypad.addWidget(self.plus, 0, 3)
        keypad.addWidget(self.minus, 1, 3)
        keypad.addWidget(self.divide, 2, 3)
        keypad.addWidget(self.multiply, 3, 3)

        main_layout = QVBoxLayout()
        main_layout.addLayout(equation_bar)
        main_layout.addLayout(keypad)

        self.setLayout(main_layout)

        for x in zip(['+', '-', '/', '*'],
                     [self.plus, self.minus, self.divide, self.multiply]):

            click = QShortcut(QKeySequence(x[0]), self)
            click.activated.connect(partial(lambda x: x.animateClick(), x[1]))
            x[1].clicked.connect(partial(lambda x:
                self.equation.setText(self.equation.text() + x), x[0]))

        delete_click = QShortcut(QKeySequence('Backspace'), self)
        delete_click.activated.connect(self.delete.animateClick)
        self.delete.clicked.connect(lambda:
            self.equation.setText(self.equation.text()[:-1]))

        enter_click = QShortcut(QKeySequence('Return'), self)
        enter_click.activated.connect(self.submit.animateClick)
        self.submit.clicked.connect(self.evaluate)

        for x in range(10):
            click = QShortcut(QKeySequence(f'{str(x)}'), self)
            click.activated.connect(partial(lambda x:
                self.keys[x].animateClick(), x))

            self.keys[x].clicked.connect(
                partial(lambda x: self.equation.setText(
                    self.equation.text() + str(x)), x))
        self.show()

    def evaluate(self):
        try:
            self.result.setText(str(eval(self.equation.text())))
        except Exception:
            self.result.setText('Incorrect input')

    def resizeEvent(self, QResizeEvent):
        pass


app = QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
