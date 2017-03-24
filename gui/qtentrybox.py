#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class EntryBox(QLineEdit):

    def __init__(self, type_=None):
        super(EntryBox, self).__init__()
        self.type_ = type_
        # New style slots
        self.textChanged.connect(self._check)

    def _check(self):
        if not self.type_:
            return
        try:
            _val = self.text()
            _val = self.type_(_val)
            self.setStyleSheet('QLineEdit{background-color:white}')

        except ValueError:
            self.setStyleSheet('QLineEdit{background-color:indianred}')


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        lineedit_standard = QLineEdit()
        lineedit_custom = EntryBox(float)

        layout = QVBoxLayout()
        layout.addWidget(lineedit_standard)
        layout.addWidget(lineedit_custom)
        self.setLayout(layout)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
