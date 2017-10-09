#!/usr/bin/python
# -*- coding: utf-8 -*-
"""View."""
import gui
import sys
import numpy
import threading
from PyQt4 import QtCore, QtGui
from qwt_plot import BarCurve
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt

messages = {}

class View(object):
    numPoints=1000

    def __init__(self):
        """Initializes the View."""
        global xs, ys, messages, spectrum, flen
        messages = {
            "bluetooth": [],
            "serial": [],
            "status": [],
            "sser_data": []
        }
        xs=numpy.arange(self.numPoints)
        ys=numpy.sin(3.14159*xs*10/self.numPoints) #this is our data
        flen=50
        spectrum=numpy.arange(flen)
        self.screen = Screen()
        self.screen.run()

    def gui(self):
        """Print some GUI."""
        # self.window.fill(backColor)
        # self.window.blit(font_32.render("Mindwave Controller", False, titleColor), (50, 50))
        # app.paint()
        pass

    def print_message(self, message, kind):
        """Print some messages."""
        if message is not None:
            messages[kind].append(message)

    def add_message(self, message, kind):
        """Add some messages."""
        messages[kind].append(message)
        if len(messages[kind]) > 50:
            messages[kind].pop(0)

    def flash_message(self, message, kind):
        # self.gui()
        self.print_message(message, kind)

    def print_spectrum(self, spectra):
        """Print mind wave spectrum."""
        global spectrum
        spectrum = spectra
        # for i in range(flen - 1):
        #     value = float(spectrum[i] * 1000)
        #     color = self.wave_color(i)
        #     pygame.draw.rect(
        #         self.window, color, (25 + i * 10, 400 - value, 5, value))

        pass

    def print_circle(self, position, value):
        """Print circle on screen."""
        # try:
        #     pygame.draw.circle(self.window, redColor, position, value)
        #     pygame.draw.circle(self.window, greenColor, position, 30, 1)
        #     pygame.draw.circle(self.window, greenColor, position, 50, 1)
        # except:
        #     return

        pass

    def print_waves(self, recorder):
        """Print word on screen."""
        global ys
        #ys=numpy.roll(ys,-1)
        ys = recorder.raw.values[-1*self.numPoints:]
        # pos_y = 650
        # self.print_message(None, None)
        # self.window.blit(font_20.render("Delta", False, deltaColor), (25,  pos_y))
        # self.window.blit(font_20.render("Theta", False, thetaColor), (50,  pos_y + 25))
        # self.window.blit(font_20.render("Alpha", False, alphaColor), (100, pos_y))
        # self.window.blit(font_20.render("Beta",  False, betaColor),  (150, pos_y + 25))
        # self.window.blit(font_20.render("Gamma", False, gammaColor), (350, pos_y))

        # pos_x = 650
        # pos_y = 200

        # self.graph(recorder)

        # """Print blink level."""
        # position = (pos_x, pos_y)
        # self.print_circle(position, int(recorder.blink[-1] / 2))
        # self.window.blit(blink_img, (pos_x - 20, pos_y + 60))

        # """Print meditation level."""
        # position = (pos_x + 150, pos_y)
        # self.print_circle(position, int(recorder.meditation[-1] / 2))
        # self.window.blit(meditation_img, (pos_x + 100, pos_y + 60))

        # """Print attention level."""
        # position = (pos_x + 300, pos_y)
        # self.print_circle(position, int(recorder.attention[-1] / 2))
        # self.window.blit(attention_img, (pos_x + 260, pos_y + 60))


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

    def plot_messages(self):
        global messages
        self.uiplot.bluetooth.setText("[Bluetooth]: %s" % self.substr(messages["bluetooth"]))
        self.uiplot.serial.setText("[Serial]: %s" % self.substr(messages["serial"]))
        self.uiplot.status.setText("[Errors]: %s" % self.substr(messages["status"]))
        self.uiplot.data.setText("[Data]: %s" % self.substr(messages["sser_data"]))

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
