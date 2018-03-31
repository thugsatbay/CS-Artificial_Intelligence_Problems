# Games and Tweet Classification

## Team Members:
### Dhaval Niphade , Gurleen Singh Dhody, Rashmi Ranjan Bidanta


## 1. Game : pichuAI

### Algorithm:  minimax with alpha-beta pruning

#### Heuristics Used:
* Material
* Piece Placement (Center Control)
* Mobility
* King Safety
* Pawn Structure

[Evaluation Criteria Reference](https://chessprogramming.wikispaces.com/Evaluation)

## 2. Twitter Location Classification

### Algorithm: Naive Bayes Classification

#### Approach: Bag Of Words
* Feature(words) extraction from Class (Location tweets) and building Vocabulary for entire training dataset as well as individual location.
* Calculation of Prior Probabilities of Location (Cities where the tweets originate)
* Calculation of likelihood Probabilities of occurrence of word given a location.
* Posterior probability calculation of location given a word using the prior and posterior probabilities calculated in step 2 and 3.
* Dataset Used:

  *Training:* 21440 tweets across 12 cities
  *Testing:* 10560 tweets across 12 cities
* Accuracy: 61%

[Reference](https://web.stanford.edu/~jurafsky/slp3/6.pdf)
