# tobii_pro_wrapperProject Title

Contains TobiiHelper class and helpful functions for working with with the new Tobii Pro SDK v 1.0 for Python, 
along with essential eye-tracking routines. 

Currently provides all functionality for running a FULL CALIBRATION 
ROUTINE for 5 and 9 point calibrations, and converting between Tobii
Trackbox, Tobii ADA, and Psychopy coordinate systems. 

This code also contains functionality for finding/calibrating the 
experimental monitor, selecting and connecting to a tobii device, 
getting tobii device coordinates, and receiving
real time gaze and eye position data from the tobii tracker. 

## Getting Started

### Prerequisites
Running tobii_pro_wrapper requires all of the following and their dependencies. 

* ([Python 2.7](https://www.continuum.io/downloads))
* ([Tobii Pro SDK v1.0](https://www.tobiipro.com/product-listing/tobii-pro-sdk/#Download)) for Python 

The Tobii Pro SDK v1.1 currently has bugs that prevent some eyetracker models from calibrating. Once 
this is fixed, tobii_pro_wrapper will be updated to work with the newer SDK releases. So to 
download the previous version, use:

```
pip install tobii_research==1.0.1.128  
```

* ([Psychopy](http://psychopy.org/installation.html))
* ([numpy](https://scipy.org/install.html))
* ([scipy](https://scipy.org/install.html))
* gtk, ([pygtk](http://www.pygtk.org/downloads.html))

### Installing

To download without installing Git, run: 

```
pip install https://github.com/oguayasa/tobii_pro_wrapper/tarball/master
```
or 
```
pip install https://github.com/oguayasa/tobii_pro_wrapper/zipball/master
```
Depending on your device security, you may either need to implement ' --user '
after the 'install' command and before the github website, or run your command line
program 'as administrator' and then navigate to your user account, or both. 

```
pip install --user https://github.com/oguayasa/tobii_pro_wrapper/zipball/master
```

You could also install by downloading the .zip file, and extracting the contents to
the site-packages folder of your working Python 2.7 installation.


End with an example of getting some data out of the system or using it for a little demo

## Package Details

### findTracker(serialString = None)
Find and connect to the eyetracker identified by its serial number.
If no serial number is given, defaults to connecting to the first eyetracker it can find.

### getTrackerSpace()
Gets the trackbox and Active Display Area coordinates for the eyetracker found with
findTracker.

### setMonitor(nameString = None, dimensions = None)
Creates, selects, and calibrates a psychopy.monitor object. You can select a specific
monitor with **nameString** and set its dimensions with **dimensions**. If no **nameString** or 
**dimensions** are given, it will use the default monitor and that monitors dimensions.

### startGazeData()
Connect to the eyetracker and start broadcasting all gaze data as a dictionary.

### getGazeData()
Takes the gaze data dictionary specified by Tobii, pulls out key values, and converts
those values to more readily understood measurements. 

Returns a single row (current sample) dictionary with gaze positions, eye positions,
pupil size, and eye validities. 

### stopGazeData()
Disconnect from the eyetracker and stop broadcasting gaze data.

### startSyncData()


### stopSyncData()

### tb2Ada(xyCoor = tuple)

### tb2PsychoNorm(xyCoor = tuple)

### ada2PsychoWin(xyCoor = tuple)

### ada2MonPix(xyCoor = tuple)

### getAvgGazePos(serialString = None)

### getAvgEyePos(serialString = None)

### getAvgEyeDist(serialString = None)

### getPupilSize()

### checkEyeValidities()

### runValidation(pointDict = dict)

### runTrackBox()

### runFullCalibration(numCalibPoints = int())

## Examples

To find the eyetracker, determing eyetracker coordinatest, define the experimental monitor, 
and run a full 5-point calibration routine:

```
# Import the wrapper
import tobii_pro_wrapper as tpw

# Create a TobiiHelper object
foo = tpw.TobiiHelper()

# Idenfity and define the experimental monitor
foo.setMonitor(nameString = None, dimensions = None)

# Find eyetrackers and connect
foo.findTracker(serialString = None)

# Determine the coordinates for the eyetracker's 
# tracking spaces (trackbox and active display area)
foo.getTrackerSpace()

# Run a full 5 point calibration routing
foo.runFullCalibration(numCalibPoints = 5)

```

To start, output, and stop the eyetracker's collection of gaze data:

```
# start the eyetracker
foo.startGazeData()

# to get real time gaze data, place this command within a "while" loop 
# during each trial run
foo.getCurrentData()

# stop the eyetracker
foo.stopGazeData()

```

That's it!

Further examples will be linked below as they are developed.

## Contributing

To report bugs, contribute changes, ask questions, or request additional functionality, please drop
an e-mail to oguayasa@gmail.com with "CONTRIBUTING to Tobii Wrapper" in the subject line. 

## Authors

**Olivia Guayasamin** - *Initial work and development* - [oguayasa](https://github.com/oguayasa)

Also see additional [contributors](https://github.com/oguayasa/tobii_pro_wrapper/contributors).

## License

This project is licensed under the Apache 2.0 - see the file for details

## Acknowledgments

* A big thanks to those who create and maintain [Psychopy](http://www.psychopy.org/about/index.html)
* Inspired by Jan Freyberg's [wrapper](https://github.com/janfreyberg/tobii-psychopy) for the previous Tobii Analytics SDK
* [Quentin Caudron](https://github.com/QCaudron) for helping this n00b figure out how to develop Python software.


