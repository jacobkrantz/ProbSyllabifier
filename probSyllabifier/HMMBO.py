class HMMBO:
    """
    Business Object for the Hidden Markov Model.

    Use: transfer trained data from training in hmm.py
        to testing in probSyllabifier.py

    Attributes:
        matrix_a (numpy matrix): holds transition probabilities
        matrix_b (numpy matrix): holds hidden state prior probabilities
        observation_lookup (list of 2 tuples): holds unique list of
            phone bigrams observed during training.
        hidden_lookup (list of strings): unique tags utilized for training.
        transcription_scheme (list of sets of phones): the provided
            phone classification model to be tested with.
    """
    matrix_a = None
    matrix_b = None
    observation_lookup = []
    hidden_lookup = []
    transcription_scheme = []
