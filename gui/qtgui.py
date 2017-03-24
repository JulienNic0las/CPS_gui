# -*- coding: utf-8 -*
import sys
import os
import textwrap
import queue

# GUI modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from capaplot_ui import CPForm
from batch_ui import BatchForm

# Project modules
#import polar as polar
#import thrust_display
#import main as main
#from load_yaml_model import extract_data

#import version
#__version__ = version.__version__


class MainAppForm(QDialog):

    def __init__(self, parent=None):
        super(MainAppForm, self).__init__(parent)

        # Set the main dialogs
        cp_form = CPForm()
        batch_form = BatchForm()

        # Set a notebook and populate it
        self.notebook = QTabWidget()
        self.notebook.addTab(cp_form, 'Capability Plots')
        self.notebook.addTab(batch_form, 'Quasi-Static Analysis')

        # Define a grid layout
        layout = QGridLayout()
        layout.addWidget(self.notebook, 0, 0)
        self.setLayout(layout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = MainAppForm()
    form.show()
    sys.exit(app.exec_())
