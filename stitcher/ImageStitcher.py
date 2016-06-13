#!/usr/bin/env python3

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os
import os.path

class ImageStitch:
    '''
    A class for organizing multiple images into a single image.
    requires:
        from PIL import Image
        from PIL import ImageFont
        from PIL import ImageDraw 
        import os
        import os.path
    '''
    def __init__(self, color = '#FFFFFF'):
        self.image_source_directory = './img/'
        self.font_source_directory  = './font/'
        self.font                   = 'Helvetica'
        self.titleSize              = 36            
        self.title                  = ''
        self.titleColor             = '#000000'
        self.graph_size             = (700, 400)
        self.background_color       = color
        self.graph                  = Image.new('RGB',
                                                self.graph_size,
                                                self.background_color)
        self.labels                 = []
        self.images                 = []
        self.number_images          = 0
        self.vert_space             = 5
        self.horz_space             = 5
        self.num_columns            = 1
    
    def _sortImages(self):
        '''
        Should only be called by the render() method.
        sortImages() is a bubble sort algorithm used to ensure images are
        in the correct order. 
        '''
        print("Sorting images...")

        index = 0
        isSorted = False
        changeMade = False

        while isSorted == False:
            # Ensure list index is within range
            if index == len(self.images) - 1:
                index = 0
                # reset changesMade
                changeMade = False

            # Assign number to current and next image depending on
            # prefixed number of the file name.
            if self.images[index].info['fileName'][1] == '_':
                currentImg = int(self.images[index].info['fileName'][0])
            else:
                currentImg = int(self.images[index].info['fileName'][:2])

            if self.images[index + 1].info['fileName'][1] == '_':
                nextImg    = int(self.images[index + 1].info['fileName'][0])
            else:
                nextImg    = int(self.images[index + 1].info['fileName'][:2])

            if currentImg > nextImg:
                # swap if necessary 
                self.images[index], self.images[index + 1] = \
                self.images[index + 1], self.images[index]
                changeMade = True

            index += 1

            # if no changes are made at end of list, then the list is sorted
            if index == len(self.images) - 1 and changeMade == False:
                isSorted = True

    def loadImages(self):
        '''
        Loads all images in specified directory.
        Naming convention for images in dir is prefix number 1 through 9,
        followed by an '_' underscore. 
        Use setImageDir() to set the dir of images.
        '''
        index = 0
        # crawl through files in current directory
        for img in os.listdir(self.image_source_directory):
            # load only if an image and for saftey ignore hidden files
            # and directorys that start with '.' 
            if os.path.isfile(self.image_source_directory + img) and\
            img[0] != '.':
                print('loading: {file}'.format(file=img))
                # open image
                if img[-3:] == 'png':
                    current_image = Image.open(self.image_source_directory +\
                                               img).convert('RGBA')
                else:
                    current_image = Image.open(self.image_source_directory +\
                                               img)
                # create a copy of the image to not edit the original
                self.images.append(current_image.copy())
                # give the image a name 
                self.images[index].info["fileName"] = img
                index += 1

        # assign number of images loaded
        self.number_images = len(self.images)
        if self.number_images == 0:
            print("WARNING: No images loaded, check your specified path.")
            return False
        else: 
            return True
    
    def _resizeImages(self):
        '''
        This method called by setSize()
        Images in a column should all be the same width and height.
        '''
        # sum of widths of a row of images
        sum_width = 0
        for i in range(0, self.num_columns):
            sum_width += self.images[i].width
            
        max_graph_space = self.graph_size[0] \
                        - self.vert_space \
                        - (self.vert_space*self.num_columns)
                
        max_img_width = max_graph_space/sum_width
        
        index = 0
        for img in self.images:
            self.images[index] = img.resize((int(img.width*max_img_width),
                                             int(img.height*max_img_width)))
            index += 1
    
    def render(self):
        '''
        Should be the second to last method called just before save().
        render() takes all the images and text specified, and pastes them
        into one image.  
        '''
        # Ensure the images are in order.
        self._sortImages()

        current_column = 1
        pos_x, pos_y = self.vert_space, self.horz_space
        # Draw the title if one exists
        if self.title != '':
            textImg = ImageDraw.Draw(self.graph)
            font    = ImageFont.truetype(self.font_source_directory, 
                                         self.titleSize)

            font_width  = textImg.textsize(self.title, font=font)[0]
            font_height = textImg.textsize(self.title, font=font)[1]

            pos_x       = (self.graph.width / 2) - (font_width / 2)
            textImg.text((pos_x, pos_y), self.title, self.titleColor, font=font)
            # Reset position after drawing title
            pos_y += (self.vert_space + font_height)
            pos_x = self.vert_space
        # Draw the images 
        for img in self.images:
            if img.info["fileName"][:2] == '1_':
                self.graph.paste(img, (int(pos_x), int(pos_y)))
                pos_x += int(self.vert_space + img.width)
            else:
                if current_column > self.num_columns:
                    pos_x = self.vert_space 
                    pos_y += (self.horz_space + img.height)
                    current_column = 1
                self.graph.paste(img, (int(pos_x), int(pos_y)))
                pos_x += (self.vert_space + img.width)
            current_column += 1
    
    def save(self, path, format = None):
        '''
        save() should be the last method called once all settings have been set.
        
        @param path should be a string specifying dir to save the file to.

        @param format is option to override auto formatting.
        If omitted, the format to use is determined from the filename extension.
        If a file object was used instead of a filename,
        this parameter should always be used.
        '''
        self.graph.save(path, format=format)

    def setImageDir(self, path):
        '''
        setImageDir() is used to set the directory to somthing other that the,
        default which is './img/'.

        @param path should be a string and a name of a file.
        '''
        self.image_source_directory = path
        
    def setTitle(self, title):
        # TODO: Add word wrap. 
        '''
        setTitle() is used to set the title of the image. If no title is set,
        there will be no caption at the top of the output image. Spacing at the
        top of the image will be set to horizontal space specified.

        @param title is the caption to be printed at top of the image. Should
        be a string.
        '''
        self.title = title
        
    def setTitleSize(self, size):
        '''
        setTitleSize() is used to set the size of the font. If none specified,
        default size will be used

        @param size should be an integer specifying size of font.
        '''
        self.titleSize = size

    def setTitleColor(self, color):
        '''
        setTitleColor() sets the color of the text at top of image.

        @param color should be a string in hexadecimal format of - '#FFFFFF'
        '''
        self.titleColor = color
    
    def setLabels(self, labels):
        '''
        setLabels() currently has no function. Future use will be to add
        captions to the images pasted.

        @param labels should be a list of captions in the order the images
        were read in.
        '''
        self.labels = labels
    
    def setFont(self, font):
        '''
        setFont() currently has no function.

        @param font
        '''
        self.font = font
        
    def setFontPath(self, path):
        '''
        setFontPath() sets the path the font will be pulled from. Convention is
        to save fonts in a sub-dir called font.

        @param should be a string specifying the path to the font to be used.
        '''
        self.font_source_directory = path

    def setColumns(self, number_columns):
        '''
        setColumns() sets the number of columns the output image should have.

        @param number_columns should be an integer specifying the number of 
        columns to be used.
        '''
        self.num_columns = number_columns

    def setSize(self, width=700):
        '''
        setSize() sets the width and height of the output image. Should always
        be called after loading the images and optionally specifying the title.

        @param width should and integer specifying how many pixels wide the 
        output image should be.  
        '''
        self.graph_size = (width, 400)
        self._resizeImages()
        self.graph_size = (width, self._getHeight())
        self.graph = self.graph.resize(self.graph_size)
        
    def _getHeight(self):
        '''
        _getHeight() called by setSize()
        '''
        height = self.horz_space
        if self.title != '':
            textImg = ImageDraw.Draw(self.graph)
            font = ImageFont.truetype(self.font_source_directory, 
                                      self.titleSize)
            font_height = textImg.textsize(self.title, font=font)[1]
            height += self.horz_space + font_height
        rows = round(self.number_images/self.num_columns)
        height += self.horz_space*rows
        height += self.images[0].height*rows
        return height
    
    def setImageSpacing(self, line_spacing):
        '''
        setImageSpacing() sets the vertical | and horizontal -- spacing.

        @param line_spacing is a two tuple contining two integers,
        (vertical spacing, horizonal spacing)
        '''
        self.vert_space = line_spacing[0]
        self.horz_space = line_spacing[1]
    
