"""
Brody Soedel
Runs a ksp app that calculates various statistics
"""

import sys
import main_menu
from PyQt5 import QtWidgets


def window():
    app = QtWidgets.QApplication([])
    menu = main_menu.Ui()
    menu.show()
    sys.exit(app.exec_())


def main():
    window()


if __name__ == "__main__":
    main()
