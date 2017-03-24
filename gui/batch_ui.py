# -*- coding: utf-8 -*
import sys
import os
import queue
from functools import partial

# GUI module
from PyQt4 import QtCore, QtGui


COLUMN_HEADERS = (
    'Hs', 'Tp', 'Gamma', 'Heading', 'Curr. vel.', 'Curr. Dir.',
    'Wind Vel.', 'Wind Dir.', 'Probability',
    )


class Table(QtGui.QDialog):

    """Table widget based on a PyQt.QTableWidget"""

    def __init__(self, parent=None, column_headers=None, init_rows=10):
        super(Table, self).__init__(parent)

        # Set up a table widget
        self.table = QtGui.QTableWidget()
        self.column_headers = column_headers
        self.init_row_number = init_rows

        # Layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.initialise()

    def initialise(self):

        # Set up the number of rows and columns
        self.table.setColumnCount(len(self.column_headers))
        self.table.setRowCount(self.init_row_number)

        # Set up headers
        for i, col in enumerate(self.column_headers):
            item = QtGui.QTableWidgetItem()
            item.setText(col)
            self.table.setHorizontalHeaderItem(i, item)

        # Set up indexes
        for i in range(1, 1, 1):
            item = QtGui.QTableWidgetItem()
            item.setText(str(i))
            self.table.setVerticalHeaderItem(i, item)

    def keyPressEvent(self, event):
        """Override key press event handler to add the following features:
            - Past table-like data from clipboard
            - Delete data
        """

        selected = self.table.selectedRanges()

        if not selected:
            return

        # Paste data from clipboard
        if event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
            # Check to see if clipboard contains table-like data. Data
            # columns must be separated by '\t' (tabs) and rows by
            # '\n'.
            clip = QtGui.QApplication.clipboard()
            raw_text = clip.text()

            if not raw_text:
                return

            first_row = selected[0].topRow()
            first_col = selected[0].leftColumn()

            for r, row in enumerate(raw_text.split('\n')):
                for c, col in enumerate(row.split('\t')):
                    self.table.setItem(
                        first_row + r,
                        first_col + c,
                        QtGui.QTableWidgetItem(col)
                        )
            return

        # Enable deleting multiple cells using 'suppr' key
        if event.key() == QtCore.Qt.Key_Delete:

            first_row = selected[0].topRow()
            last_row = selected[0].bottomRow()
            first_col = selected[0].leftColumn()
            last_col = selected[0].rightColumn()

            for r in range(first_row, last_row + 1, 1):
                for c in range(first_col, last_col + 1, 1):
                    self.table.setItem(r, c, QtGui.QTableWidgetItem(''))

            return

    def update_rows(self, nrows):
        """Append or remove rows to the table"""

        # remove last rows
        while self.table.rowCount() != nrows:

            # Remove last row
            if self.table.rowCount() > nrows:
                self.table.removeRow(self.table.rowCount() - 1)

            # Append new row
            elif self.table.rowCount() < nrows:
                self.table.insertRow(self.table.rowCount())

    def get_values(self):
        """Return the table values as dictionnary. Keys are the column
        headers.
        """

        _values = {}
        try:
            for j in range(self.table.columnCount()):
                rowvals = []
                for i in range(self.table.rowCount()):
                    cell = self.table.item(i, j)
                    if cell:
                        rowvals.append((i, float(cell.text())))
                    else:
                        rowvals.append((i, float('nan')))
                _values[self.column_headers[j]] = dict(rowvals)

        except ValueError as e:
            raise ValueError('Table content must be numbers only')

        return _values


