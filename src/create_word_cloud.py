#!/usr/bin/python

# -*- coding: utf-8 -*-
import os, sys
from optparse import OptionParser
from pytagcloud import create_tag_image, create_html_data, make_tags

import pytagcloud
import pytagcloud.helper

class FontError(Exception):
    pass

'''
def test_make_tags(self):
    self.mtags =  make_tags(self.wordcounts)
     #print self.mtags
    create_tag_image(self.mtags, os.path.join(self.home, 'cloud_mtags.png'), size=(600, 500), background=(255, 255, 255, 255), vertical=True, crop=True, fontname='pytagcloud/fonts/Arial.ttf', fontzoom=3)

def test_create_tag_image(self):
    start = time.time()
    create_tag_image(self.tags, os.path.join(self.home, 'cloud.png'), size=(600, 500), background=(255, 255, 255, 255), vertical=True, crop=True, fontname='pytagcloud/fonts/Arial.ttf', fontzoom=3)
    print "Duration: %d sec" % (time.time() - start)
'''

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
                                      min_word_length = options.length, 
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
                    size=(1280, 800), 
                    background=(255, 255, 255, 255), 
                    crop=options.crop, 
                    fontname=options.font, 
                    fontzoom=5)

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
    parser.add_option('-i', '--stdin', dest='stdin', action='store_true', default=False, help='Takes input from stdin.')
    parser.add_option('-f', '--file', dest='filename', help='Read words from filename', default='')
    # output options
    parser.add_option('-o', '--outfile', dest='outfile', default='output.png', help='Output file.')
    # svg/html/png option

    # string butchering
    parser.add_option('-n', '--numwords', dest='numwords', default='100', help='Number of words to include in cloud.')
    parser.add_option('-b', '--boring', dest='boring', default='', help='File with a list of boring words, 1 word per line.')
    parser.add_option('-w', '--minwordlength', dest='length', default=4, help='Minimum length of words in cloud.')
    # minimum word length

    # layout options
    parser.add_option('--font', dest='font', default=pytagcloud.DEFAULT_FONT, help='Font to use. Must be one of these fonts: %s'%", ".join([f['name'] for f in pytagcloud.FONT_CACHE]))
    parser.add_option('--crop', dest='crop', default=False, action='store_true', help='Crop the final image')
    # mostly vert, mostly horiz, mixed
    # colour options
    # x y image size
    # background colour/alpha
     
    (options, args) = parser.parse_args()

    ParseOptions(options,args)
