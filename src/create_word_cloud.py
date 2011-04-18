#!/usr/bin/python

# -*- coding: utf-8 -*-
import os, sys
from optparse import OptionParser
from pytagcloud import create_tag_image, create_html_data, make_tags

import pytagcloud
import pytagcloud.helper

class FontError(Exception):
    pass

def test_make_tags(self):
    self.mtags =  make_tags(self.wordcounts)
     #print self.mtags
    create_tag_image(self.mtags, os.path.join(self.home, 'cloud_mtags.png'), size=(600, 500), background=(255, 255, 255, 255), vertical=True, crop=True, fontname='pytagcloud/fonts/Arial.ttf', fontzoom=3)

def test_create_tag_image(self):
    start = time.time()
    create_tag_image(self.tags, os.path.join(self.home, 'cloud.png'), size=(600, 500), background=(255, 255, 255, 255), vertical=True, crop=True, fontname='pytagcloud/fonts/Arial.ttf', fontzoom=3)
    print "Duration: %d sec" % (time.time() - start)

def ParseOptions(options, args):
    font = '/usr/share/fonts/truetype/freefont/FreeSans.ttf'
    
    if options.font is not '':
        if os.path.exists(options.font): # check for aboslute reference
            font = options.font
        else:
            raise(FontError('Cannot find font %s'%(options.font)))        

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
    d = pytagcloud.helper.word_dist_s(input_chars,options.boring,verbose=options.verbose)
   
    options.numwords = eval(options.numwords)
    top = d[0:options.numwords] 
    
    buff = {}
    for i in range(len(top)):
        buff[top[i][0]] = top[i][1]

    mtags = make_tags(buff)

    #create_tag_image(mtags, options.outfile, size=(1280, 800), background=(255, 255, 255, 255), vertical=True, crop=False, fontname='/home/djpeake/Programming/svn/PyTagCloud/src/pytagcloud/fonts/Dave.ttf', fontzoom=5)
    create_tag_image(mtags, options.outfile, size=(1280, 800), background=(255, 255, 255, 255), vertical=True, crop=False, fontname=font, fontzoom=5)

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
    parser.add_option('-i', '--stdin', dest='stdin', action='store_true', default=False, help='Takes input from stdin.')
    parser.add_option('-f', '--file', dest='filename', help='Read words from filename', default='')
    parser.add_option('-o', '--outfile', dest='outfile', default='output.png', help='Output file')
    parser.add_option('-n', '--numwords', dest='numwords', default='100', help='Number of words to include in cloud.')
    parser.add_option('-b', '--boring', dest='boring', default='', help='File with a list of boring words, 1 word per line.')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='Print extra words which might contain useful stuff.')
    parser.add_option('--font', dest='font', default='', help='Font to use. Font must be absolute reference, in local dir or font dir');

    (options, args) = parser.parse_args()

    ParseOptions(options,args)

''' 
    d = pytagcloud.helper.word_dist_file('test.txt')

    top = d[0:100] 
    
    buff = {}
    for i in range(len(top)):
        buff[top[i][0]] = top[i][1]

    mtags = make_tags(buff)

    create_tag_image(mtags, os.path.join('/home/djpeake', 'cloud_mtags.png'), size=(1280, 800), background=(255, 255, 255, 255), vertical=True, crop=False, fontname='pytagcloud/fonts/Dave.ttf', fontzoom=5)
'''
