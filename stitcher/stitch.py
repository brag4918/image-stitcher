#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import yaml
import os, os.path
import ImageStitcher

def main():

	configFile     = open('./config.yaml', 'r')
	configContents = configFile.read()
	configFile.close()

	config = yaml.load(configContents)

	myImage = ImageStitcher.ImageStitch(config["background_color"])

	try: myImage.setImageDir(config["img_path"])
	except: pass

	if myImage.loadImages() != True: return 1

	try: myImage.setTitle(config["title"])
	except: pass

	try: myImage.setTitleColor(config['title_color'])
	except: pass

	try: myImage.setFontDir(config["font_path"])
	except: pass

	try: myImage.setTitleSize(config['title_size'])
	except: pass

	try: myImage.setColumns(config['columns'])
	except: pass

	try: myImage.setImageSpacing((config['vertical_space'],
								  config['horizontal_space']))
	except: pass
	
	try: myImage.setWidth(config["width"])
	except: myImage.setWidth()
	
	myImage.render()
	
	myImage.save(config['output_path']+config['output_name'], "jpeg")


if __name__ == '__main__':
	main()