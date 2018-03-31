###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids:
# Rashmi Bidanta, rbidanta
# Gurleen Dhody, gdhody
# Dhaval Niphade, dniphade
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # Calculate the log of the posterior probability of a given sentence
    # with a given part-of-speech labeling
    def posterior(self, sentence, label):
        # return 0
        prob = self.initial_probability.get(label[0],float(1.0e-7))
        trans_prob = 0.0
        em_prob = 0.0
        for i in xrange(0,len(sentence)-1):
            #if label[i+1] in self.transition_probability[label[i]]:
            trans_prob += math.log(self.transition_probability[label[i]].get(label[i+1],float(1.0e-7)))

        for i in xrange(0,len(sentence)):
            #if sentence[i] in self.emission_probability[label[i]]:
                #if self.emission_probability[label[i]][sentence[i]] != 0:
            em_prob += math.log(self.emission_probability[label[i]].get(sentence[i],float(1.0e-7)))
        return math.log(prob) + trans_prob + em_prob

    # Do the training!
    #
    def train(self, data):

        # HMM Probability models

        initial_probability = {}
        emission_probability = {}
        transition_probability = {}
        label_probability = {}

        # Vocabulary:

        vocabulary = set([])

        for sentence in data:
            for word in sentence[0]:
                vocabulary.add(word)
        # Parameter calculation
        label_probability = self.getLabelProbability(data)
        # print "Label probability:   ",label_probability
        self.label_probability = label_probability
        initial_probability = self.getLabelStartProbability(data)
        self.initial_probability = initial_probability
        # print "Start probability:   ",initial_probability
        transition_probability = self.getLabelXsionProability(data)
        self.transition_probability = transition_probability
        # print "Transition probability:  ",transition_probability
        emission_probability = self.getLabelEmissionProbability(data,vocabulary)
        self.emission_probability = emission_probability
        #print "Emission probability: ",emission_probability

    # Functions for each algorithm.
    #
    def simplified(self, sentence):

        #print self.emission_probability
        tagSequence = []
        for word in sentence:
            tagset = [(tag, word_dict[word]) if word in word_dict else ('x',float(1.0e-7))\
             for tag , word_dict in self.emission_probability.items()]
            tagSequence.append(max(tagset , key=lambda x: x[1])[0])
        return tagSequence
        #return [ "noun" ] * len(sentence)

    def hmm_ve(self, sentence):
        # Resulting sequence of labels for the input sentence
        result = []
        # Variable elimination probability memotization
        ve_dictionary = {}
        ve_dictionary['tau_'+str(0)] = {tag: word_dict[sentence[0]]*\
        self.label_probability[tag]*self.initial_probability[tag] if sentence[0]\
        in word_dict else float(1.0e-7) for tag,word_dict in \
        self.emission_probability.items()}

        init_tag = max([(key,value) for key,value in \
        ve_dictionary['tau_'+str(0)].items()], key=lambda x: x[1])[0]

        # print "Init Prob 1:",init_tag

        result.append(init_tag)
        for i in xrange(1,len(sentence)):
            interim_tag_dict = {}
            for tag, tag_dict in self.transition_probability.items():
                tag_prob = 0.0
                for prev_tag , prob in tag_dict.items():
                    tag_prob += ve_dictionary['tau_'+str(i-1)][prev_tag] \
                    * self.transition_probability[prev_tag][tag]
                interim_tag_dict[tag] = tag_prob* self.emission_probability[tag]\
                .get(sentence[i],float(1.0e-7))
            ve_dictionary['tau_'+str(i)] = interim_tag_dict
            result.append(max(interim_tag_dict.items(), key=lambda x : x[1])[0])
        return result


    def hmm_viterbi(self, sentence):

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
        for tag in self.label_probability:
            level0[tag] = (self.emission_probability[tag].get(sentence[0],\
            float(1.0e-7)) * self.initial_probability[tag],None)
        memotize_viterbi[0] =  level0

        for i in xrange(1,len(sentence)):
            # Dictionary to store the maximizing tag at each word position in a
            # sentence {"CURRENT POSSIBLE TAG":(probability,"PREVIOUS TAG")}
            # Example: {'noun':(0.0023,'det'),'verb':(0.0032,'noun')...} for
            # word at position 3 in the sentence
            level_maximizers = {}
            for tag in self.label_probability:
                tag_porb_possibilities = []
                for prev_tag, prob in memotize_viterbi[i-1].items():
                    tag_porb_possibilities.append((
                    self.transition_probability[prev_tag][tag]*\
                    self.emission_probability[tag].get(sentence[i],\
                    float(1.0e-7))*prob[0],prev_tag))
                tag_max_tuple = max(tag_porb_possibilities, key=lambda x:x[0])
                level_maximizers[tag] = tag_max_tuple
            memotize_viterbi[i] = level_maximizers
        level_max = max([(key,value)for key,value in memotize_viterbi\
        [len(sentence)-1].items()],key = lambda x: x[1][0])
        # Tag at n-1 position which maximizes the occurance probability of a tag
        # at the end of the sentence
        maximizer = level_max[1][1]
        # Append the tag that has maximum probability of occurance at the end of
        # the sentence to the result
        result.append(level_max[0])
        # Tracing the chain in reverse and generating the sequence that gives the
        # Maximum Aposteriori Probability
        for i in reversed(xrange(len(sentence)-1)):
            level_value = memotize_viterbi[i][maximizer]
            result.append(maximizer)
            maximizer = level_value[1]
        # Reversing the list to return the resulting sequence
        return result[::-1]



    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence)
        else:
            print "Unknown algo!"

    # This getLabelProbability() calculates the probability of occurance of a
    # particular label in the training set.
    #
    def getLabelProbability(self,data):
        dict_pos_probability = {}
        numOfWords = 0
        for item in data:
            numOfWords += len(item[0])
            for label in set(item[1]):
                if label not in dict_pos_probability:
                    dict_pos_probability[label] = item[1].count(label)
                else:
                    dict_pos_probability[label] += item[1].count(label)
        # We can do log transformation on probability
        # Removed rounding off
        return { label: (float(num_occurance)/float(numOfWords)) \
        for label , num_occurance in dict_pos_probability.items() }


    # This getLabelStartProbability() calculates the probability of occurance of a
    # particular label at the start of a sentence.
    #
    def getLabelStartProbability(self,data):
        dict_pos_start_probability = {}
        numOfSentence = 0
        for item in data:
            numOfSentence += 1
            if item[1][0] not in dict_pos_start_probability:
                dict_pos_start_probability[item[1][0]] = 1
            else:
                dict_pos_start_probability[item[1][0]] += 1
        # We can do log transformation on probability
        # Removed rounding off
        return { label: (float(num_occurance)/float(numOfSentence)) \
        if label in dict_pos_start_probability else float(1.0e-7) for label , \
        num_occurance in dict_pos_start_probability.items() }




    # This getLabelXsionProability() calculates the transition probability of
    # a lable to another lable like NOUN -> VERB, VERB -> NOUN etc.
    #
    def getLabelXsionProability(self,data,ngram=2):

        # Dictionary containing the count of all the ngram transitions
        # {(NOUN,NOUN): nnnnn,(NOUN,VERB): nnnnn,.....}
        label_transition_count = {}
        for sentence in data:
            for ngram_slot in range(0,len(sentence[1])-ngram+1):
                ngram_instance = sentence[1][ngram_slot:ngram_slot+ngram]
                if ngram_instance not in label_transition_count:
                    label_transition_count[ngram_instance] = 1
                else:
                    label_transition_count[ngram_instance] += 1

        # Dictionary that store the  the count of all the ngram transitions in the following
        # form
        # {noun:
        #       {noun: count,verb: count,....},
        #  verb:
        #       {noun: count, verb: count,....}
        #  .....
        # }
        #
        label_trans_dict = {}
        for ngram_instance , occurance in label_transition_count.items():
            label = ngram_instance[0]
            if label not in label_trans_dict:
                trans_pos_dict = {ngram_instance[1]:occurance}
                label_trans_dict[label] = trans_pos_dict
            else:
                trans_pos_dict = label_trans_dict[label]
                if ngram_instance[1] not in trans_pos_dict:
                    trans_pos_dict[ngram_instance[1]] = occurance
                else:
                    trans_pos_dict[ngram_instance[1]] += occurance
                label_trans_dict[label] = trans_pos_dict


        for label , trans_dict in label_trans_dict.items():
            for item in set(label_trans_dict) - set(trans_dict):
                label_trans_dict[label].update({item: float(1.0e-7)})


        # Removed Rounding off
        return { label: {next_label: float(occurance)/\
        float(sum(trans_dict.values())) for next_label , occurance in\
         trans_dict.items()} for label , trans_dict in label_trans_dict.items()}



    # This getLabelEmmissionProbability() calculates the emmission probability of
    # a word given a label.
    #
    def getLabelEmissionProbability(self,data,vocabulary):
        emission_probability = {}
        tag_word_count_dict = {}
        for sentence in data:
            for position,label in enumerate(sentence[1]):
                if label not in tag_word_count_dict:
                    probable_word_dictionary = {sentence[0][position]: 1}
                    tag_word_count_dict[label] = probable_word_dictionary
                else:
                    probable_word_dictionary = tag_word_count_dict[label]
                    if sentence[0][position] not in probable_word_dictionary:
                        probable_word_dictionary[sentence[0][position]] = 1
                    else:
                        probable_word_dictionary[sentence[0][position]] += 1
                    tag_word_count_dict[label] = probable_word_dictionary

        return  { label: { word: float(word_dict.get(word))/\
        float(sum(word_dict.values())) if word in\
        word_dict else float(1.0e-7) \
        for word in vocabulary } for label,word_dict in \
        tag_word_count_dict.items()}
        #pass
