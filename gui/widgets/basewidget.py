# -*- coding: utf-8 -*-
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class BaseWidget(QWidget):
    """Base class for any main widgets of the interface. This base widget
    specifies common methods to be overrided by enherited widgets.
    """

    def __init__(self, parent=None, **kwargs):
        super(BaseWidget, self).__init__(parent)

    def run(self):
        raise NotImplementedError()

    def pause(self):
        raise NotImplemented()

    def stop(self):
        raise NotImplemented()

    def export(self, *args, **kwargs):
        raise NotImplemented()

    def communicate(self, *args, **kwargs):
        raise NotImplementedError()


