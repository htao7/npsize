# npsize
nanoparticle size measurement

This program is for NP size measurement from Hitachi HT 7700 TEM images. 

To use the program, put images in a folder starting with "sphere/cube/rod" and run npsize_multi.py. The program will open all the jpg/tif 
files and measures the average size of the particles (radius for spheres (to be developed), edge length for cubes, width and height for rods). The particles measured will be highlighted with green rectangles. Press 'n' on keyboard to open the next image. Press 'Esc' to quit.

Manual adjustments:
1. Use the trackbar on top to change the size of the binding rectangles for more precise measurements.
2. Enlarge part of the image by dragging on the original image.
3. Set the standard for desired NPs in the 'Findxxx' functions. 
