# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_win_plot(object):
    def setupUi(self, win_plot):
        win_plot.setObjectName(_fromUtf8("win_plot"))
        win_plot.resize(844, 682)
        self.centralwidget = QtGui.QWidget(win_plot)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.qwtPlot = QwtPlot(self.centralwidget)
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.verticalLayout.addWidget(self.qwtPlot)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(6, 0, 6, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnA = QtGui.QPushButton(self.centralwidget)
        self.btnA.setObjectName(_fromUtf8("btnA"))
        self.horizontalLayout.addWidget(self.btnA)
        self.btnB = QtGui.QPushButton(self.centralwidget)
        self.btnB.setObjectName(_fromUtf8("btnB"))
        self.horizontalLayout.addWidget(self.btnB)
        self.btnC = QtGui.QPushButton(self.centralwidget)
        self.btnC.setObjectName(_fromUtf8("btnC"))
        self.horizontalLayout.addWidget(self.btnC)
        self.btnD = QtGui.QPushButton(self.centralwidget)
        self.btnD.setObjectName(_fromUtf8("btnD"))
        self.horizontalLayout.addWidget(self.btnD)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.bluetooth = QtGui.QLabel(self.centralwidget)
        self.bluetooth.setAutoFillBackground(False)
        self.bluetooth.setTextFormat(QtCore.Qt.RichText)
        self.bluetooth.setWordWrap(False)
        self.bluetooth.setObjectName(_fromUtf8("bluetooth"))
        self.verticalLayout_2.addWidget(self.bluetooth)
        self.serial = QtGui.QLabel(self.centralwidget)
        self.serial.setObjectName(_fromUtf8("serial"))
        self.verticalLayout_2.addWidget(self.serial)
        self.status = QtGui.QLabel(self.centralwidget)
        self.status.setObjectName(_fromUtf8("status"))
        self.verticalLayout_2.addWidget(self.status)
        self.data = QtGui.QLabel(self.centralwidget)
        self.data.setMaximumSize(QtCore.QSize(16777215, 17))
        self.data.setObjectName(_fromUtf8("data"))
        self.verticalLayout_2.addWidget(self.data)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        win_plot.setCentralWidget(self.centralwidget)

        self.retranslateUi(win_plot)
        QtCore.QMetaObject.connectSlotsByName(win_plot)

    def retranslateUi(self, win_plot):
        win_plot.setWindowTitle(_translate("win_plot", "TEEG Application", None))
        self.label_2.setText(_translate("win_plot", "TEEG - Translate Electroencefalography", None))
        self.btnA.setText(_translate("win_plot", "A", None))
        self.btnB.setText(_translate("win_plot", "B", None))
        self.btnC.setText(_translate("win_plot", "C", None))
        self.btnD.setText(_translate("win_plot", "D", None))
        self.bluetooth.setText(_translate("win_plot", "<html><head/><body><p><span style=\" color:#0000ff;\">[Bluetooth]</span></p></body></html>", None))
        self.serial.setText(_translate("win_plot", "<html><head/><body><p><span style=\" color:#aa0000;\">[Serial]</span></p></body></html>", None))
        self.status.setText(_translate("win_plot", "<html><head/><body><p><span style=\" color:#005500;\">[Status]</span></p></body></html>", None))
        self.data.setText(_translate("win_plot", "[Data]", None))

from qwt_plot import QwtPlot