class BatchInputArea(QtGui.QDialog):

    def __init__(self, parent=None):
        super(BatchInputArea, self).__init__(parent)

        layout = QtGui.QGridLayout()

        row_widget = 0

        # Vessel model input
        layout.addWidget(QtGui.QLabel('<b>Vessel</b>'), row_widget, 0, 1, 3)
        row_widget += 1
        self.le_vessel = QtGui.QLineEdit()
        self.bt_vessel = QtGui.QPushButton('...')
        layout.addWidget(QtGui.QLabel('Vessel Model:'), row_widget, 0)
        layout.addWidget(self.le_vessel, row_widget, 1)
        layout.addWidget(self.bt_vessel, row_widget, 2)
        row_widget +=1

        # External Loads
        layout.addWidget(QtGui.QLabel('<b>Applied Loads</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        self.le_loadx = QtGui.QLineEdit()
        self.le_loadx.setText('0.0')
        self.le_loadx.setToolTip('X-axis from aft to bow')
        layout.addWidget(QtGui.QLabel('Pipe Load X'), row_widget, 0)
        layout.addWidget(self.le_loadx, row_widget, 1)
        layout.addWidget(QtGui.QLabel('[kN]'), row_widget, 2)
        row_widget +=1
        self.le_loady = QtGui.QLineEdit()
        self.le_loady.setText('0.0')
        self.le_loady.setToolTip('Y-axis from centerline to portside')
        layout.addWidget(QtGui.QLabel('Pipe Load Y'), row_widget, 0)
        layout.addWidget(self.le_loady, row_widget, 1)
        layout.addWidget(QtGui.QLabel('[kN]'), row_widget, 2)
        row_widget +=1
        self.le_loadz = QtGui.QLineEdit()
        self.le_loadz.setText('0.0')
        self.le_loadz.setToolTip('Positive from X-axis to Y-axis')
        layout.addWidget(QtGui.QLabel('Pipe Moment Z'), row_widget, 0)
        layout.addWidget(self.le_loadz, row_widget, 1)
        layout.addWidget(QtGui.QLabel('[kN.m]'), row_widget, 2)
        row_widget +=1

        # Main propellers options
        layout.addWidget(QtGui.QLabel('<b>Main Propellers</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        self.cb_rudder_mng = QtGui.QComboBox()
        self.cb_rudder_mng.addItems(('off', 'auto'))
        self.cb_rudder_mng.setEnabled(False)
        layout.addWidget(QtGui.QLabel('Rudder Management'), row_widget, 0)
        layout.addWidget(self.cb_rudder_mng, row_widget, 1)
        layout.addWidget(QtGui.QLabel(''), row_widget, 2)
        row_widget +=1
        self.le_rudder_angle = QtGui.QLineEdit()
        layout.addWidget(QtGui.QLabel('Rudder Angles'), row_widget, 0)
        layout.addWidget(self.le_rudder_angle, row_widget, 1)
        layout.addWidget(QtGui.QLabel('[deg]'), row_widget, 2)
        row_widget +=1

        # Allocator options
        layout.addWidget(QtGui.QLabel('<b>Allocator Options</b>'), row_widget, 0, 1, 3)
        row_widget +=1
        self.cb_failed_thrusters = QtGui.QComboBox()
        layout.addWidget(QtGui.QLabel('Inactive Thrusters'), row_widget, 0)
        layout.addWidget(self.cb_failed_thrusters, row_widget, 1)
        layout.addWidget(QtGui.QLabel(''), row_widget, 2)
        row_widget +=1
        self.le_use_limit = QtGui.QLineEdit()
        self.le_use_limit.setEnabled(False)
        layout.addWidget(QtGui.QLabel('Utilization Limit'), row_widget, 0)
        layout.addWidget(self.le_use_limit, row_widget, 1)
        layout.addWidget(QtGui.QLabel('[%]'), row_widget, 2)
        row_widget +=1
        self.ck_thrust_loss = QtGui.QCheckBox('Thrust Loss')
        self.ck_thrust_loss.setChecked(True)
        layout.addWidget(self.ck_thrust_loss, row_widget, 1, 1, 2)
        row_widget +=1
        self.ck_wavedamp = QtGui.QCheckBox('Wave/Current')
        layout.addWidget(self.ck_wavedamp, row_widget, 0)
        self.ck_fdz_dep = QtGui.QCheckBox('Fdz_dependency')
        layout.addWidget(self.ck_fdz_dep, row_widget, 1, 1, 2)
        row_widget +=1

        # Number of simulations to proceed
        label = QtGui.QLabel('Nb of simulations')
        self.spinBox = QtGui.QSpinBox()
        layout.addWidget(self.ck_fdz_dep, row_widget, 1, 1, 2)

        self.setLayout(layout)


class BatchFormView(QtGui.QDialog):

    def __init__(self, parent=None):
        super(BatchFormView, self).__init__(parent)

        self.resize(870, 400)

        # Add A label, a spinbox and a table
        label = QtGui.QLabel('Nb of simulations')
        self.spinBox = QtGui.QSpinBox()
        self.table = Table(column_headers=COLUMN_HEADERS)
        self.table.setMinimumSize(QtCore.QSize(600, 0))
        self.start_button = QtGui.QPushButton('START')
        self.progress_bar = QtGui.QProgressBar()

        # Add the user input area
        self.input_frame = BatchInputArea()

        self.spinBox.setValue(self.table.init_row_number)

        # Define a grid layout
        layout = QtGui.QGridLayout()
        layout.addWidget(label, 0, 3)
        layout.addWidget(self.spinBox, 0, 4)
        layout.addWidget(self.table, 1, 1, 1, 4)
        layout.addWidget(self.input_frame, 0, 0, 2, 1)
        layout.addWidget(self.start_button, 2, 0)
        layout.addWidget(self.progress_bar, 2, 1, 1, 4)

        # To setup space at the border of the layout
        layout.setMargin(0)

        self.setLayout(layout)



class AppForm(QtGui.QDialog):

    def __init__(self, parent=None):
        super(AppForm, self).__init__(parent)

        # Set the main dialogs
        self.form = BatchFormView()

        # Define a grid layout
        layout = QtGui.QGridLayout()
        layout.addWidget(self.form, 0, 0)
        self.setLayout(layout)

        # Connect the spinbox with the table widget to add or remove rows
        self.form.spinBox.valueChanged[int].connect(self.form.table.update_rows)

        # Connect the push button to the open file dialog method
        self.form.input_frame.bt_vessel.clicked.connect(
            partial(self._file_dialog, self.form.input_frame.le_vessel)
            )

        self.form.start_button.clicked.connect(self.run)

        self.set_model()

    def set_model(self):

        # Define a parameter dictionnary to store user inputs (set up
        # default values also)
        self._params = {
            'vessel': '',
            'load_x': 0.0,
            'load_y': 0.0,
            'load_z': 0.0,
            'rudder_management': 'off',
            'main_propellers_rudder_angle': 0.0,
            'failed_thrusters': '',
            'use_limitation': 1.0,
            'fdz_dep': False,
            'thrust_loss': True,
            'wave_damp': False,
            }

        # Set up the connection between the _param dict and the corresponding
        # widgets
        frame = self.form.input_frame
        frame.le_vessel.textChanged.connect(
            partial(self._update_params_lineedit, 'vessel', double=False)
            )
        frame.le_loadx.textChanged.connect(
            partial(self._update_params_lineedit, 'load_x', double=True)
            )
        frame.le_loady.textChanged.connect(
            partial(self._update_params_lineedit, 'load_y', double=True)
            )
        frame.le_loadz.textChanged.connect(
            partial(self._update_params_lineedit, 'load_z', double=True)
            )
        frame.cb_rudder_mng.currentIndexChanged.connect(
            partial(self._update_params_combobox, 'rudder_management')
            )
        frame.le_rudder_angle.textChanged.connect(
            partial(self._update_params_lineedit, 'main_propellers_rudder_angle', double=True)
            )
        frame.cb_failed_thrusters.currentIndexChanged.connect(
            partial(self._update_params_combobox, 'failed_thrusters')
            )
        frame.le_use_limit.textChanged.connect(
            partial(self._update_params_lineedit, 'use_limitation', double=True)
            )
        frame.ck_fdz_dep.stateChanged.connect(
            partial(self._update_params_lineedit, 'fdz_dep')
            )
        frame.ck_thrust_loss.stateChanged.connect(
            partial(self._update_params_lineedit, 'thrust_loss')
            )
        frame.ck_wavedamp.stateChanged.connect(
            partial(self._update_params_lineedit, 'wave_damp')
            )

    def _update_params_lineedit(self, name, double=False):

        sender = self.sender()
        print(double)

        if double:
            validator = QtGui.QDoubleValidator()
            state = validator.validate(sender.text(), 0)[0]
            if state == QtGui.QValidator.Invalid:
                color = '#f6989d'
                sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
            else:
                color = 'white'
                sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

        self._params[name] = sender.text()

    def _update_params_combobox(self, name):
        sender = self.sender()
        self._params[name] = sender.currentText()

    def _update_params_checkbox(self, name):
        sender = self.sender()
        self._params[name] = sender.checkState()

    def _file_dialog(self, entry_widget):
        options = {
            'caption': 'Vessel model file',
            'directory': os.path.realpath('..') + '\\Vessels',
            'filter': ('YAML file (*.yml)'),
            }
        fname = QtGui.QFileDialog.getOpenFileName(self, **options)
        if fname:
            entry_widget.setText(fname.split('/')[-1])

    def run(self):
        print(self._params)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    form = AppForm()
    form.show()
    sys.exit(app.exec_())
