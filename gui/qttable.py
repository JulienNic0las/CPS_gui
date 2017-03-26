#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Table(QWidget):

    column_headers = (
        'Hs', 'Tp', 'Gamma', 'Heading', 'Curr. vel.', 'Curr. Dir.',
        'Wind Vel.', 'Wind Dir.', 'Probability',
        )
    init_row_number = 10

    def __init__(self, parent=None):
        super(Table, self).__init__(parent)

        # Set up a table widget
        self.table = QTableWidget()

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.initialise()

    def initialise(self):

        # Set up the number of rows and columns
        self.table.setColumnCount(len(self.column_headers))
        self.table.setRowCount(self.init_row_number)

        # Set up headers
        for i, col in enumerate(self.column_headers):
            item = QTableWidgetItem()
            item.setText(col)
            self.table.setHorizontalHeaderItem(i, item)

        # Set up indexes
        for i in range(1, 1, 1):
            item = QTableWidgetItem()
            item.setText(str(i))
            self.table.setVerticalHeaderItem(i, item)


    def keyPressEvent(self, event):
        """Override key press event handler to add the following features:
            - Past table-like data from clipboard
            - Delete data using supp. key
        """

        selected = self.table.selectedRanges()

        if not selected:
            return

        # Paste data from clipboard
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            # Check to see if clipboard contains table-like data. Data
            # columns must be separated by '\t' (tabs) and rows by
            # '\n'.
            clip = QApplication.clipboard()
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
                        QTableWidgetItem(col)
                        )
            return

        # Enable deleting multiple cells using 'suppr' key
        if event.key() == Qt.Key_Delete:

            # Figure out boudaries of the selected data to delete
            first_row = selected[0].topRow()
            last_row = selected[0].bottomRow()
            first_col = selected[0].leftColumn()
            last_col = selected[0].rightColumn()

            # Set null value ('') in each cells of the selected range
            for r in range(first_row, last_row + 1, 1):
                for c in range(first_col, last_col + 1, 1):
                    self.table.setItem(r, c, QTableWidgetItem(''))
            return

    def update_rows(self, nrows):
        """Append or remove rows to the table based on a given number of
        rows.
        """
        while self.table.rowCount() != nrows:
            # Remove last row
            if self.table.rowCount() > nrows:
                self.table.removeRow(self.table.rowCount() - 1)
            # Append new row
            elif self.table.rowCount() < nrows:
                self.table.insertRow(self.table.rowCount())

    def get_values(self):
        """Return values of the table as dictionnary. Empty cells are
        considered as NaN values.
        """

        _values = {}

        for j in range(self.table.columnCount()):
            rowvals = []
            for i in range(self.table.rowCount()):
                cell = self.table.item(i, j)
                if cell:
                    try:
                        rowvals.append((i, float(cell.text())))
                    except ValueError as e:
                        raise ValueError('Table content must be numbers only')
                else:
                    rowvals.append((i, float('nan')))
                _values[self.column_headers[j]] = dict(rowvals)

        return _values


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("Application")

        # Add A label, a spinbox and a table
        label = QLabel('Nb of simulations')
        spinBox = QSpinBox()
        self.table = Table()
        button = QPushButton('Values')

        spinBox.setValue(self.table.init_row_number)

        # Define a grid layout
        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(spinBox, 0, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(button, 2, 0)

        self.setLayout(layout)

        # Connect the spinbox with the table widget to add or remove rows
        spinBox.valueChanged[int].connect(self.table.update_rows)

        # Connect button to display table content
        button.clicked.connect(self.display_table_content)

    def display_table_content(self):
        print(self.table.get_values())


def main():
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
