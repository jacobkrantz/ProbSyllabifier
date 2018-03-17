
from config import settings as config
from ps_utils import Utils
from SimpleHOHMM import HiddenMarkovModelBuilder as Builder


class ProbSyllabifier:
    """
    Syllabifies a given sequence of phones using the Viterbi Algorithm.
    Provides an empty result when a foreign phone bigram is parsed.
    """

    def __init__(self, transcription_scheme=[]):
        self._transcription_scheme = transcription_scheme
        self._model = None
        self._utils = Utils()
        if(len(transcription_scheme) == 0):
            self._transcription_scheme = self._utils.load_scheme(2)

    def train(self, training_set):
        """
        Trains all structures needed to create a Hidden Markov Model.
        Returns:
            HiddenMarkovModel: An HMM after being trained explicitly
        """
        obs, states = self._split_training_set(training_set)
        builder = Builder()
        builder.add_batch_training_examples(obs, states)
        self._model = builder.build(synthesize_states=True, k_smoothing=0.0)

    def learn(self, model, sequences):
        """
        Improve the HMM parameter estimations given a set of sequence
            observations to condition on.
        Args:
            model (HiddenMarkovModel): model to further train
            sequences (list<O>): list of observations O = (O1,O2,...On)
                where O is list<char>
        Returns:
            Boolean: true if the model was iterated over.
        """
        if model == None:
            return False
        return self._model.learn(sequences, delta=0.01, k_smoothing=0.1) > 0

    def syllabify(self, observation):
        """
        Generates the syllabification of a given word string.
        Args:
            observation (string): sequence of phones
        Returns:
            string: observation string with '-'
                            representing syllable boundaries.
        """
        states = self._model.decode(self._format_obs(observation))
        return self._combine(observation, states)

    # ---------------- #
    #     Private      #
    # ---------------- #

    # 2-@n-mVN-g@R
    # {-n@-pists
    def _split_training_set(self, training_set):
        all_obs = []
        all_states = []
        for word in training_set:
            result = self._utils.parse_celex_training_word(
                word,
                self._transcription_scheme
            )
            all_obs.append(result[0])
            all_states.append(result[1])

        return all_obs, all_states

    def _format_obs(self, word):
        """
        Formats a word into a list of observations for the HMM.
        Args:
            word (string): example: '_VgIN'
        Returns:
            list<string>: example: ['md', 'di', 'ij', 'jh', 'hd', 'dm']
                where m is the start and end tag category.
        """
        observation, ignore = self._utils.parse_celex_training_word(
            word,
            self._transcription_scheme
        )
        return observation

    def _combine(self, observation, states):
        result = ""

        # ignore the start and end tags that the model outputs
        if config["model"]["use_start_tags"]:
            states = states[1:-1]

        for i in range(len(observation) - 1):
            result += observation[i]
            if('1' in states[i]):
                result += '-'
        else: # no break
            result += observation[-1]

        return result
