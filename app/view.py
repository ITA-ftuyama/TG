#!/usr/bin/python
# -*- coding: utf-8 -*-
"""View."""
import gui
import sys
import numpy
import threading
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt


class View(object):
    numPoints=1000

    def __init__(self):
        """Initializes the View."""
        global xs, ys
        self.quit = False
        self.messages = {
            "bluetooth": [],
            "serial": [],
            "status": [],
            "sser_data": []
        }
        xs=numpy.arange(self.numPoints)
        ys=numpy.sin(3.14159*xs*10/self.numPoints) #this is our data
        self.run()

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
        self.c.attach(self.uiplot.qwtPlot) #attach it to the qwtPlot object
        self.uiplot.timer = QtCore.QTimer() #start a timer (to call replot events)
        self.uiplot.timer.start(10.0) #set the interval (in ms)
        self.win_plot.connect(self.uiplot.timer, QtCore.SIGNAL('timeout()'), self.plot)

        self.win_plot.show()
        sys.exit(self.app.exec_())

    def plot(self):
        global ys
        #ys=numpy.roll(ys,-1)
        self.c.setData(xs, ys)
        self.uiplot.qwtPlot.replot()

    def graph(self, recorder):
        """Print some graph."""
        # self.fig = plt.figure(1,figsize=(10,3), dpi=100)
        pass

    def gui(self):
        """Print some GUI."""
        # self.window.fill(backColor)
        # self.window.blit(font_32.render("Mindwave Controller", False, titleColor), (50, 50))
        # app.paint()
        pass

    def substr(self, messages):
        """Print cropped message."""
        msg = ", ".join(messages)
        return msg[-100:]

    def print_message(self, message, kind):
        """Print some messages."""
        # if message is not None:
        #     self.messages[kind].append(message)

        # self.window.blit(font_20.render(self.substr(self.messages["bluetooth"]),  False, blueColor),  (50, 100))
        # self.window.blit(font_20.render(self.substr(self.messages["serial"]),     False, redColor),   (50, 125))
        # self.window.blit(font_20.render(self.substr(self.messages["status"]),     False, whiteColor), (50, 150))
        # self.window.blit(font_14.render("Sent Serial: " + "; ".join(self.messages["sser_data"]),   False, redColor),   (50, 175))

        pass

    def add_message(self, message, kind):
        """Add some messages."""
        self.messages[kind].append(message)
        if len(self.messages[kind]) > 10:
            self.messages[kind].pop(0)

    def flash_message(self, message, kind):
        # self.gui()
        # self.print_message(message, kind)
        # pygame.display.update()

        pass


    def wave_color(self, freq):
        """Color according to the wave."""
        # if freq < 3:
        #     return deltaColor
        # elif freq < 8:
        #     return thetaColor
        # elif freq < 13:
        #     return alphaColor
        # elif freq < 30:
        #     return betaColor
        # else:
        #     return gammaColor
        return None

    def print_spectrum(self, spectrum, flen):
        """Print mind wave spectrum."""
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
