To test the headset:
0. Make sure it is paired with your computer:
	a. The LED light on the headset indicate the following:
		1.  off - headset is not turned on.
		2.  double blink blue: ready to be paired with computer.
		3.  solid red: unpaired.
		4.  single blinking blue: paired and ready to be used.
		5.  double blinking red: low battery.
	b.  To pair: hold the on/off switch past the on position for 3 seconds.
	c.  To forget pairing: hold on/off switch past on for 6+ seconds.  Headset stores maximum of
		three computers it is paired with.

If you have the black headset, it must be paired with Bluetooth (the white one uses a USB adapter, 
not bluetooth).  If you have the white headset, consult the Manual 
(http://developer.neurosky.com/docs/lib/exe/fetch.php?media=mindwave_user_guide_en.pdf)
to set up the USB adapter, and also here: http://developer.neurosky.com/docs/doku.php?id=mindwave.

If you cannot pair the device with your computer you might need to configure Bluetooth (black
headset) or reinstall the USB adapter drivers (white headset).  See the
User's Guide, Appendix 5.

1. Turn it on.  Place it on your head.
2. Click on TestHeadset.exe in this folder.
3. Click on start.
4. Wait for the "finished" line.
5. Click on "copy to clipboard" button.
6. Paste the data into email to me (CNTL_V), fredm73@gmail.com if you did not connect to the app. with the headset.
7. If a pop-up window with a stack trace happens, do a CNTL-C in the window and then a CTL-V in email to me.

There are known problems with Windows 8/10 and the headsets (both Mindwave and Mindwave Mobile).  
Sometimes NeuroExperimenter fails to connect to the headset, and yet this test app. is successful.
Please read the Users' Guide (click on "help" tab in NeuroExperimenter) for instructions on fixing
NEx on Windows 8/10.  See the Appendix 5.

If the test is successful, it alters the 
<portUsed>COM5</portUsed>
to the correct port (as described in the Users' Guide for NEx).  So, you should not have to do that yourself.

The output from a successful test looks like:
------------------------------------
Startup: 6/22/2015 5:56 PM
OS: Microsoft Windows 7 Home Premium 
Framework: v4.0.30319
ThinkGear.dll: 2.8.4892.19806
Ports:
	COM4 - Standard Serial over Bluetooth link (COM4)
	COM3 - Standard Serial over Bluetooth link (COM3)
Validating: 
Device found on: COM3
Port fix: start up port was ok: COM3
good signal achieved
good signal achieved
good signal achieved
good signal achieved
good signal achieved
good signal achieved
Finished: 5:56 PM
-----------------------------------

The bottom line: you need to get TestHeadSet working before NeuroExperimenter has a chance
of working. Failure of TestHeadSet is almost certainly a problem with the installation of
the Bluetooth (black headset) or USB Adapter driver (white headset).  Use the NeuroSky
Manuals and other resources to resolve the problem.  You can contact me, at 
fredm73@gmail.com, if you wish.