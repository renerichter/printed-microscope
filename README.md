# printed-microscope
Here we are going to present our work, efforts and results on the 3d-printed microscope while realizing various approaches. The aim is to build a functional high-resolution microscope, which is not only fast, but stable, cheap and disposable.  

Getting Started

The idea of our project itself is based on the fabulous work of Richard W. Bowman (link) and his crew.
<Cite Paper etc>
 
Printing and Assembling the Microscope: 
Printable-Files and Documentation > https://github.com/rwb27/openflexure_microscope#kits-and-license 
Assembling on easy Example > http://docubricks.com/viewer.jsp?id=1044562654723960832

If you, like us, feel the temptation to change the Designs to your special needs, you can open them in according tools. 
OpenSCAD > http://www.openscad.org/
Supporting tools for openSCAD > 
CGAL > Geometric Algorithms : http://www.cgal.org/
Slic3r > Generates G-Code to used with 3D printers > http://slic3r.org/
FREECAD > http://www.freecadweb.org/wiki/?title=Download (to provide a portability to tools like Inventor (e.G. STEP) > didn't work well yet)

The University of Cambridge hosts the OpenLabTools project, which provides interesting new Designs for use with e.g. 3Dprinted Microscopes. 
http://www.openlabtools.org/

For Printing our own parts, we use the Ultimaker Pro 2 Extended () with it's software Cura.
https://ultimaker.com/en/products/cura-software

To drive the microscope automatically attaching motors to it is the method of choice. We decided to use the following modell:
<LINK?>

Project One - disWiFi (disposable Widefield) System Calibration and Bio-Samples
Our first project is based on reconstructing the work as presented by Richard W. Bowman et Al. Hereby the originally used lens of the Raspberry-PiCam shall be compared to different objectives.

The Setup hence consists out of the following parts and all necesarry files can be found in the subfoulder <name>. 

Additionally different analysis where done to clarify the different stability parameters of the system. 

<Vibrational Analysis @Scott, Elsie>

<IMAGES...> @Elsie

The basic Code to drive the motors is contained in the libraries of project two. 

Project Two - disConfo (disposable Confocal) Setting up and GUI
Our second aim is to take the imaging capabilities of such a system to a new level and realize a simple, cheap, but yet stable and reliable confocal imaging system. The necessary Code is written in Python and contained in the subfolder...

Documentation@Scott

MotorControl.py is used to control the stepper motors that control the stage motion. 
In it, a 3D scanning method is implemented to scan through a defined 3D region at a particular speed.
After the 3D scanning method is calibrated to the microscope, an image processing method will be needed to turn the individual points taken by the confocal sample scanning into a real image.








