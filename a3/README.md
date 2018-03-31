# Assignment 3 Applications of Hidden Markov Models
## Team Members: Dhaval Niphade, Gurleen Singh Dhody, Rashmi Ranjan Bidanta


## Part 1 Part Of Speech(POS) Tagging

### Given :
* **Training Data:** A text file from brown corpus with each word tagged with corresponding POS tags
* **Number of Sentences:**  44204
* **Number of Words:**  955797

### HMM Parameters:

**Initial Probability**: Python dictionary where key the Tag and value is the probability of that tag being the first word for the sentence in the training text file e.g: {'noun':.019,'verb':0.011,....,'.':0.016}

**Transition Probability**: Python dictionary where key is the Tag1 and Value is a python dictionary with key Tag2 and its probability given the Tag1.
e.g:{'noun':{'noun':0.00013,'verb':0.00123,....,'.':0.00023},'verb':{'noun':0.00013,'verb':0.00123,....,'.':0.00023},....,'.':{'noun':0.00013,'verb':0.00123,....,'.':0.00023}}

**Emission Probability**: Python dictionary where key is the Tag and Value is a python dictionary with key as word and value as its probability given the Tag.
e.g:{'noun':{'word_1':0.00013,'word_2':0.00123,....,'word_n':0.00023},'verb':{'word_1':0.00013,'word_2':0.00123,....,'word_n':0.00023},....,'.':{'word_1':0.00013,'word_2':0.00123,....,'word_n':0.00023}}



### To Do :
* Find the sequence of POS tags for test sentences based on the HMM model trained from the the given training data
* Find the log posterior probability of sequence of POS tag for test sentence

### Algorithms  :
  - *Simplified* :- This built based on a simplified Bayes Net where observation drives the occurrence of a POS tag. Here we just have to take into account the maximum emission probability for each word in the sentence to find out the sequence of POS tags.

  - *HMM Variable elimination* :- This is based on the Bayes Net where we also have to take into account the transition probability from one tag to another and then perform variable elimination to find out the maximum likelihood sequence of POS tags for a given sentence.

  - *HMM Viterbi* :- Here we use the Viterbi decoding, to find out the Maximum Aposteriori Probability of a sequence of tags for a test sentence. This uses dynamic programming approach where we build a trellis like structure as we calculate the POS probability for each word in the sentence. Once we are done with the whole sentence we take the maximum probability POS tag for the last word and then trace back the tag that maximized the probability of this last word. We follow this approach for each word and trace the MAP sequence of POS tags.

### Results :

For a test file with 2000 sentences and 29442 words we got the following results:

0. Ground truth:      **100.00%**             **100.00%**
1. Simplified:        **90.75%**               **34.95%**
2. HMM VE:            **93.39%**               **44.45%**
3. HMM MAP:           **95.07%**               **54.50%**

The words were identified with increasing probability of Simplified(90.75%) < HMM VE(93.39%) < HMM Viterbi(95.07%)
Sentences Simplified(34.95%) < HMM VE(44.45%) < HMM Viterbi(54.50%)

## Part 2 Optical Character Recognition

### Given:
* **Training Image**: An courier-train.png image file consisting of images of 26 upper case letters 26 lower, 0-9 Numbers and "(),.-!?'" " special characters a total of 72 characters.
* **Training Text**: We used brown_train.txt to train the HMM parameters and create the HMM model.

### HMM Parameters:

**Initial and Transition Probability**:We calculated the Initial and Transition Probability the similar way we calculated in part one, but in this case the probabilities were calculated for the letters instead of words.

**Emission Probability**: The most challenging part was calculating the emission probability. The approach we used was we assigned probabilities to the individual pixel in the observed letter from the Image. We used the Naive Bayes approach to find these probabilities. As we had 350 pixels so the actual probability ran into the problem of underflow and we had to perform [log transformation](https://www.youtube.com/watch?v=-RVM21Voo7Q) to handle the problem of extremely small numbers.

### To Do:
Recognize the sequence to letters from the test image files. The image files could contain noise as well.

### Algorithms:
Same as were used for part 1

### Result:
We tested the model on ![Image](./part2/test-17-0.png) and got the following result.

  - Simplified:   **1t is so ordered.**
  - HMM VE:   **It is so ordered.**
  - HMM Viterbi:  **It is so ordered.**
