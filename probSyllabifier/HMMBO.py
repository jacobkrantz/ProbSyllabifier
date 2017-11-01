class HMMBO:
    """
    Business Object for the Hidden Markov Model.

    Use: transfer trained data from training in hmm.py
        to testing in probSyllabifier.py

    Attributes:
        matrixA (numpy matrix): holds transition probabilities
        matrixB (numpy matrix): holds hiddden state prior probabilites
        observationLookup (list of 2 tuples): holds unique list of phone
                                bigrams observed during training.
        hiddenLookup (list of strings): unique tags utilized for training.
        transcriptionScheme (list of sets of phones): the provided phone
                                classification model to be tested with.
    """
    matrixA             = None
    matrixB             = None
    observationLookup   = []
    hiddenLookup        = []
    transcriptionScheme = []
