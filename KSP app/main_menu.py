"""
Brody Soedel
main menu etc
"""

from PyQt5 import QtWidgets as qw, uic
from PyQt5 import QtGui
from PyQt5 import QtCore


class Ui(qw.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ksp.ui', self)
        self.show()