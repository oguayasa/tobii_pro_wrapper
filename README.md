# tobii_pro_wrapper

Contains functions for working with with the new Tobii Pro SDK v1.0 for Python, 
along with essential eye-tracking routines, in a TobiiHelper class.

Pretty much everything you need to connect to a Tobii eyetracker, calibrate the eyetracker,
get gaze, eye, and time synchronization data from the eyetracker device, and convert the confusing Tobii
coordinate systems units to units that are psychopy and interpretation friendly.

## Getting Started

### Prerequisites
Running tobii_pro_wrapper requires all of the following and their dependencies. 

* [Python 2.7](https://www.continuum.io/downloads)
* [Tobii Pro SDK v1.0](https://www.tobiipro.com/product-listing/tobii-pro-sdk/#Download) for Python 

At the time of this writing, Tobii Pro SDK v1.1 has bugs that prevent some eyetracker models from calibrating. Once 
this is fixed (I'll keep checking), tobii_pro_wrapper will be updated to work with the newer SDK releases. So to 
download the previous version, use:

```
pip install tobii_research==1.0.1.128  
```

* [Psychopy](http://psychopy.org/installation.html)
* [numpy](https://scipy.org/install.html)
* [scipy](https://scipy.org/install.html)
* [pygtk](http://www.pygtk.org/downloads.html)

### Installing

**To download without installing Git**, run:

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
**If you already have a working Git installation**, run:

```
pip install git+user https://github.com/oguayasa/tobii_pro_wrapper.git
```

*You could also install by downloading the .zip file, and extracting the contents to
the site-packages folder of your working Python 2.7 installation.*

## Package Details

### TobiiHelper() *class*
A class for a wrapper for the Tobii Pro SDK for Python. Contains the following attributes:

```
        self.eyetracker = None
        
        self.adaCoordinates = {}
        
        self.tbCoordinates = {}
        
        self.calibration = None
        
        self.tracking = False
        
        self.win = None
                
        self.gazeData = {}
        
        self.syncData = {}
        
        self.currentOutData = {}
```

### findTracker(serialString = None)
Find and connect to the eyetracker identified by its serial number.
If no serial number is given, defaults to connecting to the first eyetracker it can find.
Sets the self.eyetracker attribute.

### getTrackerSpace()
Gets the trackbox and Active Display Area coordinates for the eyetracker found with
findTracker. Sets the self.adaCoordinates and self.tbCoordinates attributes.

### setMonitor(nameString = None, dimensions = None)
Creates, selects, and calibrates a psychopy.monitor object. You can select a specific
monitor with **nameString** and set its dimensions with **dimensions**. If no **nameString** or 
**dimensions** are given, it will use the default monitor and that monitors dimensions. Sets the
self.win attributes

### startGazeData()
Connect to the eyetracker and uses the **self.gazeData** attribute to
broadcast all gaze data as a dictionary.

### getGazeData()
Takes the gaze data dictionary specified by Tobii (self.gazeData), pulls out important values, and converts
those values to more readily understood measurements. 

Returns a single row (current sample) dictionary with gaze positions, eye positions,
pupil size, and eye validities. 

### stopGazeData()
Disconnect from the eyetracker and stops broadcasting gaze data.

### startSyncData()
Connect to the internal clocks of eyetracker and computer devices,  and uses the **self.sycnData** attribute 
to broadcast internal clock values.

### stopSyncData()
Disconnet from eyetracker and stop broadcasting sync data. 

### tb2Ada(xyCoor = tuple)
Takes trackbox location coordinates and converts to active display area coordinates. Returns an (x,y)
coordinate tuple. 

### tb2PsychoNorm(xyCoor = tuple)
Takes trackbox location coordinates and converts psychopy window normal units. Returns an (x,y)
coordinate tuple. 

### ada2PsychoWin(xyCoor = tuple)
Takes active display area coordinates and converts psychopy window pixel units. Returns an (x,y)
coordinate tuple. 

### ada2MonPix(xyCoor = tuple)
Takes active display area coordinates and converts to monitor pixel coordinates. Returns an (x,y)
coordinate tuple. 

### getAvgGazePos()
Uses broadcasting **self.gazeData** to return the average (x,y) gaze position of the left and right eyes as a
tuple. Gaze position is returned in active display area units.

### getAvgEyePos()
Uses broadcasting **self.gazeData** to return the average 3D (x, y, z) physical position of the left and right 
eyes relative to the eyetracker origin as a tuple. Returns position in mm units. 

### getAvgEyeDist()
Uses broadcasting **self.gazeData** and **self.getAvgEyePos()** to return average distance of the left and right eyes
from the eyetracker origin. Retures position in cm units.

### getPupilSize()
Uses broadcasting **self.gazeData** to return average pupil size of left and right eyes as a tuple. Returns
pupil diameter in mm units.

### checkEyeValidities()
Uses broadcasting **self.gazeData** to return the validities of both eyes. Returns integer values of 0, 1, 2, or 3
depending on if no eyes were found, left eye was found, right eye was found, or both eyes are found respectively.

### runValidation(pointDict = dict)
Shows real time gaze position and draws several reference points (**pointDict** is a dictionary with numbered keys
and coordinate values for drawing those points) to check calibration quality. If no value for **pointDict** is given,
reference points will be drawn at the standard locations for a 5 point calibration.

### runTrackBox()
Shows real time eye position within in the Tobii eyetracker trackbox. Uses colors and reported eye distance to let
the subject know if they are well positioned relative to the tracker.

### runFullCalibration(numCalibPoints = int())
Runs a full 5 or 9 point calibration routine as specified by **numCalibPoints**. If **numCalibPoints** is not defined,
then the default is a 9 point calibration. This full calibration routine includes: finding eye positions within the trackbox,
running a calibration, showing calibration accuracy, re-calibrating problem points, checking the quality of the calibration, and
saving the calibration to the eyetracker. Requires a working keyboard to control. 

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

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/oguayasa/tobii_pro_wrapper/blob/master/LICENSE.txt) file for details.

## Acknowledgments

* A big thanks to those who create and maintain [Psychopy](http://www.psychopy.org/about/index.html)
* Inspired by Jan Freyberg's [wrapper](https://github.com/janfreyberg/tobii-psychopy) for the previous Tobii Analytics SDK
* [Quentin Caudron](https://github.com/QCaudron) for helping this n00b figure out how to develop Python software.


