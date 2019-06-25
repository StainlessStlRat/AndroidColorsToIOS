
from os import listdir
from os.path import isfile, join

import os
import xml.etree.ElementTree as ET

import json

def convertXML(xmlfile, night_xmlfile, output_folder): 
    print "Begin conversion"

    print "Parsing day file"
    cache = _file_to_cache(xmlfile)
    print "Parsing night file"
    night_cache = _file_to_cache(night_xmlfile)

    for color_name, color_string in cache.items():
        night_color_string = None
        if color_name in night_cache:
            night_color_string = night_cache[color_name]
        _convert_value(color_name, color_string, night_color_string, output_folder)    
    

def _file_to_cache(xmlfile):
    cache = {}
    if xmlfile == None:
        return cache

    unresolved = {}
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
    for color in root: 
  
        #print color.get("name")
        # iterate child elements of item 

        color_name = color.get("name")
        color_string = color.text.encode('utf8')
        
        if color_string[0] != '#': # must be reference entry
            color_string = color_string.replace('@color/', '')
            unresolved[color_name] = color_string
            print 'placed in unresolved', color_name, color_string
        else:
            cache[color_name] = color_string
            

    print len(unresolved), "referential colors. Processing now"
    for color_name, color_reference in unresolved.items():
        if color_reference in cache:
            resolved_color_string = cache[color_reference]
            cache[color_name] = resolved_color_string
        else:
            raise ValueError("Couldn't resolve entry:" + color_name)

    return cache
          
def _convert_value(color_name, color_string, night_color_string, output_folder):
    print color_name, color_string

    new_folder = join(output_folder, color_name + '.colorset')

    # create the color's folder
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    r,g,b,a = _android_hex_to_rgba(color_string)
    #print "Converted", color_string, "to RGBA", r, g, b, a

    # create the color's JSON
    if night_color_string == None:
        json_data = _create_color_json_data(r, g, b, a)
    else:
        night_r, night_g, night_b, night_a = _android_hex_to_rgba(night_color_string)
        json_data = _create_color_json_data_with_night(r, g, b, a, night_r, night_g, night_b, night_a)

    with open(join(new_folder, 'Contents.json'), 'w') as outfile:  
        json.dump(json_data, outfile)


def _android_hex_to_rgba(android_hex_color):
    r = 1.0 
    g = 1.0 
    b = 1.0 
    a = 1.0

    # print "Length of", android_hex_color, ":", len(android_hex_color)

    #format is argb or rgb
    if len(android_hex_color) == 7:
        r = _hex_string_to_decimal(android_hex_color[1:3])
        g = _hex_string_to_decimal(android_hex_color[3:5])
        b = _hex_string_to_decimal(android_hex_color[5:7])
    elif len(android_hex_color) == 9:
        a = _hex_string_to_decimal(android_hex_color[1:3])
        r = _hex_string_to_decimal(android_hex_color[3:5])
        g = _hex_string_to_decimal(android_hex_color[5:7])
        b = _hex_string_to_decimal(android_hex_color[7:9])
    else:
        raise ValueError("Failed to parse argb from " + android_hex_color)

    return r, g, b, a

def _hex_string_to_decimal(hex_value_string):
    if len(hex_value_string) != 2:
        raise ValueError('Hex value should always be length == 2! Value:' + hex_value_string)
    integer_value = int(hex_value_string, 16)
    return integer_value / 255.0

def _create_color_json_data(r, g, b, a):
    data = {}  
    
    data['info'] = {  
        'version': '1',
        'author': 'xcode'
    }

    data['colors'] = []
    data['colors'].append({
        'idiom' : 'universal',
        'color' : _create_json_color(r,g,b,a)
    })
    return data

def _create_color_json_data_with_night(r, g, b, a, night_r, night_g, night_b, night_a):
    data = {}  
    
    data['info'] = {  
        'version': '1',
        'author': 'xcode'
    }

    data['colors'] = []
    data['colors'].append({
        'idiom' : 'universal',
        'color' : _create_json_color(r,g,b,a)
    })

    data['colors'].append({
        'idiom' : 'universal',
        "appearances" : [{
            "appearance" : "luminosity",
            "value" : "light"
        }],
        'color' : _create_json_color(r,g,b,a)
    })

    data['colors'].append({
        'idiom' : 'universal',
        "appearances" : [{
            "appearance" : "luminosity",
            "value" : "dark"
        }],
        'color' : _create_json_color(night_r,night_g,night_b,night_a)
    })
    return data

def _create_json_color(r,g,b,a):
    return {
        'color-space' : 'srgb',
        'components' : {
          'red' : str(r),
          'blue' : str(b),
          'green' : str(g),
          'alpha' : str(a),
        }
    }

#def test():
#    print "Running test"
#    filename = '/Users/harrison/dev/gameye/android/GAMEYE/app/src/main/res/values/colors.xml'
#    night_filename = '/Users/harrison/dev/gameye/android/GAMEYE/app/src/main/res/values-night/colors.xml'
#    output_folder = '/Users/harrison/Documents/colors_test'
#    convertXML(filename, None, output_folder)
#    convertXML(filename, night_filename, output_folder + '_night')
