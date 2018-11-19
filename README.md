# npsize
nanoparticle size measurement

This program is for NP size measurement from Hitachi HT 7700 TEM images. 

To use the program, download the 'mag' folder and 'npsize_multi.py'. Put images in a folder starting with "sphere/cube/rod" and run npsize_multi.py. The program will open all the jpg/tif  files and measures the average size of the particles (radius for spheres, edge length for cubes, width and height for rods). The particles measured will be highlighted with green rectangles/circles and index number. Press 'n' on keyboard to open the next image. Press 'Esc' to quit. After finishing, all the labelled NP images and the corresponding measurements will be recorded in newly generated files.

Manual adjustments:
1. Use the trackbar on top to change the size of the binding shapes for more precise measurements.
2. Enlarge part of the image by dragging on the original image.
3. Set the standard for desired NPs in the 'Findxxx' functions. 
