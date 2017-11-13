#!/usr/bin/python
# -*- coding: utf-8 -*-
"""View."""
import gui
import sys
import numpy
import threading
from mindwave.pyeeg import bin_power
from PyQt4 import QtCore, QtGui
from qwt_plot import BarCurve
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt

# Gui info
lvl = [[], [], []]
messages = {}
actions = ['idle']
action_msgs = ['idle 1.0']
intention = 'idle 1.0'
has_intention = False
flen = 50

# Recording opts
record = False
rec_start = 0
rec_stop = 0
rec_period = 1024
recorder_size = 0
over = False
recorded = []


class View(object):
    numPoints=1000

    def __init__(self):
        """Initializes the View."""
        global xs, ys, lvl, messages, spectrum, flen
        messages = {
            "bluetooth": [],
            "serial": [],
            "status": []
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

    def print_action(self, action, proba):
        global actions, intention, has_intention
        intention = action + " %.2f" % proba
        has_intention = (proba > 0.6 and action != actions[-1])
        if has_intention:
            actions.append(action)
            action_msgs.append(action + " %.2f" % proba)

    def update_spectrum(self, spectra):
        """Print mind wave spectrum."""
        global spectrum
        spectrum = spectra

    def print_waves(self, recorder):
        """Print word on screen."""
        global ys, lvl, recorded, recorder_size
        #ys=numpy.roll(ys,-1)
        recorded = recorder.raw.values
        recorder_size = len(recorder.raw.values)
        ys = recorder.raw.values[-1*self.numPoints:]
        
        lvl[0].append(recorder.blink[-1])
        lvl[1].append(recorder.attention[-1])
        lvl[2].append(recorder.meditation[-1])


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
        self.uiplot.btnA.clicked.connect(lambda: self.uiplot.timer.setInterval(100.0))
        self.uiplot.btnB.clicked.connect(lambda: self.uiplot.timer.setInterval(50.0))
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
        self.uiplot.timer.start(50.0) #set the interval (in ms)
        self.win_plot.connect(self.uiplot.timer, QtCore.SIGNAL('timeout()'), self.plot)

        # plot messages
        self.uiplot.msg_timer = QtCore.QTimer() #start a timer (to call replot events)
        self.uiplot.msg_timer.start(500.0) #set the interval (in ms)
        self.win_plot.connect(self.uiplot.msg_timer, QtCore.SIGNAL('timeout()'), self.plot_messages)
        self.uiplot.bluetooth.setStyleSheet('color: blue')
        self.uiplot.serial.setStyleSheet('color: red')
        self.uiplot.status.setStyleSheet('color: green')
        self.uiplot.intention_label.setStyleSheet('color: blue')
        self.uiplot.action_label.setStyleSheet('color: green')
        self.uiplot.action_label.setWordWrap(True)

        # set up button
        self.uiplot.pushButton.clicked.connect(self.record)

        self.win_plot.show()
        sys.exit(self.app.exec_())

    def plot(self):
        global ys, over, spectrum, has_intention, flen, rec_start, recorder_size
        #ys=numpy.roll(ys,-1)

        # Real time EEG
        self.c.setData(xs, ys)
        self.uiplot.qwtPlot.replot()

        # Frequency EEG
        for i in range(flen - 1):
            value = numpy.log10(float(spectrum[i] * 1000) + 1)
            self.bar[i].setData([i, i + 1], [0, value])
        self.uiplot.qwtBarPlot.replot()

        # Mindwave levels
        if len(lvl[0]) > 0:
            self.uiplot.progressBar.setValue(int(numpy.mean(lvl[0][-50:])))
            self.uiplot.progressBar_2.setValue(int(numpy.mean(lvl[1][-50:])))
            self.uiplot.progressBar_3.setValue(int(numpy.mean(lvl[2][-50:])))

        # Intention color
        if has_intention:
            self.uiplot.intention_label.setStyleSheet('color: red')
        else:
            self.uiplot.intention_label.setStyleSheet('color: blue')

        # Recording info
        if record:
            recording = (recorder_size - rec_start) % rec_period
            remaining = (rec_period - recording)
            cycle     = (recorder_size - rec_start) / rec_period
            
            self.uiplot.pushButton.setText("Recording in %s" % remaining)
            if cycle % 2 == 0:
                self.c.setPen(QtGui.QPen(Qt.Qt.darkRed, 1.2))
            else: 
                self.c.setPen(QtGui.QPen(Qt.Qt.blue, 1.2))

            # Recording is over on 5th period
            if cycle == 10:
                over = True
                self.record()


    def plot_messages(self):
        global messages, action, intention
        # Messages info
        self.uiplot.bluetooth.setText("[Bluetooth]: %s" % self.substr(messages["bluetooth"]))
        self.uiplot.serial.setText("[Serial]: %s" % self.substr(messages["serial"]))
        self.uiplot.status.setText("[Errors]: %s" % self.substr(messages["status"]))

        # Action info
        self.uiplot.intention_label.setText("Intentions: [%s]" % intention)
        self.uiplot.action_label.setText("Actions:      [%s]" % self.substr(action_msgs))

    def record(self):
        global record, over, rec_start, rec_stop, recorder_size
        if not record:
            self.uiplot.pushButton.setText("Recording")
            rec_start = recorder_size
        else:
            self.uiplot.pushButton.setText("Not Recording")
            self.c.setPen(QtGui.QPen(Qt.Qt.darkRed, 1.2))
            rec_stop = recorder_size
            if over:
                self.save_record()
        record = not record
        over = False

    def save_record(self):
        global ys, flen, recorded
        step = 0
        data = []
        spec = []
        i = rec_start
        while i + rec_period < rec_stop:
            if step % 2 != 0:
                # Cropping the recorded session
                session = recorded[i:(i+rec_period)]
                dt, data_spec = bin_power(session, range(flen), 512)
                data.append(session)
                spec.append(data_spec)
            i += rec_period
            step += 1

        if len(data) > 0:
            data = numpy.array(data)
            spec = numpy.array(spec)
            file = str(self.uiplot.lineEdit.text())
            
            numpy.savetxt('records/raw/'  + file + '.txt', data, delimiter=" ", fmt="%s", newline="\r\n") 
            numpy.savetxt('records/spec/' + file + '.txt', spec, delimiter=" ", fmt="%s", newline="\r\n") 

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
