# image-stitcher

A python library and exec script for stitching multiple images neatly into one image file.

## Overview

image-stitcher is a python class that makes use of [Pillow][link to pillow] to stitch together multiple images neatly into one image file.

**ADD IMAGE FOR EXAMPLE HERE**

---

# Stitch

---

## Overview

Stitch is a stand alone exec program that was created using the Image-Stitcher module. PyInstaller was used to create the executable.

## Installation

1. [Download or clone here](https://github.com/brag4918/image-stitcher)

2. Open the dir image-stitcher/stitcher/dist

3. You must copy the stitch exec (located in above directory) file into your `/Users/User/bin/` directory (replace User with your user name).

## Project Setup

### Directory Structure

Your project should have a main directory. Name this whatever you want. For Example 'MyProject'.

Inside your project directory you should have two things.
1. A directory by default called 'img'. This 'img' directory will hold all of the images you plan to stitch into your final image. You can change the name of this directory to anything you would like, but you must set the option 'img_path' in your config file to the desired name of your directory (more on that under config.yaml).
2. A file named config.yaml to store the settings for your output/final image.


```
- MyProject
		   \
		  - img
		  - config.yaml
```

### config.yaml

The purpose of the config.yaml file is to store settings and other data that stitch needs to know in order to create your desired output.

Most of the options are not required and have a default value set. 

Here are all of the possible options **(some are required and are noted with a * and bolded)** with a brief description of what the option does.

Options:

- title
	- Title of the figure as a string (i.e. `'Figure 1.'`).
- title_color
	- Color of the title in hex stored as a string (i.e. `'#FFFFFF'`)
- title_size
	- Font size of the title as an integer (i.e `38`)
- labels
	- An array of strings that label the top of each column (i.e. `['col1', 'col2', 'col3']`)
- label_size
	- Font size of the labels as an integer (i.e `38`).
- color_labels
	- Colored boxes used to visually label a row. Appear on the left of the rows. Should be an array of strings containing hex values for each box (i.e. `['#FFFFFF', '#FF00FF', '#00FFFF']`).
- background_color
	- Color of the background of the final image in hex form (i.e `'#FFFFFF'`)
- __*columns__
	- Number of columns
- vertical_space
	- The amount of vertical space between the columns as an integer (i.e `3`). 
- horizontal_space
	- The amount of horizontal space between the columns as an integer (i.e `3`).
- __*output_path__
	- The location of the directory the output image should be written to relative to the location of the config.yaml file (i.e `'./output/'`).
- __*output_name__
	- Name of the final image (i.e `'Figure1'`).
- img_path
	- path to the directory containing your images relative to your config.yaml file (i.e `'./img'`).
- __*width__
	- Width of your final output image in pixels (i.e. `1000`). Recommended/default at 1000.

Example config.yaml file:

```
title: 'Figure 2.'
title_color: '#000000'
labels: ['Y-SED', 'O-SED', 'O-AEx']
background_color: '#FFFFFF'
columns: 3
vertical_space: 3
horizontal_space: 3
output_path: "./"
output_name: "Figure2.jpg"
img_path: "./img/"
title_size: 50
label_size: 38
width: 1000
color_labels: ['#a77a00', '#e63b7a', '#00f900', '#ffb5af', '#919191']
```

#### Image Naming Scheme

stitch can compose up to 99 images into one final image. For stitch to know how to order your images, you must use the naming scheme of "number"_"name of your image".jpg/png.

stitch will read in the images and write them to your final image from left to right, top to bottom.
In the config file, you should specify how many columns you want in your final image. An example of this would be if you have six images total (they should be named prefixed with 1\_, 2\_, 3\_...6\_) and you want two columns. The solution would be to set the option columns to 2 (i.e. `columns: 2`). This will give you two columns and three rows.

Example:

```
- MyProject
           \
          - img
               \
                1_firstImage.jpg
                2_secondImage.jpg
                3_thirdImage.jpg
                ...(4,5,6,7,8,9)
                10_tenthImage.jpg
                11_eleventhImage.jpg
          - config.yaml
```  

## Usage In Terminal

`stitch path/to/your/project/directory`

## Integration With R / R Studio

For some reason, within R Studio, using just `system('stitch')` does not work. R Studio wants to know exactly where the program lives, so the fix for now is as below.

`system('~/bin/stitch path/to/your/project/directory')`

---

#### TODO

- Finish this README

- ~~Add compatibility for .png or other files that contain transparency.~~ Done

- Find bug where certain .png images with transparent backgrounds dont load properly. 

- ~~Add support for more than 9 images.~~ Done (now supports up to 99 images)

- ~~Add documentation for using the ImageStitcher module.~~ Done

- Add examples of how to set up folder and config.yaml file. 

- Create getter methods for the ImageStitcher module/class.

- Set variables in ImageStitcher module/class to protected. 

[link to pillow]: http://pillow.readthedocs.io/en/3.1.x/index.html 