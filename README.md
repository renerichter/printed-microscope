# disMicro - a disposeable 3D printed Microscope project
Here we are going to present our work, efforts and results on the 3d-printed microscope while realizing various approaches. The aim is to build a functional high-resolution microscope, which is not only fast, but stable, cheap and disposable.  

## Getting Started

The idea of our project itself is based on the fabulous work of Richard W. Bowman (link) and his crew. [Paper](https://www.repository.cam.ac.uk/handle/1810/253365)
 
### Printing and Assembling the Microscope: 
- [Printable-Files and Documentation](https://github.com/rwb27/openflexure_microscope#kits-and-license) 
- [Assembling on easy Example](http://docubricks.com/viewer.jsp?id=1044562654723960832)

If you - like us - feel the temptation to change the designs to your special needs, you can open and edit them using the following tools: 
- [OpenSCAD](http://www.openscad.org/) > programmable CAD
- [CGAL](http://www.cgal.org/) > Geometric Algorithms  
- [Slic3r](http://slic3r.org/) > Generates G-Code to used with 3D printers
- [FreeCAD](http://www.freecadweb.org/wiki/?title=Download) > to provide a portability to commercial-tools like Inventor (e.G. STEP), but in our case didn't work well yet

The University of Cambridge hosts the [OpenLabTools](http://www.openlabtools.org/) project, which provides interesting new Designs for use with e.g. 3Dprinted Microscopes. 

For Printing our own parts, we use the [Ultimaker 2+](https://ultimaker.com/en/products/ultimaker-2-plus) with it's software [Cura](https://ultimaker.com/en/products/cura-software).


To drive the microscope automatically attaching motors to it is the method of choice. We decided to use the following modell:
<LINK?>

## Project One - disWiFi (disposable Widefield) System Calibration and Bio-Samples
Our first project is based on reconstructing the work as presented by Richard W. Bowman et Al. Hereby the originally used lens of the Raspberry-PiCam shall be compared to different objectives.

### ToDo
| Snehal  				| Elsie 			| Scott					|
| ------------- 			| ------------- 		| ------------- 			|
| - [x] Damping/Attenuation  		| - [] Calibration / Improv.	| - [] Code for Image-Acquisition	|
| - [ ] Vibr.Analysis  			| - [] Testing diff. Samples  	| - [] Documentation			|
| - [ ] Redesign of Parts in Inventor  	| - [] Comparison Elyra/Confocal| 					|
| - [ ] Documentation		 	| - [] Documentation		|  					|

### The Setup
The Setup hence consists out of the following parts and all necesarry files can be found in the subfoulder <name>. 

### Analysis and Calibration
Additionally different analysis where done to clarify the different stability parameters of the system. 

<Vibrational Analysis @Snehal, Elsie>

### Sample-Measurements and Comparison

The basic Code to drive the motors is contained in the libraries of project two. 

## Project Two - disConfo (disposable Confocal) Setting up and GUI
Our second aim is to take the imaging capabilities of such a system to a new level and realize a simple, cheap, but yet stable and reliable confocal imaging system. The necessary Code is written in Python and contained in the subfolder...

| Snehal  				| Elsie 			| Scott					|
| ------------- 			| ------------- 		| ------------- 			|
| - [] Damping/Attenuation  		| - [] Calibration  		| - [] Setting final setup together	|
| - [] Vibr.Analysis  			| - [] Testing diff. Samples  	| - [] Code for Image-Acquisition	|
| - [] Redesign of Parts in Inventor  	| - [] Comparison Elyra/WF	| - [] Improvements			|
| - [] Documentation		 	| - [] Documentation		| - [] Documentation			|

MotorControl.py is used to control the stepper motors that control the stage motion. 
In it, a 3D scanning method is implemented to scan through a defined 3D region at a particular speed.
After the 3D scanning method is calibrated to the microscope, an image processing method will be needed to turn the individual points taken by the confocal sample scanning into a real image.


## About the Group
We:

| Role 			| Person 		| Contact	|
| ----			| ----			|	---	|
| PhD-stud. 		| René Richter  	| 303 		|
| DIng.Eng.		| Robert Kretschmer   	| 303 		|
| Internship(ASP) 	| Scott Stratchan   	| 303 		|
| Internship(ASP) 	| Elsie Quansah   	| 432 		|
| Pract.-Lab.(FH) 	| Snehal Chaitanya   	| 432 		|

 are part of the [AG Heintzmann](https://sites.google.com/site/nanoimagingproject/) at the [Leibniz Institute of Photonic Technologies Jena](http://www.ipht-jena.de/) and the [Friedrich-Schiller-Universtity Jena](https://www.uni-jena.de/). 





