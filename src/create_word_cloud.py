#!/usr/bin/python

# -*- coding: utf-8 -*-
import os, sys
from optparse import OptionParser, OptionGroup
from pytagcloud import create_tag_image, create_html_data, make_tags

import pytagcloud
import pytagcloud.helper

class FontError(Exception):
    pass

def ParseOptions(options, args):
    # Check font 
    if not options.font in [pytagcloud.FONT_CACHE[i]['name'] for i in range(len(pytagcloud.FONT_CACHE))]:
        raise(FontError('Font %s not in cache.'%(options.font)))
    
    '''
    if options.font is not '':                
        if os.path.exists(options.font): # check for aboslute reference
            font = options.font
        else:
            raise(FontError('Cannot find font %s'%(options.font)))        
        '''

    # Check layout
    options.layout = options.layout.lower().strip()

    layout = pytagcloud.LAYOUT_MIX

    if options.layout == 'mixed':
        layout = pytagcloud.LAYOUT_MIX
    elif options.layout == 'vertical':
        layout = pytagcloud.LAYOUT_VERTICAL
    elif options.layout == 'horizontal':
        layout = pytagcloud.LAYOUT_HORIZONTAL
    elif options.layout == 'mostlyhorizontal':
        layout = pytagcloud.LAYOUT_MOST_HORIZONTAL
    elif options.layout == 'mostlyvertical':
        layout = pytagcloud.LAYOUT_MOST_VERTICAL
    else:
        print 'Unknown layout option %s'%options.layout
     
    # Read file
    if options.stdin: # read from std input
        if options.verbose:
            print 'Reading from stdin'
        input_chars = sys.stdin.read()
    elif options.filename != '':
        if options.verbose:
            print 'Reading from %s'%(options.filename)
        input_chars = open(options.filename,'r').read()
    else:
        print 'What? No input? Wierdo.'
        return

    # Calculate word distribution
    d = pytagcloud.helper.word_dist_s(input_chars,
                                      boring_words = options.boring, 
                                      min_word_length = eval(options.length), 
                                      verbose=options.verbose)
   
    options.numwords = eval(options.numwords)

    if options.numwords < len(d):
        top = d[0:options.numwords] 
    else:
        top = d   
 
    buff = {}
    for i in range(len(top)):
        buff[top[i][0]] = top[i][1]

    buff = zip(buff.keys(), buff.values()) # make_tags now needs a list of tuples 

    mtags = make_tags(buff)

    create_tag_image(mtags, 
                    options.outfile, 
                    size=(eval(options.width), eval(options.height)), 
                    background=(255, 255, 255, 255), 
                    crop=options.crop, 
                    fontname=options.font,
                    layout=layout,
                    fontzoom=eval(options.fontzoom))

if __name__ == "__main__":
    '''
    options needed
    --------------
    colours
    font file
    background colour
    file type (png, jpg, svg)
    orientation (vertical, horizontal)
    crop (true false)    
    imagesize
    fontsize    
    '''

    parser = OptionParser()
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Print extra words which might contain useful stuff.')

    # input options
    input_options = OptionGroup(parser, 'Input Options')
    input_options.add_option('-i', '--stdin', dest='stdin', action='store_true', default=False, help='Takes input from stdin.')
    input_options.add_option('-f', '--file', dest='filename', help='Read words from filename', default='',metavar='FILE')
    parser.add_option_group(input_options)

    # output options
    output_options = OptionGroup(parser, 'Output Options')    
    output_options.add_option('-o', '--outfile', dest='outfile', default='output.png', help='Output file.',metavar='FILE')
    # svg/html/png option
    parser.add_option_group(output_options)

    # string butchering
    string_options = OptionGroup(parser, 'String Manipulation Options')
    string_options.add_option('-n', '--numwords', dest='numwords', default='100', help='Number of words to include in cloud.')
    string_options.add_option('-b', '--boring', dest='boring', default='', help='File with a list of boring words, 1 word per line.',metavar='FILE')
    string_options.add_option('-w', '--minwordlength', dest='length', default=4, help='Minimum length of words in cloud.')
    parser.add_option_group(string_options)

    # layout options
    layout_options = OptionGroup(parser, 'Layout Options')
    layout_options.add_option('--font', dest='font', default=pytagcloud.DEFAULT_FONT, help='Font to use. Must be one of these fonts: %s'%", ".join([f['name'] for f in pytagcloud.FONT_CACHE]))
    layout_options.add_option('--crop', dest='crop', default=False, action='store_true', help='Crop the final image')
    layout_options.add_option('--layout',dest='layout',default='Mixed',help='Word orientation: Mixed, Vertical, Horizontal, MostlyVertical or MostlyHorizontal')
    layout_options.add_option('-x', dest='width', default=1280, help='Width of image')
    layout_options.add_option('-y', dest='height', default=800, help='Height of image')
    layout_options.add_option('-z', '--zoom', dest='fontzoom', default=3, help='Font zoom (effect of tag count on the font size)')
    # colour options
    # background colour/alpha
    parser.add_option_group(layout_options)
     
    (options, args) = parser.parse_args()

    ParseOptions(options,args)
