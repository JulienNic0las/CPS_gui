# -*- coding: utf-8 -*-
"""
    Demo of a toolbar
"""
import sys
import os
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
from functools import partial

ICONS_PATH = os.path.join(os.getcwd(), 'icons')
print(ICONS_PATH)

class MyWidget(QWidget):

    def __init__(self, parent=None, text=''):
        super(MyWidget, self).__init__(parent)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


class ToolBarDemo(QMainWindow):

    def __init__(self, parent=None):
        super(ToolBarDemo, self).__init__(parent)
        self.initUI()

    def initUI(self):

        self.init_simu_panel()
        self.init_toolbar()

        # Build some widgets
        self._widgets = QStackedWidget()
        self.setCentralWidget(self._widgets)
        for i in range(3):
            widget = MyWidget(self, 'Widget %i' % i)
            self._widgets.addWidget(widget)

        self.setWindowTitle('Toolbar Demo!!')
        self.show()

    def init_simu_panel(self):

        toolbar = QToolBar('Simulations')
        toolbar.setStyleSheet(
            'border: 0px;'
            'background-color: #404244;'
            'border-right: 1px solid #26282A;'
            'border-left: 1px solid #26282A;'
            )
        toolbar.setOrientation(Qt.Vertical)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.LeftToolBarArea, toolbar)

        # Create a QActionGroup to group actions together to make each
        # actions checkable, one at a time
        action_group = QActionGroup(self)

        action = QAction(QIcon(ICONS_PATH + '/' + 'home.png'), 'Dummy', action_group)
        action.objectName = 't'
        action.triggered.connect(partial(self.switch_widget, 0))
        toolbar.addAction(action)

        action = QAction(QIcon(ICONS_PATH + '/' + 'home.png'), 'Dummy', action_group)
        action.triggered.connect(partial(self.switch_widget, 1))
        toolbar.addAction(action)

        action = QAction(QIcon(ICONS_PATH + '/' + 'settings_24.png'), 'Settings', action_group)
        action.triggered.connect(partial(self.switch_widget, 2))
        toolbar.addAction(action)

        # Apply style to each actions
        for action in toolbar.actions():
            action.setCheckable(True)
            widget = toolbar.widgetForAction(action)
            widget.setStyleSheet(
                'QToolButton {color: white; border: 0px}'
                'QToolButton:checked {background-color: #26282A};'
                )
            widget.setFixedSize(80, 60)

    def init_toolbar(self):

        # Make void toolbar to prevent button to be above the simulation
        # left pannel
        tb = QToolBar()
        tb.setStyleSheet(
            'background-color: #404244;'
            'min-width: 82px;'
            'border: 0px;'
            'border-left: 1px solid #26282A;'
            'border-bottom: 1px solid #26282A;'
            )
        tb.setOrientation(Qt.Horizontal)
        tb.setMovable(False)
        tb.setFloatable(False)
        self.addToolBar(tb)

        toolbar = QToolBar('Toolbar')
        toolbar.setStyleSheet(
            'background-color: #404244;'
            'border-right: 1px solid #26282A;'
            'border-left: 1px solid #26282A;'
            'border-bottom: 1px solid #26282A;'
            )
        toolbar.setOrientation(Qt.Horizontal)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(toolbar)

        action = QAction(QIcon(ICONS_PATH + '/' + 'ic_play_arrow_24px.png'), 'run', self)
        action.triggered.connect(self.cbk_run)
        toolbar.addAction(action)

        action = QAction(QIcon(ICONS_PATH + '/' + 'stop.png'), 'stop', self)
        action.triggered.connect(self.cbk_stop)
        toolbar.addAction(action)

    def switch_widget(self, widget_id):
        self._widgets.setCurrentIndex(widget_id)

    def cbk_run(self):
        print('Ruuuuuuunnnn')

    def cbk_stop(self):
        print('STOP !!')


class App(QMainWindow):

    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        widget = MyWidget(self, 'Weeeeedget!')
        self.setCentralWidget(widget)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = ToolBarDemo()
    #form = App()
    sys.exit(app.exec_())
