from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import os, os.path

class ImageStitch:
    '''
    A class for organizing multiple images into a single image.
    requires:
        from PIL import Image
        from PIL import ImageFont
        from PIL import ImageDraw 
        import os, os.path
    '''
    def __init__(self, color = '#000000'):
        self.image_source_directory = './img/'
        self.font_source_directory  = './font/'
        self.font                   = 'Helvetica'
        self.titleSize              = 36            
        self.title                  = ''
        self.titleColor             = (0, 0, 0)
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
        
    def loadImages(self):
        index = 0
        # crawl through files in current directory
        for img in os.listdir(self.image_source_directory):
            # load only if an image and for saftey ignore hidden files
            # and directorys that start with '.' 
            if os.path.isfile(self.image_source_directory + img) and\
            img[0] != '.':
                # open image
                current_image = Image.open(self.image_source_directory + img)
                # create a copy of the image to not edit the original
                self.images.append(current_image.copy())
                # give the image a name 
                self.images[index].info["fileName"] = img
                index += 1

        # assign number of images loaded
        self.number_images = len(self.images)
        if self.number_images == 0:
            print("WARNING: no images loaded")
            return False
        else: return True
    
    def resizeImages(self):
        # sum of widths of a row of images
        sum_width = self.images[0].width * self.num_columns
            
        max_graph_space = self.graph_size[0] -\
                          self.vert_space -\
                          (self.vert_space * self.num_columns)
                
        max_img_width = max_graph_space / sum_width
        
        index = 0
        for img in self.images:
            self.images[index] = img.resize((int(img.width*max_img_width),
                                             int(img.height*max_img_width)))
            index += 1
    
    def render(self):
        current_column = 1
        pos_x, pos_y = self.vert_space, self.horz_space
        
        if self.title != '':
            textImg = ImageDraw.Draw(self.graph)
            font    = ImageFont.truetype(self.font_source_directory, 
                                         self.titleSize)
            font_width  = textImg.textsize(self.title, font=font)[0]
            font_height = textImg.textsize(self.title, font=font)[1]
            pos_x       = (self.graph.width / 2) - (font_width / 2)
            textImg.text((pos_x, pos_y), self.title, self.titleColor, font=font)
            pos_y += (self.vert_space + font_height)

        pos_x = self.vert_space

        for img in self.images:
            if img.info["fileName"][0] == '1':
                self.graph.paste(img,(int(pos_x), int(pos_y)))
                pos_x += int(self.vert_space + img.width)
            else:
                if current_column > self.num_columns:
                    pos_x = self.vert_space 
                    pos_y += (self.horz_space + img.height)
                    current_column = 1
                self.graph.paste(img, (int(pos_x) , int(pos_y)))
                pos_x += (self.vert_space + img.width)
            current_column += 1
    
    def save(self, path, format = None):
        self.graph.save(path, format=format)

    def setImageDir(self, path):
        self.image_source_directory = path
        
    def setTitle(self, title):
        self.title = title
        
    def setTitleSize(self, size):
        self.titleSize = size

    def setTitleColor(self, color):
        self.titleColor = color
    
    def setLabels(self, labels):
        self.labels = labels
    
    def setFont(self, font):
        self.font = font
        
    def setFontDir(self, path):
        self.font_source_directory = path

    def setColumns(self, number_columns):
        self.num_columns = number_columns

    def setWidth(self, width = 700):
        self.graph_size = (width, 400)
        self.resizeImages()
        self.graph_size = (width, self.getHeight())
        self.graph = self.graph.resize(self.graph_size)
        
    def getHeight(self):
        height = self.horz_space
        if self.title != '':
            textImg = ImageDraw.Draw(self.graph)
            font = ImageFont.truetype(self.font_source_directory, 
                                      self.titleSize)
            font_height = textImg.textsize(self.title, font=font)[1]
            height += self.horz_space + font_height
        rows = round(self.number_images / self.num_columns)
        height += self.horz_space * rows
        height += self.images[0].height * rows
        return height
    
    def setImageSpacing(self, line_spacing):
        self.vert_space = line_spacing[0]
        self.horz_space = line_spacing[1]
    
    