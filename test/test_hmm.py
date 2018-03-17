import unittest

from utils import HiddenMarkovModel as Hmm
from utils import HiddenMarkovModelBuilder as Builder

class TestHMM(unittest.TestCase):
    def setUp(self):
        self.sequences = [
            ['normal', 'cold', 'dizzy','normal','normal'],
            ['normal', 'cold', 'normal','dizzy','normal'],
            ['dizzy', 'dizzy', 'dizzy','cold','normal'],
            ['dizzy', 'dizzy', 'normal','normal','normal'],
            ['cold', 'cold', 'dizzy','normal','normal'],
            ['normal', 'dizzy', 'dizzy','normal','cold'],
        ]

    def tearDown(self):
        self.sequences = None

    def test_hmm_explicit(self):
        all_observations = ['normal', 'cold', 'dizzy']
        all_states = ['healthy', 'fever']
        start_probs = {"healthy": 0.6, "fever": 0.4}
        trans_probs = [
            [0.7, 0.3],
            [0.4, 0.6]
        ]
        emission_probs = [
            [0.5, 0.4, 0.1],
            [0.1, 0.3, 0.6]
        ]

        hmm = Hmm(
            all_observations,
            all_states,
            trans_probs,
            emission_probs,
            start_probs
        )
        hmm.learn(self.sequences, delta=0.1, k_smoothing=0.1)
        self._check_output(hmm)

    def test_hmm_builder(self):
        builder = Builder()
        obs = [
            ['normal', 'cold', 'dizzy', 'dizzy','normal','normal'],
            ['dizzy', 'cold', 'dizzy', 'normal','normal','normal'],
            ['dizzy', 'cold', 'dizzy', 'normal','normal','normal']
        ]
        states = [
            ['healthy', 'healthy', 'fever', 'fever', 'healthy', 'healthy'],
            ['fever', 'fever', 'fever', 'healthy', 'healthy', 'fever'],
            ['fever', 'fever', 'fever', 'healthy', 'healthy', 'fever'],
        ]
        builder.add_batch_training_examples(obs, states)
        hmm = builder.build()
        self._check_output(hmm)

    def _check_output(self, model):
        observation = ['cold', 'cold', 'dizzy','normal','normal']
        self.assertGreater(
            model.evaluate(observation),
            0
        )
        self.assertGreater(
            len(model.decode(observation)),
            0
        )
        self.assertGreater(
            len(set(model.decode(observation))),
            1
        )
