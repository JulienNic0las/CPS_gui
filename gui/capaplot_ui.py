# -*- coding: utf-8 -*
import sys
import os
import textwrap
import queue

# GUI modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Plotting modules
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT


class ValidateEntry(QLineEdit):
    """Custom QLineEdit widget in order to link a dict key, value with
    the edit value.
    """
    def __init__(self, _dict, key, default=None, valuetype=None, parent=None):
        super(ValidateEntry, self).__init__(parent)
        self._dict = _dict
        self._dict[key] = default
        self._key = key
        self._type = valuetype
        if not default is None:
            self.setText(str(default))

        self.textChanged.connect(self._check)

    def _check(self, _dict):
        if not self._type:
            return
        try:
            _val = self._type(self.text())
            self._dict[self._key] = self.text()
            self.setStyleSheet('QLineEdit{background-color:white}')

        except ValueError:
            self.setStyleSheet('QLineEdit{background-color:indianred}')


class InputArea(QWidget):

    def __init__(self, parent=None):
        super(InputArea, self).__init__(parent)

        # Reference to the parent attribute _params. Used to share a
        # unique dictionnary across every widgets of the input area
        self.params = parent._params

        layout = QGridLayout()

        row_widget = 0

        # Vessel model input
        layout.addWidget(QLabel('<b>Vessel</b>'), row_widget, 0, 1, 3)
        row_widget += 1
        lineedit_vessel = QLineEdit()
        button_vessel = QPushButton('...')
        layout.addWidget(QLabel('Vessel Model:'), row_widget, 0)
        layout.addWidget(lineedit_vessel, row_widget, 1)
        layout.addWidget(button_vessel, row_widget, 2)
        button_vessel.clicked.connect(self._file_dialog)
        row_widget +=1

        # Simulation type
        layout.addWidget(QLabel('<b>Simulation</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        layout.addWidget(QRadioButton('Thrust Capability Plot'), row_widget, 0, 1, 3)
        row_widget +=1
        layout.addWidget(QRadioButton('Wind Speed CP'), row_widget, 0, 1, 3)
        row_widget +=1
        layout.addWidget(QRadioButton('Current Speed CP'), row_widget, 0, 1, 3)
        row_widget +=1
        layout.addWidget(QRadioButton('DNV ERN'), row_widget, 0, 1, 3)
        row_widget +=1
        layout.addWidget(QRadioButton('Dynamic CP (OrcaFlex)'), row_widget, 0, 1, 3)
        row_widget +=1

        # Environmental parameters
        layout.addWidget(QLabel('<b>Environment</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        lineedit_hs = ValidateEntry(self.params, 'wave_hs', 0.0, float)
        layout.addWidget(QLabel('Wave Hs'), row_widget, 0)
        layout.addWidget(lineedit_hs, row_widget, 1)
        layout.addWidget(QLabel('[m]'), row_widget, 2)
        row_widget +=1
        lineedit_tp = ValidateEntry(self.params, 'wave_tp', 0.0, float)
        layout.addWidget(QLabel('Wave Tp'), row_widget, 0)
        layout.addWidget(lineedit_tp, row_widget, 1)
        layout.addWidget(QLabel('[s]'), row_widget, 2)
        row_widget +=1
        lineedit_gamma = ValidateEntry(self.params, 'wave_gamma', 0.0, float)
        layout.addWidget(QLabel('Wave Gamma'), row_widget, 0)
        layout.addWidget(lineedit_gamma, row_widget, 1)
        layout.addWidget(QLabel('[-]'), row_widget, 2)
        row_widget +=1
        lineedit_curr = ValidateEntry(self.params, 'curr_vel', 0.0, float)
        layout.addWidget(QLabel('Current Vel.'), row_widget, 0)
        layout.addWidget(lineedit_curr, row_widget, 1)
        layout.addWidget(QLabel('[m/s]'), row_widget, 2)
        row_widget +=1
        lineedit_wind = ValidateEntry(self.params, 'wind_vel', 0.0, float)
        layout.addWidget(QLabel('Wind Vel.'), row_widget, 0)
        layout.addWidget(lineedit_wind, row_widget, 1)
        layout.addWidget(QLabel('[m/s]'), row_widget, 2)
        row_widget +=1

        # External Loads
        layout.addWidget(QLabel('<b>Applied Loads</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        lineedit_loadx = ValidateEntry(self.params, 'load_x', 0.0, float)
        layout.addWidget(QLabel('Pipe Load X'), row_widget, 0)
        layout.addWidget(lineedit_loadx, row_widget, 1)
        layout.addWidget(QLabel('[kN]'), row_widget, 2)
        row_widget +=1
        lineedit_loady = ValidateEntry(self.params, 'load_y', 0.0, float)
        layout.addWidget(QLabel('Pipe Load Y'), row_widget, 0)
        layout.addWidget(lineedit_loady, row_widget, 1)
        layout.addWidget(QLabel('[kN]'), row_widget, 2)
        row_widget +=1
        lineedit_loadz = ValidateEntry(self.params, 'load_z', 0.0, float)
        layout.addWidget(QLabel('Pipe Moment Z'), row_widget, 0)
        layout.addWidget(lineedit_loadz, row_widget, 1)
        layout.addWidget(QLabel('[kN.m]'), row_widget, 2)
        row_widget +=1

        # Main propellers options
        layout.addWidget(QLabel('<b>Main Propellers</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        combobox_rudder_mng = QComboBox()
        layout.addWidget(QLabel('Rudder Management'), row_widget, 0)
        layout.addWidget(combobox_rudder_mng, row_widget, 1)
        layout.addWidget(QLabel(''), row_widget, 2)
        row_widget +=1
        lineedit_rudder_angle = ValidateEntry(
            self.params, 'main_propellers_rudder_angle', 0.0, float
            )
        layout.addWidget(QLabel('Rudder Angles'), row_widget, 0)
        layout.addWidget(lineedit_rudder_angle, row_widget, 1)
        layout.addWidget(QLabel('[deg]'), row_widget, 2)
        row_widget +=1

        # Allocator options
        layout.addWidget(QLabel('<b>Allocator Options</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        combobox_failed_thruster = QComboBox()
        layout.addWidget(QLabel('Inactive Thrusters'), row_widget, 0)
        layout.addWidget(combobox_failed_thruster, row_widget, 1)
        layout.addWidget(QLabel(''), row_widget, 2)
        row_widget +=1
        lineedit_use_limit = ValidateEntry(
            self.params, 'use_limitation', 0.0, float
            )
        layout.addWidget(QLabel('Utilization Limit'), row_widget, 0)
        layout.addWidget(lineedit_use_limit, row_widget, 1)
        layout.addWidget(QLabel('[%]'), row_widget, 2)
        row_widget +=1
        checkbox_symmetrize = QCheckBox('Symmetrize')
        layout.addWidget(checkbox_symmetrize, row_widget, 0)
        checkbox_symmetrize = QCheckBox('Thrust Loss')
        layout.addWidget(checkbox_symmetrize, row_widget, 1, 1, 2)
        row_widget +=1
        checkbox_symmetrize = QCheckBox('Wave/Current')
        layout.addWidget(checkbox_symmetrize, row_widget, 0)
        checkbox_symmetrize = QCheckBox('Fdz_dependency')
        layout.addWidget(checkbox_symmetrize, row_widget, 1, 1, 2)
        row_widget +=1

        # To have no space between widgets
        layout.setSpacing(0)
        # To have no space at the border of the layout
        layout.setMargin(0)
        self.setLayout(layout)

    def _update_params(self, key):
        self.params[key] = None

    def _toggle_vessel_selection(self, fname):
        pass

    def _toggle_rudder_management(self, event):
        pass

    def _file_dialog(self, entry_widget):
        options = {
            'caption': 'Vessel model file',
            'directory': os.path.realpath('..') + '\\Vessels',
            'filter': ('YAML file (*.yml)'),
            }
        fname = QFileDialog.getOpenFileName(self, **options)
        if fname:
            entry_widget.setText(name.split('/')[-1])
            self.params['vessel'] = fname

    def _file_inspect(self):
        if 'vessel' in self.params:
            vessel_file = self.params['vessel']
        raise NotImplementedError('Text editor')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):

        self.fig = plt.Figure()
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)


class GraphArea(QWidget):

    # Figures dimensions
    HEIGHT = 560
    WIDTH = 800

    def __init__(self, parent=None):
        super(GraphArea, self).__init__(parent)

        # Set a notebook
        self.notebook = QTabWidget()

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(self.notebook, 0, 0)
        self.setLayout(layout)

        # Create two tabs
        self._create_polar_tab()
        self._create_vector_tab()

    def _create_polar_tab(self):

        polar_plot_area = MplCanvas(self)
        self.notebook.addTab(polar_plot_area, 'Polar Plot')

    def _create_vector_tab(self):

        vector_plot_area = MplCanvas(self)
        self.notebook.addTab(vector_plot_area, 'Polar Plot')

    def plot_polar(self, results=None, simu_info=None):
        # simu_info may be no longer necessary. Share a common dict between
        # the differen widgets
        pass

    def plot_vector(self, solutions):
        pass


class StatusBar(QWidget):

    def __init__(self, parent=None):
        super(StatusBar, self).__init__(parent)

        self.progress = 0.0
        self.status = 'Ready'

        # Status label
        self.status_label = QLabel(self.status)
        # Progress bar
        self.progress_bar = QProgressBar()
        # Progress label
        self.progress_label = QLabel('0.0%')

        layout = QHBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)

        self.setLayout(layout)

    def update_progress(self, value):
        pass

    def update_status(self, text):
        pass


class ButtonBar(QWidget):

    def __init__(self, parent=None):
        super(ButtonBar, self).__init__(parent)

        # Define buttons
        start_button = QPushButton('START')
        savefig_button = QPushButton('SAVE FIG')
        export_button = QPushButton('EXPORT TXT')

        # Set up the layout
        layout = QHBoxLayout()
        layout.addWidget(start_button)
        layout.addWidget(savefig_button)
        layout.addWidget(export_button)
        self.setLayout(layout)

        # Bind buttons to the parent methods
        start_button.clicked.connect(parent.run)
        savefig_button.clicked.connect(parent.save_fig)
        export_button.clicked.connect(parent.export)


class CPForm(QDialog):

    _params = {}

    def __init__(self, parent=None):
        super(CPForm, self).__init__(parent)

        # Define sub widgets
        input_area = InputArea(self)
        graph_area = GraphArea(self)
        button_bar = ButtonBar(self)
        status_bar = StatusBar(self)

        # Set up the layout
        layout = QGridLayout()
        layout.addWidget(input_area, 0, 0)
        layout.addWidget(graph_area, 0, 1)
        layout.addWidget(button_bar, 1, 0)
        layout.addWidget(status_bar, 1, 1)

        self.setLayout(layout)

        # Create a period call using a timer
        self.periodic_call()

    def periodic_call(self):
        pass

    def run(self):
        # TEMPORARY: Display the user input data gathered through the UI
        print(self._params)

    def save_fig(self):
        options = {
            'caption': 'Save figure as',
            'directory': os.path.realpath('..') + '\\Results',
            'filter': ('PNG file (*.png)'),
            }
        fname = QFileDialog.getOpenFileName(self, **options)

    def export(self):
        options = {
            'caption': 'Save simulation as',
            'directory': os.path.realpath('..') + '\\Results',
            'filter': ('Text file (*.txt)'),
            }
        fname = QFileDialog.getOpenFileName(self, **options)


class AppForm(QDialog):

    def __init__(self, parent=None):
        super(AppForm, self).__init__(parent)

        # Set the main dialogs
        form = CPForm()

        # Define a grid layout
        layout = QGridLayout()
        layout.addWidget(form, 0, 0)
        self.setLayout(layout)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    sys.exit(app.exec_())
