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
        win_plot.resize(1065, 708)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_5.addWidget(self.label)
        self.qwtPlot = QwtPlot(self.centralwidget)
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.verticalLayout_5.addWidget(self.qwtPlot)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_3.addWidget(self.label_3)
        self.qwtBarPlot = QwtPlot(self.centralwidget)
        self.qwtBarPlot.setObjectName(_fromUtf8("qwtBarPlot"))
        self.verticalLayout_3.addWidget(self.qwtBarPlot)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_6.addWidget(self.groupBox_2)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_6.addWidget(self.label_6)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_6.addWidget(self.progressBar)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_6.addWidget(self.label_5)
        self.progressBar_2 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName(_fromUtf8("progressBar_2"))
        self.verticalLayout_6.addWidget(self.progressBar_2)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_6.addWidget(self.label_7)
        self.progressBar_3 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_3.setProperty("value", 24)
        self.progressBar_3.setObjectName(_fromUtf8("progressBar_3"))
        self.verticalLayout_6.addWidget(self.progressBar_3)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_6.addWidget(self.groupBox, QtCore.Qt.AlignBottom)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout_6.addWidget(self.pushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
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
        self.label.setText(_translate("win_plot", "<html><head/><body><p><span style=\" font-size:14pt;\">Dados em tempo real</span></p></body></html>", None))
        self.label_3.setText(_translate("win_plot", "<html><head/><body><p><span style=\" font-size:14pt;\">Análise espectral</span></p></body></html>", None))
        self.groupBox_2.setTitle(_translate("win_plot", "Niveis Mindwave", None))
        self.label_6.setText(_translate("win_plot", "Piscada", None))
        self.label_5.setText(_translate("win_plot", "Atenção", None))
        self.label_7.setText(_translate("win_plot", "Meditação", None))
        self.pushButton.setText(_translate("win_plot", "Not Recording", None))
        self.btnA.setText(_translate("win_plot", "A", None))
        self.btnB.setText(_translate("win_plot", "B", None))
        self.btnC.setText(_translate("win_plot", "C", None))
        self.btnD.setText(_translate("win_plot", "D", None))
        self.label_4.setText(_translate("win_plot", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Log de mensagens</span></p></body></html>", None))
        self.bluetooth.setText(_translate("win_plot", "<html><head/><body><p><span style=\" color:#0000ff;\">[Bluetooth]</span></p></body></html>", None))
        self.serial.setText(_translate("win_plot", "<html><head/><body><p><span style=\" color:#aa0000;\">[Serial]</span></p></body></html>", None))
        self.status.setText(_translate("win_plot", "<html><head/><body><p><span style=\" color:#005500;\">[Status]</span></p></body></html>", None))
        self.data.setText(_translate("win_plot", "[Data]", None))

from qwt_plot import QwtPlot
