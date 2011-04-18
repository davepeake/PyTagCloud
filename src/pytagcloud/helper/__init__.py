'''
helper functions
'''
import string, operator

TAGCLOUD_NONE = 0
TAGCLOUD_UPPER = 1
TAGCLOUD_LOWER = 2

def remove_boring_words(words,wordlist=''):
	'''
	eventually this'll do something smarter
	at the moment it just removes all words with 3 or less letters

	wordlist = file with a bunch of boring words
	'''
	k = words.keys()

	for i in range(len(k)):
		if len(k[i]) <= 3:
			words.pop(k[i])

	if wordlist is not '':
		fin = open(wordlist,'r')
		boring_words = [i.rstrip() for i in fin.readlines()]

		for i in boring_words:
			if i in k:
				words.pop(i)

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

def sort_dict(d):
    '''
    Return a tuple of the dictionary sorted by its values
    '''
    return sorted(d.iteritems(), key=operator.itemgetter(1),reverse=True)

def word_dist_s(s, boring_words=''):
    print 'Lowering case and removing punctuation'
    s = string_conditioning(s)

    print 'Splitting words'
    s = s.split()
    print 'There are %d words'%(len(s))

    words = {}

    print 'Counting words'
    
    for i in range(len(s)):
        w = s[i]

        if (w in words.keys()):
            #print 'iterating',w
            words[w] += 1
        else:
            #print 'adding',w
            words[w] = 1

        #print 'number of unique words:',len(words.keys())
        #if not (i % 1000):
        #    print i, 'words done'

	words = remove_boring_words(words, boring_words)

    return sort_dict(words)

def word_dist_file(filename):
	fin = open(filename,'r')
	s = fin.read()

	return word_dist_s(s)
