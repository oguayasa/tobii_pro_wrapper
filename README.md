# tobii_pro_wrapper

Contains TobiiHelper class and helpful functions for working with with the new Tobii Pro SDK v 1.0 for Python, 
along with essential eye-tracking routines. 

Currently provides all functionality for running a FULL CALIBRATION 
ROUTINE for 5 and 9 point calibrations, and converting between Tobii
Trackbox, Tobii ADA, and Psychopy coordinate systems. 

This code also contains functionality for finding/calibrating the 
experimental monitor, selecting and connecting to a tobii device, 
getting tobii device coordinates, and receiving
real time gaze and eye position data from the tobii tracker. 

Requires Python 2.7 (SDK required), all dependencies for
Tobii Pro SDK 1.0.1 (tobii_research==1.0.1.128) for Python, and all dependencies
for Psychopy, Psychopy.iohub, numpy, scipy, and pygtk. The Tobii Pro SDK v1.1
currently has bugs that prevent some eyetracker models from calibrating. Once 
this is fixed, tobii_pro_wrapper will be updated to work with the newer SDK releases.

To download without installing Git, run: 

pip install https://github.com/oguayasa/tobii_pro_wrapper/tarball/master

or 

pip install https://github.com/oguayasa/tobii_pro_wrapper/zipball/master

Depending on your device security, you may either need to implement ' --user '
after the 'install' command and before the github website, or run your command line
program 'as administrator' and then navigate to your user account, or both. 

See tobii_pro_wrapper.py for more details. 

Example to find eyetracker, calibrate tracker coordinates and experimental monitor, 
and run a full 5-point calibration routine:

import tobii_pro_wrapper as tpw

foo = tpw.TobiiHelper()
foo.setMonitor()
foo.findTracker()
foo.getTrackerSpace()
foo.runFullCalibration(5)


That's it!
