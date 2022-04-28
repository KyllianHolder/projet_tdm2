import PIL.Image
import os
import json
from sklearn.cluster import KMeans
from colorthief import ColorThief
from IPython.display import display
from IPython.display import clear_output
from scipy.spatial import KDTree
from webcolors import hex_to_rgb
from webcolors import CSS3_HEX_TO_NAMES

class ImageAnalysis:
    '''
    A class for analysis images and extracting metadata from them
    
    Parameters
    ----------
    directory: The directory where the images reside
    ret_name: The name of the returned json file 
    '''
    def __init__(self, directory, ret_name):
        self.extract_metadata(directory)
        self.ret_name = ret_name

    def orientation(self, height, width):
        if height > width:
            return "Portrait"
        elif width > height:
            return "Paysage"
        else:
            return "Carre"
            
    def taille(self, height, width):
        if height*width >= (1200*900):
            return "Big"
        if height*width >= (500*500) and height*width < (1200*900):
            return "Medium"
        else:
            return "Small"

    def convert_rgb_to_names(self, rgb_tuple):
        # a dictionary of all the hex and their respective names in css3
        css3_db = CSS3_HEX_TO_NAMES
        names = []
        rgb_values = []
        for color_hex, color_name in css3_db.items():
            # Ajoute à la liste names les noms des couleurs
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))

        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return f'{names[index]}'

    def extract_metadata(self, directory_name):
        directory = os.fsencode(directory_name)
        dataDict = {}
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            img = PIL.Image.open(directory_name+"/"+filename)
            exif_data = img._getexif()
            color_thief = ColorThief(directory_name+"/"+filename)
            tabcolor = color_thief.get_palette(color_count=5)
            dataDict[filename] = {
                "Height": img.height,
                "Width": img.width,
                "Orientation": self.orientation(img.height, img.width),
                "Taille": self.taille(img.height, img.width),
                "Couleur dominante 1": (self.convert_rgb_to_names(tabcolor[0]), tabcolor[0]),
                "Couleur dominante 2": (self.convert_rgb_to_names(tabcolor[1]), tabcolor[1]),
                "Couleur dominante 3": (self.convert_rgb_to_names(tabcolor[2]), tabcolor[2]),
                "Couleur dominante 4": (self.convert_rgb_to_names(tabcolor[3]), tabcolor[3]),
                "Couleur dominante 5": (self.convert_rgb_to_names(tabcolor[4]), tabcolor[4])
            }

        with open(self.ret_name, 'w') as outfile:
            json.dump(dataDict, outfile)
