#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import yaml
import sys
import os
import os.path
import ImageStitcher

def main():
	pathToFile = '.'

	try: pathToFile = sys.argv[1]
	except:
		print('Usage: ./stitch.py path/to/file')
		return 1

	os.chdir(pathToFile)
	configFile     = open(pathToFile + '/config.yaml', 'r')
	configContents = configFile.read()
	configFile.close()

	config = yaml.load(configContents)

	myImage = ImageStitcher.ImageStitch(config["background_color"])

	try: myImage.setImageDir(config["img_path"])
	except: pass

	if myImage.loadImages() != True: return 1

	try: myImage.setTitle(config["title"])
	except: pass

	try: myImage.setLabels(config["labels"])
	except: pass

	try: myImage.setTitleColor(config['title_color'])
	except: pass

	try: myImage.setFontPath(config["font_path"])
	except: pass

	try: myImage.setTitleSize(config['title_size'])
	except: pass

	try: myImage.setLabelSize(config['label_size'])
	except: pass

	try: myImage.setColumns(config['columns'])
	except: pass

	try: myImage.setColorLabels(config['color_labels'])
	except: pass

	try: myImage.setColorLabelWidth(config['color_label_width'])
	except: pass

	try: myImage.setImageSpacing((config['vertical_space'],
								  config['horizontal_space']))
	except: pass
	
	try: myImage.setSize(config["width"])
	except: myImage.setSize()
	
	myImage.render()
	
	myImage.save(config['output_path']+config['output_name'], "jpeg")


if __name__ == '__main__':
	main()