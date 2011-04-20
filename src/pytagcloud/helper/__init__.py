'''
helper functions
'''
import string, operator

TAGCLOUD_NONE = 0
TAGCLOUD_UPPER = 1
TAGCLOUD_LOWER = 2

def vprint(msg, verbose):
    if verbose:
        print msg
    
def remove_boring_words(words,wordlist=''):
    '''
    wordlist = file with a bunch of boring words
    '''
    k = words.keys()

    if wordlist is not '':
        fin = open(wordlist,'r')
        boring_words = [i.rstrip() for i in fin.readlines()]

        for i in boring_words:
            if i in k:
                words.pop(i)

    return words

def remove_short_words(words, minlength=3):
    '''
    eventually this'll do something smarter
    at the moment it just removes all words with 3 or less letters

    '''
    if minlength == 0:
        return words

    k = words.keys()
    for i in range(len(k)):
        if len(k[i]) <= minlength:
            words.pop(k[i])

    return words

def string_conditioning(s, s_case=TAGCLOUD_LOWER, s_punc=False):
    '''
    massage the string

    s_case = TAGCLOUD_NONE # leave the capitalisation
             TAGCLOUD_UPPER # capitalise everything
             TAGCLOUD_LOWER # everything lower case

    s_punc = True # leave the punctuation
             False # remove the punctuation
    '''
    if s_case == TAGCLOUD_LOWER:
        s = s.lower()
    elif s_case == TAGCLOUD_UPPER:
        s = s.upper()
    
    if not s_punc:
        t = string.maketrans(string.punctuation,' ' * len(string.punctuation))
        s = s.translate(t)

    return s

def sort_dict(d,verbose=False):
    '''
    Return a tuple of the dictionary sorted by its values
    '''
    vprint('Sorting words by count',verbose)

    return sorted(d.iteritems(), key=operator.itemgetter(1),reverse=True)

def word_dist_s(s, boring_words='', min_word_length=4, verbose=False):

    vprint('Lowering case and removing punctuation',verbose)
    s = string_conditioning(s)

    vprint('Splitting words',verbose)
    s = s.split()
    vprint('There are %d words'%(len(s)),verbose)

    words = {}

    vprint('Counting words',verbose)
    
    for i in range(len(s)):
        w = s[i]

        if (w in words.keys()):
            #print 'iterating',w
            words[w] += 1
        else:
            #print 'adding',w
            words[w] = 1

        if not (i % 1000):
            vprint( '%d words done'%(i), verbose)

    vprint('number of unique words:%d'%len(words.keys()), verbose)

    if boring_words is not '':
        vprint('Removing boring words',verbose)
        words = remove_boring_words(words, boring_words)

    vprint('Removing words over length %d'% min_word_length,verbose)
    words = remove_short_words(words, min_word_length)

    return sort_dict(words,verbose)

def word_dist_file(filename,verbose=False):
    fin = open(filename,'r')
    s = fin.read()

    return word_dist_s(s,verbose)
