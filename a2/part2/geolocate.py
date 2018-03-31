#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import operator
import copy
import heapq
import math


# This Naive Bayes classifier, classifies the Tweets based on its location.
# The Training dataset consists of 32000 tweets and test dataset consists of
# 500 tweets.
# The accuracy of current model is approximately 60% on the testing dataset
# The accuracy on Training dataset is 70%


'''Source: http://www.nltk.org/book/ch02.html'''
# ---------------------------------------------------------

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
            'his', 'himself','she', 'her', 'hers','herself', 'it', 'its',
            'itself', 'they', 'them', 'their','theirs', 'themselves','what',
            'which', 'who', 'whom', 'this', 'that', 'these','those', 'am',
            'is', 'are','was', 'were', 'be', 'been', 'being', 'have', 'has',
            'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
            'and', 'but','if', 'or', 'because', 'as', 'until','while', 'of',
            'at', 'by', 'for', 'with','about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after','above', 'below', 'to',
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over','under',
            'again', 'further', 'then', 'once', 'here', 'there', 'when',
            'where','why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
            'most', 'other','some', 'such', 'no', 'nor', 'not', 'only', 'own',
            'same', 'so','than', 'too','very', 's', 't', 'can', 'will', 'just',
            'don', 'should', 'now']

#----------------------------------------------------------


# Read file from arguments
trainingTweetBank = sys.argv[1]

testingTweetBank = sys.argv[2]

classifyOutput = sys.argv[3]


def buildDataModel(datafile):

    '''
    Builds the data model from the testing bank of tweets and returns three dictionaries

    1)
        Bag of words for a location, This is a dictionary with location as key and a
        dictionary as a value. The dictionary value has a word as key and word freq
        as the value. example:

        loc_BagOWords = {   location1:  {   word1:  freq,
                                            word2:  freq,
                                            .
                                            .
                                            .
                                        }

                            location2:  {   word1:  freq,
                                            .
                                            .
                                            .
                                        }
                            .
                            .
                            .
                        }
    2) Dictiory of location and corresponding count of tweets
        Dictionary : Key = Location , Value = Frequency of tweets
        loc_tweet_count_dict =  {   location1: numoftweets,
                                    location2: numoftweets,
                                    .
                                    .
                                    .
                                }
    3) Vocabulary of entire training tweet set with frequency of each word
        Vocabulary Dictionary : Key = Word , Value = Frequency of word
        global_bagOfWords = {   word1:  freq,
                                word2:  freq,
                                .
                                .
                                .
                            }
    '''
    loc_BagOWords = {}
    loc_tweet_count_dict = {}
    global_bagOfWords = {}
    with open(trainingTweetBank) as tweets:
        for tweet in tweets:
            location = getTweetLocation(tweet)
            bOWords = generateBagOfWords(tweet)
            locWordDict = {}
            if location in loc_BagOWords:
                locWordDict = loc_BagOWords.get(location)
                loc_tweet_count_dict[location] += 1
            else:
                loc_tweet_count_dict[location] = 1
            for word in bOWords:
                if word in locWordDict and word != '':
                    locWordDict[word] = int(locWordDict.get(word))+1
                else:
                    locWordDict[word] = 1
                if word in global_bagOfWords:
                    global_bagOfWords[word] +=1
                else:
                    global_bagOfWords[word] = 1
            loc_BagOWords[location] = locWordDict

    # Removing words that occur once in a Location's bag pf words
    for location,bagofwords in loc_BagOWords.iteritems():
        loc_BagOWords[location] = dict(filter(lambda word: word[1] != 1 , bagofwords.items()))

    global_bagOfWords = dict(filter(lambda word: word[1] != 1 , global_bagOfWords.items()))

    return loc_BagOWords,loc_tweet_count_dict,global_bagOfWords



def printTopFiveWordsFrequency(loc_BagOWords):
    ''' Prints the top 5 words for all the locations'''
    for location,bagofwords in loc_BagOWords.iteritems():
        print "======================================"
        print "Top 5 tweet words for ",location
        print "**************************************"
        sort_dict = list(reversed(sorted(bagofwords.items() , \
        key=operator.itemgetter(1))))[:5] #Print top five words
        for word_freq in sort_dict:
            print word_freq[0]," has ",word_freq[1], "occurances"


def getTweetLocation(tweet):
    ''' Returns actual location from the tweet'''
    location = tweet.split(' ')[0].strip().split('\r')[0]
    return location

