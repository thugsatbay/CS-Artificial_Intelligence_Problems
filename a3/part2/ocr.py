#!/usr/bin/python
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: Rashmi Ranjan Bidanta rbidanta
#          Gurleen Singh Dhody gdhody
#          Dhaval Niphade dniphade
# (based on skeleton code by D. Crandall, Oct 2017)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print im.size
    print int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    print len(TRAIN_LETTERS)
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }


def extractTrainData(filename):
    letterCountDictionary = {}
    letterTransitionDictionary = {}
    initialLetterDictionary = {}
    emission_probability = {}
    with open(train_txt_fname,mode='r') as train_file:
        words = []
        for line in train_file:
            for i in xrange(len(line)-1):
                if line[i] in train_letters:
                    if line[i] not in letterCountDictionary:
                        letterCountDictionary[line[i]] = 1.0
                    else:
                        letterCountDictionary[line[i]] += 1.0

                    if line[i] not in letterTransitionDictionary :
                        if line[i+1] in train_letters:
                            letterTransitionDictionary[line[i]] = {line[i+1]: 1}
                    else:
                        currentletterxdict = letterTransitionDictionary[line[i]]
                        if line[i+1] not in currentletterxdict:
                            if line[i+1] in train_letters:
                                currentletterxdict[line[i+1]] = 1.0
                        else:
                            if line[i+1] in train_letters:
                                currentletterxdict[line[i+1]] += 1.0
                        letterTransitionDictionary[line[i]] = currentletterxdict
            if line[0] in train_letters:
                initialLetterDictionary[line[0]] = 1.0 if line[0] not in \
                initialLetterDictionary else initialLetterDictionary[line[0]] + 1.0


    letter_occurance_probability = { key: float(value)/sum(letterCountDictionary.\
    values()) for key, value in letterCountDictionary.items()}

    # Probability that a letter begins a sentence
    letter_begin_probability = {letter: float(sent_count_dict)/float\
    (sum(initialLetterDictionary.values())) for letter, sent_count_dict in\
    initialLetterDictionary.items()}

    # Transition probability Dictionary
    letter_trans_probability = { key: { letter: float(count)/sum(value.values())\
    for letter, count in value.items()} for key, value in \
    letterTransitionDictionary.items()}

    for trn_letter,value in train_letters.items():
        pix_letter = list(''.join([ pix_row for pix_row in value]))
        emission_probability[trn_letter] = {}
        for pos,item in enumerate(test_letters):
            obs_letter = list(''.join(item))
            match_prob = 0.0
            for i in xrange(len(obs_letter)):
                if obs_letter[i] != pix_letter[i] and pix_letter[i]=='*':
                    match_prob +=math.log(0.4)
                elif obs_letter[i] != pix_letter[i] and pix_letter[i]!='*':
                    match_prob +=math.log(0.2)
                else:
                    if obs_letter[i] == pix_letter[i] and pix_letter[i]=='*':
                        match_prob +=math.log(0.9)
                    else:
                        match_prob +=math.log(0.6)
            emission_probability[trn_letter].\
            update({'obs_letter'+str(pos): match_prob})

    return letter_occurance_probability,letter_begin_probability,\
    letter_trans_probability,emission_probability


def simplified():
    result = []
    for pos,item in enumerate(test_letters):
        pos_prob = []
        for letter , diction in letter_emission_prob.items():
            # if 'obs_letter'+str(pos) in diction.values():
            pos_prob.append((letter,diction.get('obs_letter'+str(pos))))
        result.append(max(pos_prob,key=lambda x: x[1])[0])
    print " Simplified:",''.join(result)


def hmm_ve():
    result = []
    ve_dictionary = {}
    ve_dictionary[0] = {letter: let_em_dict.get('obs_letter0')+\
    math.log(letter_begin_prob.get(letter,float(1.0e-7)))+math.log(letter_occurance_prob.\
    get(letter)) for letter , let_em_dict in letter_emission_prob.items()}
    result.append(max(ve_dictionary[0].items(),key=lambda x:x[1])[0])
    for i in xrange(1,len(test_letters)):
        interim_letter_dict = {}
        for letter, letter_dict in letter_trans_prob.items():
            letter_prob = 1.0
            for prev_letter , prob in letter_dict.items():
                letter_prob += math.exp(ve_dictionary[i-1].get(prev_letter) \
                + math.log(letter_trans_prob[prev_letter].get(letter,float(1.0e-7))))
            interim_letter_dict[letter] = math.log(letter_prob)+ letter_emission_prob[letter]\
            .get('obs_letter'+str(i))
        ve_dictionary[i] = interim_letter_dict
        result.append(max(interim_letter_dict.items(), key=lambda x : x[1])[0])
    print "     HMM VE:",''.join(result)

def hmm_viterbi():
    result = []
    # This is the dictionary that memotizes the all the marginal probabilities
    # for the possible tags at all the word positions in the sentence
    # {'position0':{tag1: (prob,None),tag2: (prob,None)
    # , tag3: (prob,None)}
    #  'position1':{tag1: (prob,Previous Maximizing tag1),tag2: (prob,
    # Previous Maximizing tag2), tag3: (prob,Previous Maximizing tag2)}
    # .......}
    memotize_viterbi = {}

    level0 = {}
    for letter in letter_occurance_prob:
        level0[letter] = (letter_emission_prob[letter].get('obs_letter0',\
        math.log(float(1.0e-7))) + math.log(letter_begin_prob.get(letter,float(1.0e-7))),None)
    memotize_viterbi[0] =  level0

    for i in xrange(1,len(test_letters)):
        # Dictionary to store the maximizing tag at each word position in a
        # sentence {"CURRENT POSSIBLE TAG":(probability,"PREVIOUS TAG")}
        # Example: {'noun':(0.0023,'det'),'verb':(0.0032,'noun')...} for
        # word at position 3 in the sentence
        level_maximizers = {}
        for letter in letter_occurance_prob:
            letter_porb_possibilities = []
            for prev_letter, prob in memotize_viterbi[i-1].items():
                letter_porb_possibilities.append((
                math.log(letter_trans_prob[prev_letter].get(letter,float(1.0e-7)))+\
                letter_emission_prob[letter].get('obs_letter'+str(i),\
                math.log(float(1.0e-7)))+prob[0],prev_letter))
            letter_max_tuple = max(letter_porb_possibilities, key=lambda x:x[0])
            level_maximizers[letter] = letter_max_tuple
        memotize_viterbi[i] = level_maximizers
    level_max = max([(key,value)for key,value in memotize_viterbi\
    [len(test_letters)-1].items()],key = lambda x: x[1][0])
    # Tag at n-1 position which maximizes the occurance probability of a tag
    # at the end of the sentence
    maximizer = level_max[1][1]
    # Append the tag that has maximum probability of occurance at the end of
    # the sentence to the result
    result.append(level_max[0])
    # Tracing the chain in reverse and generating the sequence that gives the
    # Maximum Aposteriori Probability
    for i in reversed(xrange(len(test_letters)-1)):
        level_value = memotize_viterbi[i][maximizer]
        result.append(maximizer)
        maximizer = level_value[1]
    # Reversing the list to return the resulting sequence

    print "HMM Viterbi:",''.join(result[::-1])

#####
# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

letter_occurance_prob,letter_begin_prob,letter_trans_prob,letter_emission_prob\
 = extractTrainData(train_txt_fname)

# Calling Individual Algorithms
simplified()
hmm_ve()
hmm_viterbi()
