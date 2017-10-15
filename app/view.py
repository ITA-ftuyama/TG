#!/usr/bin/python
# -*- coding: utf-8 -*-
"""View."""
import gui
import sys
import numpy
import datetime
import threading
from PyQt4 import QtCore, QtGui
from qwt_plot import BarCurve
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt

record = False
lvl = [0, 0, 0]
messages = {}
flen = 50

class View(object):
    numPoints=1000

    def __init__(self):
        """Initializes the View."""
        global xs, ys, lvl, messages, spectrum, flen
        messages = {
            "bluetooth": [],
            "serial": [],
            "status": [],
            "sser_data": []
        }
        xs=numpy.arange(self.numPoints)
        ys=numpy.sin(3.14159*xs*10/self.numPoints) #this is our data
        spectrum=numpy.arange(flen)
        self.screen = Screen()
        self.screen.run()

    def print_message(self, message, kind):
        """Print some messages."""
        if message is not None:
            messages[kind].append(message)

    def add_message(self, message, kind):
        """Add some messages."""
        messages[kind].append(message)
        if len(messages[kind]) > 50:
            messages[kind].pop(0)

    def update_spectrum(self, spectra):
        """Print mind wave spectrum."""
        global spectrum
        spectrum = spectra

    def print_waves(self, recorder):
        """Print word on screen."""
        global ys, lvl
        #ys=numpy.roll(ys,-1)
        ys = recorder.raw.values[-1*self.numPoints:]
        lvl = [int(recorder.blink[-1] / 2), int(recorder.attention[-1] / 2), int(recorder.meditation[-1] / 2)]


class Screen(object):
    def __init__(self):
        """Initializes the Gui."""
        self.quit = False

    def run(self):
        """Runs GUI on separate thread."""
        self.thread = threading.Thread(target=self.start)
        self.thread.start()

    def die(self, event):
        """Kills thread."""
        self.app.exit()
        self.quit = True

    def start(self):
        """Starts the GUI."""
        self.app = QtGui.QApplication(sys.argv)
        self.win_plot = gui.QtGui.QMainWindow()
        self.win_plot.closeEvent = self.die

        self.uiplot = gui.Ui_win_plot()
        self.uiplot.setupUi(self.win_plot)

        # tell buttons what to do when clicked
        self.uiplot.btnA.clicked.connect(self.plot)
        self.uiplot.btnB.clicked.connect(lambda: self.uiplot.timer.setInterval(100.0))
        self.uiplot.btnC.clicked.connect(lambda: self.uiplot.timer.setInterval(10.0))
        self.uiplot.btnD.clicked.connect(lambda: self.uiplot.timer.setInterval(1.0))

        # set up the QwtPlot (pay attention!)
        self.c=Qwt.QwtPlotCurve()  #make a curve
        self.c.setPen(QtGui.QPen(Qt.Qt.darkRed, 1.2))
        self.c.attach(self.uiplot.qwtPlot) #attach it to the qwtPlot object

        # set up the QwtPlot (pay attention!)
        self.bar=[]
        for i in range(flen - 1):
            value = float(spectrum[i] * 1000)
            self.bar.append(BarCurve(Qt.Qt.black, self.wave_color(i)))
            self.bar[i].attach(self.uiplot.qwtBarPlot)
            self.bar[i].setData([25 + i * 10, 400 - value], [5, value])

        # set up timer to replot
        self.uiplot.timer = QtCore.QTimer() #start a timer (to call replot events)
        self.uiplot.timer.start(10.0) #set the interval (in ms)
        self.win_plot.connect(self.uiplot.timer, QtCore.SIGNAL('timeout()'), self.plot)

        # plot messages
        self.uiplot.msg_timer = QtCore.QTimer() #start a timer (to call replot events)
        self.uiplot.msg_timer.start(500.0) #set the interval (in ms)
        self.win_plot.connect(self.uiplot.msg_timer, QtCore.SIGNAL('timeout()'), self.plot_messages)
        self.uiplot.bluetooth.setStyleSheet('color: blue')
        self.uiplot.serial.setStyleSheet('color: red')
        self.uiplot.status.setStyleSheet('color: green')

        # set up button
        self.uiplot.pushButton.clicked.connect(self.record)

        self.win_plot.show()
        sys.exit(self.app.exec_())

    def plot(self):
        global ys, spectrum, flen
        #ys=numpy.roll(ys,-1)
        self.c.setData(xs, ys)
        for i in range(flen - 1):
            value = numpy.log10(float(spectrum[i] * 1000) + 1)
            self.bar[i].setData([i, i + 1], [0, value])

        self.uiplot.qwtPlot.replot()
        self.uiplot.qwtBarPlot.replot()

        self.uiplot.progressBar.setValue(lvl[0])
        self.uiplot.progressBar_2.setValue(lvl[1])
        self.uiplot.progressBar_3.setValue(lvl[2])

    def plot_messages(self):
        global messages
        self.uiplot.bluetooth.setText("[Bluetooth]: %s" % self.substr(messages["bluetooth"]))
        self.uiplot.serial.setText("[Serial]: %s" % self.substr(messages["serial"]))
        self.uiplot.status.setText("[Errors]: %s" % self.substr(messages["status"]))
        self.uiplot.data.setText("[Data]: %s" % self.substr(messages["sser_data"]))

    def record(self):
        global record
        if not record:
            print "Start recording"
            self.uiplot.pushButton.setText("Recording")
        else:
            print "Stop recording"
            self.uiplot.pushButton.setText("Not Recording")
            self.save_record()
        record = not record

    def save_record(self):
        global ys
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        numpy.savetxt('records/' + now + '.txt', ys, delimiter="\n", fmt="%s") 

    def substr(self, messages):
        """Print cropped message."""
        msg = "; ".join(messages)
        return msg[-100:]

    def wave_color(self, freq):
        """Color according to the wave."""
        if freq < 3:
            return Qt.Qt.white #deltaColor
        elif freq < 8:
            return Qt.Qt.magenta #thetaColor
        elif freq < 13:
            return Qt.Qt.red #alphaColor
        elif freq < 30:
            return Qt.Qt.cyan #betaColor
        else:
            return Qt.Qt.green #gammaColor
        return None