def generateBagOfWords(tweet):
    '''
        Generates the bag of words for the tweet based on the follwoing criteria:
        1) Ignores the cases (Converts all the words to lower case)
        2) Removes the special characters from the word except for '.','@' and '#'
        3) Filters stopwords Source: http://www.nltk.org/book/ch02.html
        4) Removes numerical words
        5) Only considers words with length greater than one, abbreviations like
           IL,MA,CA should be counted as legitimate words
    '''
    # Ignoring special characters in words
    # Ignoring the case
    tweet_instance = [word.strip().lower() if word.strip().isalnum() else
    re.sub(r'[^a-zA-Z0-9@#\.]+',r'',word).strip().lower() for word\
    in tweet.split(' ')[1:] ];
    # Ignoring Stop Words
    tweet_instance = list(filter(lambda words: words!='' and words not \
    in stopwords and not words.strip(' ').isdigit() and len(words)>1,tweet_instance))
    # Ignoring digits
    return [word for word in tweet_instance if not word.isdigit()]


# Prior Calculation: Probaility that a tweet belongs to a particular location
def calculatePrior(location,loc_tweet_count_dict,totalTweetCount):
    '''Prior Calculation: Log of Probaility that a tweet belongs to a particular location'''
    loc_tweet_count = loc_tweet_count_dict[location]
    return math.log(float(loc_tweet_count)/float(totalTweetCount))



def trainNaiveBayes(loc_BagOWords,loc_tweet_count_dict,global_bagOfWords):
    '''
    Trains the Naive Bayes Classification Model with Prior and Likelihood Probaility calculation

    prior_dict          :    Dictionary of prior probability for the locations
    likelihood_dict     :    Dictionary of likelihood probaility that a word from
                             vocabulary would appear given we know the location
    all_tweet_count     :    Total number of tweets in training data set.
    vocabulary          :    All disticst words in the training data set.

    Returns:- Dictionary for Prior and likelihood  and voc
              List of all the words in training Vocabulary

    '''
    prior_dict = {}
    likelihood_dict = {}
    all_tweet_count = sum(loc_tweet_count_dict.values())
    vocabulary = global_bagOfWords.keys()
    for loc,locbagofwords in loc_BagOWords.iteritems():
        prior_dict[loc] = calculatePrior(loc,loc_tweet_count_dict,\
        all_tweet_count)
        for word in global_bagOfWords:
            if word in locbagofwords:
                loc_word_count = locbagofwords[word]
            else:
                loc_word_count = 0.0
            likelihood_dict[(word,loc)] = calculateLikelihood(loc_word_count,\
            loc_tweet_count_dict[loc],len(vocabulary))
    return prior_dict,likelihood_dict,vocabulary


# Calculates liklihood of a word to occur given a lcoation is provided
def calculateLikelihood(loc_word_count,loc_allword_count,vocabulary):
    '''Calculates log probability for the likelihood of a word to occur given a location is provided'''
    likelihood = (float(loc_word_count)+1)/((float(loc_allword_count)+vocabulary))
    return math.log(likelihood)

# Test the trained model on a test twitter bank
def dclassifyTweetLoc(testingTweetBank,prior_dict,likelihood_dict,vocabulary):
    '''Test the trained model on a test twitter bank'''
    accuracy = 0;
    testtweetcount = 0;

    outfile = open(classifyOutput,"w")
    with open(testingTweetBank) as testweets:
        for testweet in testweets:
            testtweetcount+=1
            location = testweet.split(' ')[0]
            classifiedas = calculatePosterior(testweet,prior_dict,\
            likelihood_dict,vocabulary)
            outfile.write(classifiedas[1]+" "+testweet)
            if location == classifiedas[1]:
                accuracy+=1
    outfile.close()
    print "Accuracy=",(float(accuracy)/float(testtweetcount))*100.0



# Calulates the probability of location given a word P(location|word)
def calculatePosterior(testweet,prior_dict,likelihood_dict,vocabulary):
    ''' Calculates Posterior Probability of a City Given words in a Tweet '''
    tweet_BOW = generateBagOfWords(testweet)
    posteriors = []
    for loc,loc_prior in prior_dict.iteritems():
        loc_word_posterior_prob = prior_dict[loc]
        for word in tweet_BOW:
            if word in vocabulary:
                loc_word_posterior_prob+=likelihood_dict[(word,loc)]
        posteriors.append((loc_word_posterior_prob,loc))
    return max(posteriors)


# Execution of code
# Generate Bag of Words, Twitter bank vocabulary, Dataset
loc_BagOWords,loc_tweet_count_dict,global_bagOfWords = \
buildDataModel(trainingTweetBank)
# Train the Naive Bayes Classifier
prior_dict,likelihood_dict,vocabulary = trainNaiveBayes(loc_BagOWords,\
loc_tweet_count_dict,global_bagOfWords)
# D-Classify the Test Dataset
dclassifyTweetLoc(testingTweetBank,prior_dict,likelihood_dict,vocabulary)
# Print Top five words for each location
printTopFiveWordsFrequency(loc_BagOWords)

'''Referrence: Naive Bayes Classification and Sentiments https://web.stanford.edu/~jurafsky/slp3/6.pdf '''
