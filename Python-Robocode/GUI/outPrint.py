# -*- coding: utf-8 -*-

"""
Module implementing outPrint.
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QTextCursor

from Ui_outPrint import Ui_Form

class outPrint(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QWidget.__init__(self, parent)
        self.setupUi(self)

        
    def add(self, msg):
        if self.isTextEmpty:
            self.textEdit.setPlainText(msg)
            self.isTextEmtpy = False
        else:
            self.textCursor.movePosition(QTextCursor.MoveOperation.End)
            self.textCursor.insertText("\n" + msg)
