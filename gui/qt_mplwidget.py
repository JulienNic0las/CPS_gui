# -*- coding:Utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.fig = plt.Figure()
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

        # Dunno what the purpose of this line
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        plot_area = MplCanvas(self)

        layout = QGridLayout()
        layout.addWidget(plot_area, 0, 0)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
